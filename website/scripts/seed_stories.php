<?php
/**
 * Creates DRAFT Stories and podcast episodes from seed.json (built by build_seed.mjs). Never publishes.
 * Images must already be in wp-content/uploads/bhr-seed/ (paths in seed.json are relative to the repo; only the
 * file name is used). Skips items whose slug already exists. Run:
 *   wp.sh eval-file - < seed_stories.php      (with BHR_SEED=/path/inside/container/seed.json)
 */

require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$seed = json_decode( (string) file_get_contents( getenv( 'BHR_SEED' ) ), true );
if ( ! $seed ) {
	WP_CLI::error( 'No seed data.' );
}
$dir    = WP_CONTENT_DIR . '/uploads/bhr-seed/';
$author = get_user_by( 'login', 'bhr_owner' );

function bhr_seed_p( $text ) {
	return "<!-- wp:paragraph -->\n<p>" . esc_html( $text ) . "</p>\n<!-- /wp:paragraph -->\n\n";
}

// "Publisher: domain.org/path" -> "Publisher | | https://domain.org/path"; anything else stays a title.
function bhr_seed_source( $s ) {
	if ( preg_match( '#^(.*?):\s*((?:https?://)?[a-z0-9.-]+\.[a-z]{2,}/\S*)$#i', $s, $m ) ) {
		$url = preg_match( '#^https?://#', $m[2] ) ? $m[2] : 'https://' . $m[2];
		return trim( $m[1] ) . ' | | ' . $url;
	}
	return $s;
}

function bhr_seed_image( $path, $dir, $title, $caption, $alt ) {
	$file = $dir . basename( $path );
	if ( ! $path || ! file_exists( $file ) ) {
		return 0;
	}
	$tmp = wp_tempnam( basename( $file ) );
	copy( $file, $tmp );
	$id = media_handle_sideload( array( 'name' => basename( $file ), 'tmp_name' => $tmp ), 0, $title, array( 'post_excerpt' => $caption ) );
	if ( is_wp_error( $id ) ) {
		WP_CLI::warning( basename( $file ) . ': ' . $id->get_error_message() );
		return 0;
	}
	update_post_meta( $id, '_wp_attachment_image_alt', $alt );
	return $id;
}

function bhr_seed_term( $taxonomy, $slug, $name = '' ) {
	$term = get_term_by( 'slug', $slug, $taxonomy );
	if ( ! $term && $name ) {
		$res  = wp_insert_term( $name, $taxonomy, array( 'slug' => $slug ) );
		$term = is_wp_error( $res ) ? null : get_term( $res['term_id'], $taxonomy );
	}
	return $term ? (int) $term->term_id : 0;
}

$made = 0;
foreach ( $seed['stories'] as $s ) {
	if ( get_page_by_path( $s['slug'], OBJECT, 'story' ) ) {
		WP_CLI::log( "skip {$s['slug']} (exists)" );
		continue;
	}
	$content = '';
	foreach ( $s['paragraphs'] as $p ) {
		$content .= bhr_seed_p( $p );
	}
	$id = wp_insert_post( array(
		'post_type'    => 'story',
		'post_status'  => 'draft',
		'post_title'   => $s['title'],
		'post_name'    => $s['slug'],
		'post_excerpt' => $s['excerpt'],
		'post_content' => $content,
		'post_author'  => $author ? $author->ID : 1,
	), true );
	if ( is_wp_error( $id ) ) {
		WP_CLI::warning( $s['slug'] . ': ' . $id->get_error_message() );
		continue;
	}
	wp_set_object_terms( $id, array( bhr_seed_term( 'section', $s['section'] ) ), 'section' );
	wp_set_object_terms( $id, array_map( function ( $d ) {
		return bhr_seed_term( 'domain', $d );
	}, $s['domains'] ), 'domain' );
	wp_set_object_terms( $id, array( bhr_seed_term( 'country', $s['country'], $s['country_name'] ) ), 'country' );
	wp_set_object_terms( $id, array( bhr_seed_term( 'era', $s['era'] ) ), 'era' );

	update_post_meta( $id, 'bhr_full_name', $s['title'] );
	update_post_meta( $id, 'bhr_birth_year', $s['birth'] );
	update_post_meta( $id, 'bhr_death_year', $s['death'] );
	update_post_meta( $id, 'bhr_sources', implode( "\n", array_map( 'bhr_seed_source', $s['sources'] ) ) );
	update_post_meta( $id, 'bhr_image_credit', $s['image_credit'] );
	update_post_meta( $id, 'bhr_seed_reel', $s['reel'] ); // where the text came from (publish/reels/<reel>.md)

	$caption = sprintf( '%s. %s.', $s['title'], $s['cover_caption'] );
	if ( $s['cover_source'] ) {
		$caption .= ' <a href="' . esc_url( $s['cover_source'] ) . '">Source</a>.';
	}
	$img = bhr_seed_image( $s['cover_name'], $dir, $s['title'], $caption, 'Portrait of ' . $s['title'] );
	if ( $img ) {
		set_post_thumbnail( $id, $img );
	}
	$made++;
}
WP_CLI::log( "Stories created as drafts: {$made}" );

$eps = 0;
foreach ( $seed['episodes'] as $e ) {
	if ( get_page_by_path( $e['slug'], OBJECT, 'bhr_episode' ) ) {
		continue;
	}
	$content = bhr_seed_p( 'Transcript to be added.' );
	$id      = wp_insert_post( array(
		'post_type'    => 'bhr_episode',
		'post_status'  => 'draft',
		'post_title'   => $e['title'],
		'post_name'    => $e['slug'],
		'post_excerpt' => implode( ' ', $e['paragraphs'] ),
		'post_content' => $content,
		'post_author'  => $author ? $author->ID : 1,
	), true );
	if ( is_wp_error( $id ) ) {
		continue;
	}
	update_post_meta( $id, 'bhr_episode_number', $e['number'] );
	update_post_meta( $id, 'bhr_spotify_url', BHR_PODCAST_SPOTIFY );
	$img = bhr_seed_image( $e['cover'], $dir, $e['title'], 'Episode cover, The Black History Room.', 'Cover of episode ' . $e['number'] );
	if ( $img ) {
		set_post_thumbnail( $id, $img );
	}
	$story = get_page_by_path( $e['story'], OBJECT, 'story' );
	if ( $story ) {
		update_post_meta( $id, 'bhr_related_posts', (string) $story->ID );
		update_post_meta( $story->ID, 'bhr_podcast_url', home_url( '/podcast/' . $e['slug'] . '/' ) );
	}
	$eps++;
}
WP_CLI::success( "Drafts: {$made} stories, {$eps} podcast episodes. Nothing was published." );

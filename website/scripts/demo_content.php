<?php
/**
 * TEMPORARY design-test content (placeholder text, generated images). Every item is tagged with the meta key
 * bhr_demo=1. Remove with:  wp.sh eval-file - < demo_content.php   (with BHR_DEMO=remove in the environment)
 * Never leave this content on the live site.
 */

require_once ABSPATH . 'wp-admin/includes/image.php';

$demo_ids = get_posts( array( 'post_type' => array( 'post', 'bhr_episode', 'attachment' ), 'post_status' => 'any', 'meta_key' => 'bhr_demo', 'posts_per_page' => -1, 'fields' => 'ids' ) );
if ( 'remove' === getenv( 'BHR_DEMO' ) ) {
	foreach ( $demo_ids as $id ) {
		'attachment' === get_post_type( $id ) ? wp_delete_attachment( $id, true ) : wp_delete_post( $id, true );
	}
	WP_CLI::success( 'Removed ' . count( $demo_ids ) . ' demo items.' );
	return;
}
if ( $demo_ids ) {
	WP_CLI::error( 'Demo content already exists (' . count( $demo_ids ) . ' items).' );
}

function bhr_demo_image( $n, $w, $h ) {
	$im    = imagecreatetruecolor( $w, $h );
	$tones = array( array( 120, 98, 70 ), array( 88, 74, 60 ), array( 140, 120, 92 ), array( 70, 62, 55 ) );
	$base  = $tones[ $n % 4 ];
	for ( $y = 0; $y < $h; $y++ ) {
		$f = 0.65 + 0.35 * ( $y / $h );
		imageline( $im, 0, $y, $w, $y, imagecolorallocate( $im, (int) ( $base[0] * $f ), (int) ( $base[1] * $f ), (int) ( $base[2] * $f ) ) );
	}
	$ink = imagecolorallocate( $im, 235, 225, 205 );
	imagestring( $im, 5, 30, $h - 50, 'DESIGN TEST IMAGE ' . $n . ' - placeholder, not a historical photo', $ink );
	ob_start();
	imagejpeg( $im, null, 85 );
	$bits = ob_get_clean();
	$up   = wp_upload_bits( "design-test-{$n}.jpg", null, $bits );
	$id   = wp_insert_attachment( array( 'post_mime_type' => 'image/jpeg', 'post_title' => "Design test image {$n}", 'post_status' => 'inherit' ), $up['file'] );
	wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $up['file'] ) );
	update_post_meta( $id, '_wp_attachment_image_alt', 'Placeholder image for design testing' );
	wp_update_post( array( 'ID' => $id, 'post_excerpt' => 'Placeholder image caption (design test).' ) );
	update_post_meta( $id, 'bhr_demo', 1 );
	return $id;
}

$lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus, posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Cras mattis consectetur purus sit amet fermentum.';
$body  = '';
foreach ( array( 'Background', 'The turning point', 'What happened next', 'Legacy' ) as $i => $h2 ) {
	$body .= "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">{$h2}</h2>\n<!-- /wp:heading -->\n\n";
	for ( $p = 0; $p < 6; $p++ ) {
		$body .= "<!-- wp:paragraph -->\n<p>{$lorem} {$lorem}</p>\n<!-- /wp:paragraph -->\n\n";
	}
	if ( 1 === $i ) {
		$body .= "<!-- wp:group {\"className\":\"is-style-bhr-disputed\"} -->\n<div class=\"wp-block-group is-style-bhr-disputed\"><!-- wp:paragraph -->\n<p>Example of a disputed-claim note (design test).</p>\n<!-- /wp:paragraph --></div>\n<!-- /wp:group -->\n\n";
		$body .= "<!-- wp:quote {\"className\":\"is-style-bhr-document\"} -->\n<blockquote class=\"wp-block-quote is-style-bhr-document\"><!-- wp:paragraph -->\n<p>Example of an archival document quote (design test).</p>\n<!-- /wp:paragraph --></blockquote>\n<!-- /wp:quote -->\n\n";
	}
}

$cats = array( 'forgotten-history', 'historical-figures', 'african-history', 'african-american-history', 'civil-rights', 'historical-figures', 'forgotten-history', 'science-innovation', 'african-history', 'historical-figures' );
$today = current_datetime();
foreach ( $cats as $n => $slug ) {
	$img = bhr_demo_image( $n + 1, 1600, 900 );
	$id  = wp_insert_post( array(
		'post_title'   => '[Design test ' . ( $n + 1 ) . '] Placeholder headline for a long historical story',
		'post_excerpt' => 'Placeholder deck: one or two sentences that tell the reader why this story matters. Design test only.',
		'post_content' => $body,
		'post_status'  => 'publish',
		'post_date'    => $today->modify( '-' . ( $n * 2 ) . ' hours' )->format( 'Y-m-d H:i:s' ),
		'post_category' => array( get_category_by_slug( $slug )->term_id ),
	) );
	set_post_thumbnail( $id, $img );
	update_post_meta( $id, 'bhr_demo', 1 );
	update_post_meta( $id, 'bhr_sources', "Placeholder source one | https://www.loc.gov/\nPlaceholder source two (book), page 12" );
	if ( $n < 3 ) {
		update_post_meta( $id, 'bhr_event_date', '1900-' . $today->modify( "+{$n} days" )->format( 'm-d' ) );
	}
}
$ep = wp_insert_post( array( 'post_type' => 'bhr_episode', 'post_title' => '[Design test] Placeholder episode', 'post_excerpt' => 'Placeholder description.', 'post_status' => 'publish' ) );
update_post_meta( $ep, 'bhr_demo', 1 );
update_post_meta( $ep, 'bhr_episode_number', 99 );
update_post_meta( $ep, 'bhr_spotify_url', 'https://open.spotify.com/show/42IinLdMCZx7RnXPFwY8Ih' );
WP_CLI::success( 'Created ' . count( $cats ) . ' demo posts, ' . count( $cats ) . ' images, 1 demo episode.' );

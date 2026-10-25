<?php
/**
 * Inserts archival images inside live stories as captioned figures (wp:image blocks), one after each chosen
 * H2 section. Uploads each file once (attachment meta bhr_inline_key = "<slug>/<key>"), re-uses it afterwards,
 * and replaces any figures it inserted before, so it can be re-run.
 *   BHR_JSON=<plan>  content/inline-images-*.json   BHR_DIR=<folder with "<slug>__<file>" images>
 *   BHR_ONLY=slug1,slug2   BHR_DRY=1 (report only)
 * Run: wp eval-file - < insert_images.php
 */
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$plan = json_decode( (string) file_get_contents( getenv( 'BHR_JSON' ) ), true );
$dir  = rtrim( getenv( 'BHR_DIR' ), '/' ) . '/';
$only = array_filter( explode( ',', (string) getenv( 'BHR_ONLY' ) ) );
$dry  = (bool) getenv( 'BHR_DRY' );
if ( ! $plan ) {
	WP_CLI::error( 'No plan.' );
}

function bhr_find_attachment( $key ) {
	$q = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'any', 'meta_key' => 'bhr_inline_key', 'meta_value' => $key, 'posts_per_page' => 1, 'fields' => 'ids' ) );
	return $q ? (int) $q[0] : 0;
}

function bhr_figure( $id, $im ) {
	$src   = wp_get_attachment_image_url( $id, 'large' );
	$meta  = wp_get_attachment_metadata( $id );
	$size  = isset( $meta['sizes']['large'] ) ? $meta['sizes']['large'] : $meta;
	$cred  = esc_html( $im['credit'] );
	$lic   = esc_html( $im['license'] );
	$link  = $im['source'] ? ' &middot; <a href="' . esc_url( $im['source'] ) . '" rel="noopener nofollow" target="_blank">Source</a>' : '';
	$cap   = esc_html( $im['caption'] ) . ' <span class="bhr-credit">' . $cred . ' &middot; ' . $lic . $link . '</span>';
	$attrs = wp_json_encode( array( 'id' => $id, 'sizeSlug' => 'large', 'linkDestination' => 'none', 'className' => 'bhr-figure' ) );
	return "<!-- wp:image $attrs -->\n<figure class=\"wp-block-image size-large bhr-figure\"><img src=\"" . esc_url( $src ) . '" alt="' . esc_attr( $im['alt'] ) . '" class="wp-image-' . $id . '" width="' . (int) $size['width'] . '" height="' . (int) $size['height'] . "\"/><figcaption class=\"wp-element-caption\">$cap</figcaption></figure>\n<!-- /wp:image -->\n\n";
}

foreach ( $plan['stories'] as $slug => $st ) {
	if ( $only && ! in_array( $slug, $only, true ) ) {
		continue;
	}
	$story = get_page_by_path( $slug, OBJECT, 'story' );
	if ( ! $story ) {
		WP_CLI::warning( "no live story $slug" );
		continue;
	}
	// Drop figures from a previous run, then split into H2 sections.
	$content = preg_replace( '~<!-- wp:image \{[^\n]*"className":"bhr-figure"[^\n]*\} -->.*?<!-- /wp:image -->\n*~s', '', $story->post_content );
	$parts   = preg_split( '~(?=<!-- wp:heading -->)~', $content );
	$nsec    = count( $parts ) - 1; // parts[0] is anything before the first H2
	$added   = array();
	foreach ( $st['images'] as $im ) {
		$key = "$slug/{$im['key']}";
		$id  = bhr_find_attachment( $key );
		if ( ! $id && ! $dry ) {
			$file = $dir . $slug . '__' . $im['file'];
			if ( ! is_readable( $file ) ) {
				WP_CLI::warning( "missing $file" );
				continue;
			}
			$tmp = wp_tempnam( $im['file'] );
			copy( $file, $tmp );
			$id = media_handle_sideload( array( 'name' => $slug . '-' . $im['file'], 'tmp_name' => $tmp ), $story->ID, $im['caption'], array( 'post_excerpt' => $im['caption'] . ' ' . $im['credit'] . ' (' . $im['license'] . ')' ) );
			if ( is_wp_error( $id ) ) {
				WP_CLI::warning( $file . ': ' . $id->get_error_message() );
				continue;
			}
			update_post_meta( $id, '_wp_attachment_image_alt', $im['alt'] );
			update_post_meta( $id, 'bhr_inline_key', $key );
			update_post_meta( $id, 'bhr_image_credit', $im['credit'] . ' | ' . $im['license'] . ' | ' . $im['source'] );
		}
		$at = max( 1, min( $nsec, (int) $im['after'] ) );
		if ( $id ) {
			$parts[ $at ] = rtrim( $parts[ $at ] ) . "\n\n" . bhr_figure( $id, $im );
		}
		$added[] = $im['key'] . '@' . $at . ( $id ? '' : '(dry)' );
	}
	if ( ! $dry ) {
		wp_update_post( array( 'ID' => $story->ID, 'post_content' => implode( '', $parts ) ) );
	}
	WP_CLI::log( sprintf( '%-26s %d sections, figures: %s', $slug, $nsec, implode( ' ', $added ) ) );
}
WP_CLI::success( $dry ? 'Dry run complete.' : 'Figures inserted.' );

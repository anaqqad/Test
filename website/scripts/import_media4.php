<?php
/**
 * Item 4 import: podcast episode chapters + transcripts (episodes stay DRAFTS), and reel cover stills for the
 * Reels & Videos page (meta bhr_reel_cover on each story). Idempotent: existing covers are kept.
 * Run: wp eval-file - < import_media4.php   with BHR_DIR=<folder inside the container with data.json + covers>
 */
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$dir  = rtrim( getenv( 'BHR_DIR' ), '/' ) . '/';
$data = json_decode( (string) file_get_contents( $dir . 'data.json' ), true );

foreach ( $data['episodes'] as $e ) {
	$ep = get_page_by_path( $e['slug'], OBJECT, 'bhr_episode' );
	if ( ! $ep ) {
		WP_CLI::warning( "episode {$e['slug']} not found" );
		continue;
	}
	wp_update_post( array( 'ID' => $ep->ID, 'post_content' => $e['transcript'] ) );
	update_post_meta( $ep->ID, 'bhr_chapters', implode( "\n", $e['chapters'] ) );
	update_post_meta( $ep->ID, 'bhr_episode_number', (int) $e['number'] );
	update_post_meta( $ep->ID, 'bhr_spotify_url', 'https://open.spotify.com/show/42IinLdMCZx7RnXPFwY8Ih' );
	WP_CLI::log( sprintf( 'episode %d %s: %s, %d chapters, transcript, cover %s', $e['number'], $e['slug'], get_post_status( $ep ), count( $e['chapters'] ), has_post_thumbnail( $ep ) ? 'yes' : 'no' ) );
}

$n = 0;
foreach ( $data['reels'] as $r ) {
	$story = get_page_by_path( $r['story'], OBJECT, 'story' );
	if ( ! $story || get_post_meta( $story->ID, 'bhr_reel_cover', true ) ) {
		continue;
	}
	$tmp = wp_tempnam( $r['file'] );
	copy( $dir . $r['file'], $tmp );
	$id = media_handle_sideload( array( 'name' => $r['file'], 'tmp_name' => $tmp ), $story->ID, 'Reel cover: ' . $story->post_title );
	if ( is_wp_error( $id ) ) {
		WP_CLI::warning( $r['file'] . ': ' . $id->get_error_message() );
		continue;
	}
	update_post_meta( $id, '_wp_attachment_image_alt', 'Reel cover: ' . $story->post_title );
	update_post_meta( $story->ID, 'bhr_reel_cover', $id );
	$n++;
}
WP_CLI::success( "Reel covers added: $n" );

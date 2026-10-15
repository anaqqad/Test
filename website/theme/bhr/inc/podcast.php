<?php
/**
 * Podcast "Black History in 10 Minutes": an Episode post type with its own fields.
 * Archive at /podcast/, episodes at /podcast/<slug>/.
 * Title = episode title, Excerpt = description, Content = transcript, Featured image = episode cover.
 */

defined( 'ABSPATH' ) || exit;

const BHR_PODCAST_NAME    = 'Black History in 10 Minutes';
const BHR_PODCAST_SPOTIFY = 'https://open.spotify.com/show/42IinLdMCZx7RnXPFwY8Ih';

add_action( 'init', function () {
	register_post_type( 'bhr_episode', array(
		'labels'        => array(
			'name'          => 'Podcast episodes',
			'singular_name' => 'Podcast episode',
			'add_new_item'  => 'Add episode',
			'edit_item'     => 'Edit episode',
			'menu_name'     => 'Podcast',
		),
		'public'        => true,
		'has_archive'   => 'podcast',
		'rewrite'       => array( 'slug' => 'podcast', 'with_front' => false ),
		'menu_icon'     => 'dashicons-microphone',
		'menu_position' => 6,
		'show_in_rest'  => true,
		'rest_base'     => 'episodes',
		'supports'      => array( 'title', 'editor', 'excerpt', 'thumbnail', 'custom-fields', 'revisions' ),
	) );

	$auth   = function () {
		return current_user_can( 'edit_posts' );
	};
	$fields = array(
		'bhr_episode_number' => array( 'integer', 'absint' ),
		'bhr_spotify_url'    => array( 'string', 'esc_url_raw' ),
		'bhr_youtube_url'    => array( 'string', 'esc_url_raw' ),
		'bhr_apple_url'      => array( 'string', 'esc_url_raw' ),
		// Comma-separated post IDs of related articles.
		'bhr_related_posts'  => array( 'string', 'sanitize_text_field' ),
	);
	foreach ( $fields as $key => $def ) {
		register_post_meta( 'bhr_episode', $key, array(
			'type'              => $def[0],
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => $def[1],
			'auth_callback'     => $auth,
		) );
	}
} );

// Show up to 20 episodes per archive page (newest first).
add_action( 'pre_get_posts', function ( $query ) {
	if ( ! is_admin() && $query->is_main_query() && $query->is_post_type_archive( 'bhr_episode' ) ) {
		$query->set( 'posts_per_page', 20 );
	}
} );

function bhr_episode_links( $post = null ) {
	$id    = get_post( $post )->ID;
	$links = array(
		'Spotify'        => get_post_meta( $id, 'bhr_spotify_url', true ),
		'YouTube'        => get_post_meta( $id, 'bhr_youtube_url', true ),
		'Apple Podcasts' => get_post_meta( $id, 'bhr_apple_url', true ),
	);
	return array_filter( $links );
}

function bhr_episode_related( $post = null ) {
	$ids = array_filter( array_map( 'absint', explode( ',', (string) get_post_meta( get_post( $post )->ID, 'bhr_related_posts', true ) ) ) );
	return $ids ? get_posts( array( 'post__in' => $ids, 'orderby' => 'post__in', 'posts_per_page' => 6 ) ) : array();
}

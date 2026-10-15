<?php
/**
 * Article data: extra fields, reading time, table of contents, "this week" and related stories.
 *
 * Extra post fields (all editable in the editor's "Custom fields" panel and through the REST API for n8n):
 *   bhr_sources     one source per line: "Title | https://url" (URL optional)
 *   bhr_event_date  date of the historical event, YYYY-MM-DD; feeds "This week in Black history"
 * The deck (subtitle) is the post's Excerpt.
 */

defined( 'ABSPATH' ) || exit;

add_action( 'init', function () {
	add_post_type_support( 'post', 'custom-fields' );
	$auth = function () {
		return current_user_can( 'edit_posts' );
	};
	register_post_meta( 'post', 'bhr_sources', array(
		'type'              => 'string',
		'single'            => true,
		'show_in_rest'      => true,
		'sanitize_callback' => 'sanitize_textarea_field',
		'auth_callback'     => $auth,
	) );
	register_post_meta( 'post', 'bhr_event_date', array(
		'type'              => 'string',
		'single'            => true,
		'show_in_rest'      => true,
		'sanitize_callback' => function ( $value ) {
			return preg_match( '/^\d{1,4}-\d{2}-\d{2}$/', (string) $value ) ? $value : '';
		},
		'auth_callback'     => $auth,
	) );
} );

function bhr_reading_time( $post = null ) {
	$words = str_word_count( wp_strip_all_tags( (string) get_post_field( 'post_content', $post ) ) );
	return max( 1, (int) ceil( $words / 220 ) );
}

/**
 * Sources as a list of [title, url].
 */
function bhr_sources( $post = null ) {
	$raw   = (string) get_post_meta( get_post( $post )->ID, 'bhr_sources', true );
	$items = array();
	foreach ( preg_split( '/\R/', $raw ) as $line ) {
		$line = trim( $line );
		if ( '' === $line ) {
			continue;
		}
		$parts   = array_map( 'trim', explode( '|', $line, 2 ) );
		$items[] = array( $parts[0], isset( $parts[1] ) ? $parts[1] : '' );
	}
	return $items;
}

/**
 * Adds ids to <h2> headings and returns the headings for a table of contents.
 */
function bhr_toc_prepare( $content, &$items ) {
	$items = array();
	$used  = array();
	return preg_replace_callback( '#<h2([^>]*)>(.*?)</h2>#is', function ( $m ) use ( &$items, &$used ) {
		$attrs = $m[1];
		$text  = wp_strip_all_tags( $m[2] );
		if ( preg_match( '/\sid=["\']([^"\']+)["\']/', $attrs, $id ) ) {
			$slug = $id[1];
		} else {
			$slug = sanitize_title( $text ) ?: 'section';
			$base = $slug;
			$n    = 2;
			while ( isset( $used[ $slug ] ) ) {
				$slug = $base . '-' . $n++;
			}
			$attrs .= ' id="' . esc_attr( $slug ) . '"';
		}
		$used[ $slug ] = true;
		$items[]       = array( $slug, $text );
		return '<h2' . $attrs . '>' . $m[2] . '</h2>';
	}, $content );
}

// Table of contents on long articles: 3+ sections and 1,200+ words.
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( array( 'post', 'story' ) ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$items   = array();
	$content = bhr_toc_prepare( $content, $items );
	if ( count( $items ) < 3 || str_word_count( wp_strip_all_tags( $content ) ) < 1200 ) {
		return $content;
	}
	$toc = '<nav class="toc" aria-label="In this story"><p class="toc-title">In this story</p><ol>';
	foreach ( $items as $item ) {
		$toc .= '<li><a href="#' . esc_attr( $item[0] ) . '">' . esc_html( $item[1] ) . '</a></li>';
	}
	return $toc . '</ol></nav>' . $content;
}, 20 );

/**
 * Primary category (Yoast's "primary" choice if set, else the first category).
 */
function bhr_primary_category( $post = null ) {
	$post = get_post( $post );
	if ( ! $post ) {
		return null;
	}
	$primary = (int) get_post_meta( $post->ID, '_yoast_wpseo_primary_category', true );
	if ( $primary && ( $term = get_term( $primary, 'category' ) ) && ! is_wp_error( $term ) ) {
		return $term;
	}
	$cats = get_the_category( $post->ID );
	return $cats ? $cats[0] : null;
}

/**
 * Posts whose historical event falls in the next 7 days (any year).
 */
function bhr_this_week_query( $count = 4 ) {
	$days = array();
	$now  = current_datetime();
	for ( $i = 0; $i < 7; $i++ ) {
		$days[] = $now->modify( "+{$i} days" )->format( 'm-d' );
	}
	return new WP_Query( array(
		'post_type'           => array( 'story', 'post' ),
		'posts_per_page'      => $count,
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
		'meta_query'          => array(
			array(
				'key'     => 'bhr_event_date',
				'value'   => '-(' . implode( '|', $days ) . ')$',
				'compare' => 'REGEXP',
			),
		),
	) );
}

function bhr_related_query( $post = null, $count = 3 ) {
	$post = get_post( $post );
	$cat  = bhr_primary_category( $post );
	if ( ! $cat ) {
		return null;
	}
	return new WP_Query( array(
		'posts_per_page'      => $count,
		'cat'                 => $cat->term_id,
		'post__not_in'        => array( $post->ID ),
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	) );
}

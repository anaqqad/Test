<?php
/**
 * Section page URLs and listing filters.
 *
 *   /african-american-history/                     section page (WordPress page with that slug)
 *   /african-american-history/<domain>/            same page, filtered by domain
 *   /global-african-history/                       section page with the world map
 *   /global-african-history/topic/<domain>/        Global section filtered by domain
 *   /global-african-history/<iso2>/                Country archive (Country taxonomy)
 * Filters on section pages (GET): bhr_domain, bhr_country, bhr_era, bhr_letter, bhr_pg
 */

defined( 'ABSPATH' ) || exit;

add_filter( 'query_vars', function ( $vars ) {
	return array_merge( $vars, array( 'bhr_domain', 'bhr_country', 'bhr_era', 'bhr_letter', 'bhr_pg' ) );
} );

add_action( 'init', function () {
	add_rewrite_rule( '^african-american-history/([a-z0-9-]+)/?$', 'index.php?pagename=african-american-history&bhr_domain=$matches[1]', 'top' );
	add_rewrite_rule( '^global-african-history/topic/([a-z0-9-]+)/?$', 'index.php?pagename=global-african-history&bhr_domain=$matches[1]', 'top' );
} );

/**
 * Stories for a section page, from the current filters.
 */
function bhr_section_query( $section, $per_page = 12 ) {
	$tax = array(
		array( 'taxonomy' => 'section', 'field' => 'slug', 'terms' => $section ),
	);
	foreach ( array( 'domain' => 'bhr_domain', 'country' => 'bhr_country', 'era' => 'bhr_era' ) as $taxonomy => $var ) {
		$value = sanitize_title( (string) get_query_var( $var ) );
		if ( $value ) {
			$tax[] = array( 'taxonomy' => $taxonomy, 'field' => 'slug', 'terms' => $value );
		}
	}
	$args   = array(
		'post_type'      => 'story',
		'posts_per_page' => $per_page,
		'paged'          => max( 1, (int) get_query_var( 'bhr_pg' ) ),
		'tax_query'      => $tax,
	);
	$letter = strtoupper( substr( (string) get_query_var( 'bhr_letter' ), 0, 1 ) );
	if ( preg_match( '/^[A-Z]$/', $letter ) ) {
		$args['bhr_title_letter'] = $letter; // private arg: the public query var also reaches the main query
		$args['orderby']    = 'title';
		$args['order']      = 'ASC';
	}
	return new WP_Query( $args );
}

// A–Z filter: title starts with the letter.
add_filter( 'posts_where', function ( $where, $query ) {
	$letter = $query->get( 'bhr_title_letter' );
	if ( $letter ) {
		global $wpdb;
		$where .= $wpdb->prepare( " AND {$wpdb->posts}.post_title LIKE %s", $wpdb->esc_like( $letter ) . '%' );
	}
	return $where;
}, 10, 2 );

/**
 * Countries with published stories: [iso2 => [name, count, url]].
 */
function bhr_country_counts() {
	$cached = wp_cache_get( 'bhr_country_counts', 'bhr' );
	if ( false !== $cached ) {
		return $cached;
	}
	$out   = array();
	$terms = get_terms( array( 'taxonomy' => 'country', 'hide_empty' => true, 'orderby' => 'name' ) );
	foreach ( is_wp_error( $terms ) ? array() : $terms as $term ) {
		$out[ strtolower( $term->slug ) ] = array( $term->name, (int) $term->count, get_term_link( $term ) );
	}
	wp_cache_set( 'bhr_country_counts', $out, 'bhr', HOUR_IN_SECONDS );
	return $out;
}
add_action( 'set_object_terms', function () {
	wp_cache_delete( 'bhr_country_counts', 'bhr' );
} );
add_action( 'transition_post_status', function () {
	wp_cache_delete( 'bhr_country_counts', 'bhr' );
} );

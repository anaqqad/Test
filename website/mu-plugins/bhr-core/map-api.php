<?php
/**
 * Data for the interactive story map: GET /wp-json/bhr/v1/map (public, read-only, published stories only).
 * One small cached JSON document; the browser filters it (time, gender, subject, section, country) instantly.
 */

defined( 'ABSPATH' ) || exit;

function bhr_year_number( $value ) {
	return preg_match( '/-?\d{1,4}/', (string) $value, $m ) ? (int) $m[0] : null;
}

function bhr_map_data() {
	$cached = get_transient( 'bhr_map_data' );
	if ( false !== $cached ) {
		return $cached;
	}
	$stories = array();
	$posts   = get_posts( array( 'post_type' => 'story', 'post_status' => 'publish', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC' ) );
	foreach ( $posts as $p ) {
		$terms = function ( $tax ) use ( $p ) {
			$t = get_the_terms( $p, $tax );
			return ( $t && ! is_wp_error( $t ) ) ? $t : array();
		};
		$country = $terms( 'country' );
		$domains = $terms( 'domain' );
		$birth   = bhr_year_number( get_post_meta( $p->ID, 'bhr_birth_year', true ) );
		$death   = bhr_year_number( get_post_meta( $p->ID, 'bhr_death_year', true ) );
		$key     = bhr_year_number( get_post_meta( $p->ID, 'bhr_key_year', true ) );
		$from    = $birth ?? $key;
		$to      = $death ?? ( $key ?? $birth );
		$lat     = get_post_meta( $p->ID, 'bhr_lat', true );
		$lng     = get_post_meta( $p->ID, 'bhr_lng', true );
		$thumb   = get_post_thumbnail_id( $p );
		$stories[] = array(
			'id'    => $p->ID,
			't'     => html_entity_decode( get_the_title( $p ), ENT_QUOTES, 'UTF-8' ),
			'y'     => function_exists( 'bhr_story_years' ) ? bhr_story_years( $p ) : '',
			'u'     => get_permalink( $p ),
			'e'     => html_entity_decode( wp_strip_all_tags( get_the_excerpt( $p ) ), ENT_QUOTES, 'UTF-8' ),
			'img'   => $thumb ? wp_get_attachment_image_url( $thumb, 'bhr-card43-sm' ) : '',
			'img2'  => $thumb ? wp_get_attachment_image_url( $thumb, 'bhr-card43' ) : '',
			'c'     => $country ? strtolower( $country[0]->slug ) : '',
			's'     => wp_list_pluck( $terms( 'section' ), 'slug' ),
			'd'     => wp_list_pluck( $domains, 'slug' ),
			'dn'    => $domains ? html_entity_decode( $domains[0]->name, ENT_QUOTES, 'UTF-8' ) : '',
			'g'     => wp_list_pluck( $terms( 'gender' ), 'slug' ),
			'from'  => $from,
			'to'    => $to,
			'place' => ( is_numeric( $lat ) && is_numeric( $lng ) ) ? array( 'n' => (string) get_post_meta( $p->ID, 'bhr_place_name', true ), 'lat' => (float) $lat, 'lng' => (float) $lng ) : null,
		);
	}
	$names = function ( $tax ) {
		$out   = array();
		$terms = get_terms( array( 'taxonomy' => $tax, 'hide_empty' => false ) );
		foreach ( is_wp_error( $terms ) ? array() : $terms as $t ) {
			$out[ strtolower( $t->slug ) ] = html_entity_decode( $t->name );
		}
		return $out;
	};
	$used_countries = array_unique( array_filter( wp_list_pluck( $stories, 'c' ) ) );
	$countries      = array_intersect_key( $names( 'country' ), array_flip( $used_countries ) );
	asort( $countries );
	$data = array(
		'stories'   => $stories,
		'countries' => $countries,
		'domains'   => array_intersect_key( $names( 'domain' ), array_flip( array_unique( array_merge( array(), ...wp_list_pluck( $stories, 'd' ) ) ) ) ),
		'sections'  => $names( 'section' ),
		'genders'   => $names( 'gender' ),
	);
	set_transient( 'bhr_map_data', $data, DAY_IN_SECONDS );
	return $data;
}

function bhr_map_data_flush() {
	delete_transient( 'bhr_map_data' );
}
add_action( 'save_post_story', 'bhr_map_data_flush' );
add_action( 'deleted_post', 'bhr_map_data_flush' );
add_action( 'set_object_terms', 'bhr_map_data_flush' );
add_action( 'transition_post_status', 'bhr_map_data_flush' );
add_action( 'updated_post_meta', function ( $mid, $post_id ) {
	if ( 'story' === get_post_type( $post_id ) ) {
		bhr_map_data_flush();
	}
}, 10, 2 );

add_action( 'rest_api_init', function () {
	register_rest_route( 'bhr/v1', '/map', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			$res = rest_ensure_response( bhr_map_data() );
			$res->header( 'Cache-Control', 'public, max-age=300' );
			return $res;
		},
	) );
} );

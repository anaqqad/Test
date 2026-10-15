<?php
/**
 * Section page: Global African History, with the interactive story map (Leaflet, loaded only here).
 */

$bhr_has_explorer = ! get_query_var( 'bhr_domain' );
if ( $bhr_has_explorer ) {
	wp_enqueue_style( 'leaflet', get_theme_file_uri( 'assets/leaflet/leaflet.css' ), array(), '1.9.4' );
	wp_enqueue_script( 'leaflet', get_theme_file_uri( 'assets/leaflet/leaflet.js' ), array(), '1.9.4', array( 'in_footer' => true, 'strategy' => 'defer' ) );
	wp_enqueue_script( 'bhr-explorer', get_theme_file_uri( 'assets/js/explorer.js' ), array( 'leaflet' ), BHR_VERSION, array( 'in_footer' => true, 'strategy' => 'defer' ) );
}

get_header();
bhr_render_section_page( 'global-african-history', $bhr_has_explorer );
get_footer();

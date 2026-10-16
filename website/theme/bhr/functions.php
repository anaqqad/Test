<?php
/**
 * The Black History Room: lightweight editorial theme.
 * No page builder, no jQuery on the front end, self-hosted fonts, one small CSS file.
 */

defined( 'ABSPATH' ) || exit;

define( 'BHR_VERSION', '1.3.6' );

require __DIR__ . '/inc/content.php';
require __DIR__ . '/inc/podcast.php';
require __DIR__ . '/inc/template-tags.php';
require __DIR__ . '/inc/stories.php';
require __DIR__ . '/inc/section.php';

add_action( 'after_setup_theme', function () {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'align-wide' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets' ) );
	remove_theme_support( 'core-block-patterns' );

	register_nav_menus( array(
		'primary' => 'Main menu',
		'footer'  => 'Footer menu',
	) );

	// Image sizes. Recommended featured image: 1600 x 900.
	set_post_thumbnail_size( 800, 450, true );
	add_image_size( 'bhr-card', 800, 450, true );
	add_image_size( 'bhr-hero', 1600, 900, true );
	add_image_size( 'bhr-social', 1200, 630, true );
	add_image_size( 'bhr-portrait', 600, 750, true );
	add_image_size( 'bhr-square', 600, 600, true );
	// 4:3 crops kept from the top of the image, so faces in portraits stay in frame.
	add_image_size( 'bhr-card43', 800, 600, array( 'center', 'top' ) );
	add_image_size( 'bhr-card43-sm', 480, 360, array( 'center', 'top' ) ); // phones (srcset)
	add_image_size( 'bhr-hero43', 1200, 900, array( 'center', 'top' ) );
} );

add_filter( 'image_size_names_choose', function ( $sizes ) {
	return $sizes + array( 'bhr-hero' => 'Hero 16:9', 'bhr-portrait' => 'Portrait 4:5' );
} );

// Uploaded JPEG/PNG are stored as WebP (smaller files). AVIF uploads are kept as AVIF.
add_filter( 'image_editor_output_format', function ( $formats ) {
	if ( wp_image_editor_supports( array( 'mime_type' => 'image/webp' ) ) ) {
		$formats['image/jpeg'] = 'image/webp';
		$formats['image/png']  = 'image/webp';
	}
	return $formats;
} );
add_filter( 'wp_editor_set_quality', function ( $quality, $mime ) {
	return 'image/webp' === $mime ? 80 : $quality;
}, 10, 2 );
// No originals larger than 2000 px are served.
add_filter( 'big_image_size_threshold', function () {
	return 2000;
} );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'bhr', get_stylesheet_uri(), array(), BHR_VERSION );
	wp_dequeue_style( 'classic-theme-styles' );
} );
add_filter( 'should_load_separate_core_block_assets', '__return_true' );

add_action( 'wp_head', function () {
	$fonts = array( 'playfair-display-latin-wght-normal.woff2', 'source-sans-3-latin-wght-normal.woff2' );
	foreach ( $fonts as $font ) {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( get_theme_file_uri( 'assets/fonts/' . $font ) )
		);
	}
}, 1 );

// Site icon: PNG files shipped with the theme (website/scripts/make_icon.php). WordPress would otherwise serve its
// WebP copy, which iOS does not accept as a home-screen icon. The Site Icon setting still points to the same image.
add_filter( 'site_icon_meta_tags', function () {
	$u = function ( $px ) {
		return esc_url( get_theme_file_uri( "assets/icon/site-icon-{$px}.png" ) );
	};
	return array(
		'<link rel="icon" href="' . $u( 16 ) . '" sizes="16x16" type="image/png" />',
		'<link rel="icon" href="' . $u( 32 ) . '" sizes="32x32" type="image/png" />',
		'<link rel="icon" href="' . $u( 192 ) . '" sizes="192x192" type="image/png" />',
		'<link rel="apple-touch-icon" href="' . $u( 180 ) . '" />',
		'<meta name="msapplication-TileImage" content="' . $u( 270 ) . '" />',
	);
} );

// Same PNGs for /favicon.ico and anything else asking WordPress for the site icon URL.
add_filter( 'get_site_icon_url', function ( $url, $size ) {
	$px = $size <= 16 ? 16 : ( $size <= 32 ? 32 : ( $size <= 180 ? 180 : ( $size <= 192 ? 192 : ( $size <= 270 ? 270 : 0 ) ) ) );
	return get_theme_file_uri( $px ? "assets/icon/site-icon-{$px}.png" : 'assets/icon/site-icon.png' );
}, 10, 2 );

// Social sharing: stories share their 1200x630 crop (Facebook's card shape) instead of the full portrait image.
add_filter( 'wpseo_opengraph_image_size', function () {
	return 'bhr-social';
} );
// Our uploads are stored as WebP: report the real type of the shared file (Yoast reports the upload's original type).
add_filter( 'wpseo_opengraph_image', function ( $url ) {
	$GLOBALS['bhr_og_url'] = $url;
	return $url;
} );
add_filter( 'wpseo_opengraph_image_type', function ( $type ) {
	$ext   = strtolower( pathinfo( (string) wp_parse_url( $GLOBALS['bhr_og_url'] ?? '', PHP_URL_PATH ), PATHINFO_EXTENSION ) );
	$types = array( 'webp' => 'image/webp', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg', 'png' => 'image/png', 'avif' => 'image/avif' );
	return $types[ $ext ] ?? $type;
} );

// Front-end clean-up: no emoji script, no generator tag, no XML-RPC discovery.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'rsd_link' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'wp_shortlink_wp_head' );
add_filter( 'emoji_svg_url', '__return_false' );
add_filter( 'xmlrpc_enabled', '__return_false' );
add_filter( 'wp_headers', function ( $headers ) {
	unset( $headers['X-Pingback'] );
	return $headers;
} );

// Editorial notes in the editor: Block > Styles on a Group block.
add_action( 'init', function () {
	$notes = array(
		'bhr-fact'           => 'Verified fact',
		'bhr-interpretation' => 'Interpretation',
		'bhr-disputed'       => 'Disputed claim',
		'bhr-legend'         => 'Legend / myth',
	);
	foreach ( $notes as $name => $label ) {
		register_block_style( 'core/group', array( 'name' => $name, 'label' => $label ) );
	}
	register_block_style( 'core/quote', array( 'name' => 'bhr-document', 'label' => 'Archival document' ) );
} );

add_filter( 'excerpt_length', function () {
	return 28;
} );
add_filter( 'excerpt_more', function () {
	return '…';
} );

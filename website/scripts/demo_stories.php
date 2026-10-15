<?php
/**
 * TEMPORARY design-test Stories (placeholder text, generated images), tagged bhr_demo=1 like demo_content.php.
 * Remove with demo_content.php and BHR_DEMO=remove. Never leave on the live site.
 */
require_once ABSPATH . 'wp-admin/includes/image.php';

$lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus, posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper.';
$rows  = array(
	array( 'us', 'United States', 'african-american-history', 'military', '19th-century', '1839', '1915' ),
	array( 'us', 'United States', 'african-american-history', 'sports', '20th-century', '1913', '1980' ),
	array( 'us', 'United States', 'african-american-history', 'science-medicine-invention', '20th-century', '1877', '1963' ),
	array( 'ml', 'Mali', 'global-african-history', 'politics-government', 'before-1500', '', '' ),
	array( 'gh', 'Ghana', 'global-african-history', 'politics-government', '20th-century', '1909', '1972' ),
	array( 'jm', 'Jamaica', 'global-african-history', 'civil-rights-activism', '20th-century', '1887', '1940' ),
	array( 'br', 'Brazil', 'global-african-history', 'arts-music-literature', '19th-century', '1839', '1908' ),
	array( 'gh', 'Ghana', 'global-african-history', 'education', '20th-century', '1875', '1927' ),
);
foreach ( $rows as $n => $r ) {
	$im = imagecreatetruecolor( 1200, 1200 );
	for ( $y = 0; $y < 1200; $y++ ) {
		$f = 0.6 + 0.4 * $y / 1200;
		imageline( $im, 0, $y, 1200, $y, imagecolorallocate( $im, (int) ( 110 * $f ), (int) ( 92 * $f ), (int) ( 70 * $f ) ) );
	}
	imagestring( $im, 5, 30, 1150, 'DESIGN TEST IMAGE - placeholder', imagecolorallocate( $im, 235, 225, 205 ) );
	ob_start();
	imagejpeg( $im, null, 85 );
	$up  = wp_upload_bits( "design-test-story-{$n}.jpg", null, ob_get_clean() );
	$img = wp_insert_attachment( array( 'post_mime_type' => 'image/jpeg', 'post_title' => 'Design test', 'post_status' => 'inherit' ), $up['file'] );
	wp_update_attachment_metadata( $img, wp_generate_attachment_metadata( $img, $up['file'] ) );
	update_post_meta( $img, 'bhr_demo', 1 );

	$id = wp_insert_post( array(
		'post_type'    => 'story',
		'post_status'  => 'publish',
		'post_author'  => get_user_by( 'login', 'bhr_owner' )->ID,
		'post_title'   => 'Design Test Person ' . ( $n + 1 ),
		'post_excerpt' => 'Placeholder summary of about forty words for the card and the deck. Design test only, not a real story. ' . substr( $lorem, 0, 90 ),
		'post_content' => str_repeat( "<!-- wp:paragraph -->\n<p>{$lorem} {$lorem}</p>\n<!-- /wp:paragraph -->\n\n", 5 ),
		'post_date'    => current_datetime()->modify( "-{$n} hours" )->format( 'Y-m-d H:i:s' ),
	) );
	set_post_thumbnail( $id, $img );
	update_post_meta( $id, 'bhr_demo', 1 );
	foreach ( array( 'section' => $r[2], 'domain' => $r[3], 'era' => $r[4] ) as $tax => $slug ) {
		wp_set_object_terms( $id, $slug, $tax );
	}
	$c = get_term_by( 'slug', $r[0], 'country' ) ?: get_term( wp_insert_term( $r[1], 'country', array( 'slug' => $r[0] ) )['term_id'], 'country' );
	wp_set_object_terms( $id, (int) $c->term_id, 'country' );
	update_post_meta( $id, 'bhr_birth_year', $r[5] );
	update_post_meta( $id, 'bhr_death_year', $r[6] );
	update_post_meta( $id, 'bhr_sources', "Placeholder source one | Library of Congress | https://www.loc.gov/\nPlaceholder source two | Example University Press" );
	update_post_meta( $id, 'bhr_image_credit', 'Design test placeholder image.' );
	update_post_meta( $id, 'bhr_reel_url', 'https://www.facebook.com/' );
	if ( 1 === $n ) {
		update_post_meta( $id, 'bhr_event_date', '1936-' . current_datetime()->format( 'm-d' ) );
	}
}
WP_CLI::success( count( $rows ) . ' design-test stories published (temporary).' );

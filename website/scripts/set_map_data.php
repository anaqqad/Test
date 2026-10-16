<?php
/**
 * Gender, map place (from the "Location tag" in publish/reels/<slug>.md, or the story's facts) and key year for the
 * 20 seeded stories. Coordinates are city/landmark centres, rounded to 0.01°.
 * Run: wp eval-file - < set_map_data.php
 */
$rows = array(
	// slug                      gender            place                                                   lat     lng
	'bass-reeves'              => array( 'man', 'Fort Smith, Arkansas (federal court)', 35.39, -94.40 ),
	'bessie-coleman'           => array( 'woman', 'Le Crotoy, France (Caudron flight school)', 50.22, 1.62 ),
	'booker-t-washington'      => array( 'man', 'The White House, Washington, D.C.', 38.90, -77.04 ),
	'ellen-craft'              => array( array( 'woman', 'man' ), 'Macon, Georgia (where the escape began)', 32.84, -83.63 ),
	'frederick-douglass'       => array( 'man', 'Washington, D.C. (Cedar Hill, his later home)', 38.86, -76.99 ),
	'garrett-morgan'           => array( 'man', 'Cleveland, Ohio (Lake Erie waterworks tunnel)', 41.50, -81.69 ),
	'george-washington-carver' => array( 'man', 'Diamond, Missouri (birthplace)', 36.99, -94.32 ),
	'harriet-tubman'           => array( 'woman', 'Combahee River, South Carolina', 32.65, -80.63 ),
	'henry-box-brown'          => array( 'man', 'Richmond, Virginia (sealed into the box)', 37.54, -77.44 ),
	'hiram-revels'             => array( 'man', 'United States Capitol, Washington, D.C.', 38.89, -77.01 ),
	'ida-b-wells'              => array( 'woman', 'Memphis, Tennessee', 35.15, -90.05 ),
	'jack-johnson'             => array( 'man', 'Reno, Nevada (the 1910 fight)', 39.53, -119.81 ),
	'jesse-owens'              => array( 'man', 'Olympic Stadium, Berlin, Germany (1936)', 52.51, 13.24 ),
	'major-taylor'             => array( 'man', 'Montreal, Quebec (1899 world championship)', 45.50, -73.57 ),
	'mansa-musa'               => array( 'man', 'Cairo, Egypt (1324 pilgrimage)', 30.04, 31.24 ),
	'matthew-henson'           => array( 'man', 'Washington, D.C. (where he met Peary, 1887)', 38.90, -77.03 ),
	'muhammad-ali'             => array( 'man', 'Houston, Texas (induction center, 1967)', 29.76, -95.37 ),
	'robert-smalls'            => array( 'man', 'Charleston Harbor, South Carolina', 32.78, -79.93 ),
	'rosa-parks'               => array( 'woman', 'Montgomery, Alabama', 32.38, -86.30 ),
	'sojourner-truth'          => array( 'woman', 'Kingston, New York (1828 court case)', 41.93, -73.99 ),
);
$key_years = array( 'mansa-musa' => '1324', 'ellen-craft' => '1848' ); // Craft: escape, December 1848 (reel notes)

foreach ( $rows as $slug => $r ) {
	foreach ( array( 'publish', 'draft' ) as $status ) {
		$ids = get_posts( array( 'post_type' => 'story', 'post_status' => $status, 'name' => 'publish' === $status ? $slug : $slug . '-expanded', 'fields' => 'ids', 'posts_per_page' => 1 ) );
		foreach ( $ids as $id ) {
			wp_set_object_terms( $id, (array) $r[0], 'gender' );
			update_post_meta( $id, 'bhr_place_name', $r[1] );
			update_post_meta( $id, 'bhr_lat', (string) $r[2] );
			update_post_meta( $id, 'bhr_lng', (string) $r[3] );
			if ( isset( $key_years[ $slug ] ) ) {
				update_post_meta( $id, 'bhr_key_year', $key_years[ $slug ] );
			}
		}
	}
}
delete_transient( 'bhr_map_data' );
WP_CLI::success( count( $rows ) . ' stories updated (live + expanded drafts).' );

<?php
/**
 * Story post type and its taxonomies.
 *
 * Story URLs:        /story/<slug>/            (all stories: /stories/)
 * Country archive:   /global-african-history/<iso2>/   (Country term slug = ISO 3166-1 alpha-2, e.g. "ma")
 * Section pages:     /african-american-history/ and /global-african-history/ are WordPress pages (see routes.php)
 */

defined( 'ABSPATH' ) || exit;

const BHR_SECTIONS = array(
	'african-american-history' => 'African American History',
	'global-african-history'   => 'Global African History',
);

const BHR_DOMAINS = array(
	'politics-government'        => 'Politics & Government',
	'civil-rights-activism'      => 'Civil Rights & Activism',
	'slavery-emancipation'       => 'Slavery & Emancipation',
	'military'                   => 'Military',
	'science-medicine-invention' => 'Science, Medicine & Invention',
	'business-economics'         => 'Business & Economics',
	'arts-music-literature'      => 'Arts, Music & Literature',
	'sports'                     => 'Sports',
	'religion'                   => 'Religion',
	'education'                  => 'Education',
	'women-in-history'           => 'Women in History',
	'exploration'                => 'Exploration',
	'law-justice'                => 'Law & Justice',
);

const BHR_ERAS = array(
	'before-1500'  => 'Before 1500',
	'16th-century' => '16th century',
	'17th-century' => '17th century',
	'18th-century' => '18th century',
	'19th-century' => '19th century',
	'20th-century' => '20th century',
	'21st-century' => '21st century',
);

add_action( 'init', function () {
	register_post_type( 'story', array(
		'labels'        => array(
			'name'          => 'Stories',
			'singular_name' => 'Story',
			'add_new_item'  => 'Add story',
			'edit_item'     => 'Edit story',
			'all_items'     => 'All stories',
			'search_items'  => 'Search stories',
		),
		'public'        => true,
		'has_archive'   => 'stories',
		'rewrite'       => array( 'slug' => 'story', 'with_front' => false ),
		'menu_icon'     => 'dashicons-book-alt',
		'menu_position' => 5,
		'show_in_rest'  => true,
		'rest_base'     => 'stories',
		'supports'      => array( 'title', 'editor', 'excerpt', 'thumbnail', 'author', 'revisions', 'custom-fields' ),
		'taxonomies'    => array( 'post_tag' ),
	) );

	$common = array(
		'public'            => true,
		'show_in_rest'      => true,
		'show_admin_column' => true,
		'hierarchical'      => true, // checkbox UI in the editor
	);
	register_taxonomy( 'section', 'story', $common + array(
		'labels'  => array( 'name' => 'Sections', 'singular_name' => 'Section' ),
		'rewrite' => array( 'slug' => 'section', 'with_front' => false ),
	) );
	register_taxonomy( 'domain', 'story', $common + array(
		'labels'  => array( 'name' => 'Domains', 'singular_name' => 'Domain' ),
		'rewrite' => array( 'slug' => 'topic', 'with_front' => false ),
	) );
	register_taxonomy( 'country', 'story', $common + array(
		'labels'  => array( 'name' => 'Countries', 'singular_name' => 'Country', 'add_new_item' => 'Add country (slug = ISO code, e.g. gh)' ),
		'rewrite' => array( 'slug' => 'global-african-history', 'with_front' => false ),
	) );
	register_taxonomy( 'era', 'story', $common + array(
		'labels'  => array( 'name' => 'Eras', 'singular_name' => 'Era' ),
		'rewrite' => array( 'slug' => 'era', 'with_front' => false ),
	) );
} );

/**
 * Creates the fixed Section / Domain / Era terms (run once: wp eval 'bhr_create_terms();').
 */
function bhr_create_terms() {
	foreach ( array( 'section' => BHR_SECTIONS, 'domain' => BHR_DOMAINS, 'era' => BHR_ERAS ) as $tax => $terms ) {
		$order = 0;
		foreach ( $terms as $slug => $name ) {
			if ( ! get_term_by( 'slug', $slug, $tax ) ) {
				wp_insert_term( $name, $tax, array( 'slug' => $slug ) );
			}
			update_term_meta( get_term_by( 'slug', $slug, $tax )->term_id, 'bhr_order', $order++ );
		}
	}
}

/**
 * Era slug for a year (negative = BCE).
 */
function bhr_era_for_year( $year ) {
	$year = (int) $year;
	if ( $year <= 1500 ) {
		return 'before-1500';
	}
	$century = (int) floor( ( $year - 1 ) / 100 ) + 1;
	$suffix  = 21 === $century ? 'st' : 'th';
	return min( $century, 21 ) . $suffix . '-century';
}

<?php
/**
 * One-time site structure: categories, pages, menus, reading/permalink/media settings.
 * Safe to run again (finds existing items by slug). Creates no articles.
 * Run on the VPS:  bash /opt/blackhistoryroom/scripts/wp.sh eval-file - < setup_content.php
 */

function bhr_p( $text ) {
	return "<!-- wp:paragraph -->\n<p>{$text}</p>\n<!-- /wp:paragraph -->\n\n";
}
function bhr_h( $text ) {
	return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">{$text}</h2>\n<!-- /wp:heading -->\n\n";
}
function bhr_list( array $items ) {
	$li = '';
	foreach ( $items as $item ) {
		$li .= "<!-- wp:list-item -->\n<li>{$item}</li>\n<!-- /wp:list-item -->\n";
	}
	return "<!-- wp:list -->\n<ul class=\"wp-block-list\">{$li}</ul>\n<!-- /wp:list -->\n\n";
}
function bhr_note( $text ) {
	return "<!-- wp:group {\"className\":\"is-style-bhr-interpretation\"} -->\n<div class=\"wp-block-group is-style-bhr-interpretation\">"
		. "<!-- wp:paragraph -->\n<p>{$text}</p>\n<!-- /wp:paragraph --></div>\n<!-- /wp:group -->\n\n";
}

// ---------- Categories ----------
$categories = array(
	'african-history'           => array( 'African History', 'Kingdoms, empires, people and ideas from the history of the African continent.' ),
	'african-american-history'  => array( 'African-American History', 'The history of Black Americans, from the colonial era to today.' ),
	'civil-rights'              => array( 'Civil Rights', 'The long struggle for equal rights, freedom and justice.' ),
	'slavery-emancipation'      => array( 'Slavery & Emancipation', 'Enslavement, resistance, escape and the road to freedom.' ),
	'historical-figures'        => array( 'Historical Figures', 'The lives of people who changed history.' ),
	'black-women-in-history'    => array( 'Black Women in History', 'Black women whose work and courage shaped history.' ),
	'science-innovation'        => array( 'Science & Innovation', 'Inventors, scientists, engineers and explorers.' ),
	'military-history'          => array( 'Military History', 'Black soldiers, sailors and pilots, and the wars they fought in.' ),
	'politics'                  => array( 'Politics', 'Black leaders, voters and movements in political life.' ),
	'arts-culture'              => array( 'Arts & Culture', 'Music, literature, art, sport and everyday culture.' ),
	'forgotten-history'         => array( 'Forgotten History', 'Stories most history books left out.' ),
	'black-business'            => array( 'Black Business', 'Entrepreneurs, businesses and economic history.' ),
	'timelines'                 => array( 'Timelines', 'Key events in order, with dates and sources.' ),
);

// The built-in "Uncategorized" (default category) becomes African-American History, so no empty
// "Uncategorized" category is left behind.
$default = (int) get_option( 'default_category' );
$uncat   = get_term( $default, 'category' );
if ( $uncat && 'uncategorized' === $uncat->slug && ! get_category_by_slug( 'african-american-history' ) ) {
	wp_update_term( $default, 'category', array(
		'name'        => $categories['african-american-history'][0],
		'slug'        => 'african-american-history',
		'description' => $categories['african-american-history'][1],
	) );
}

$cat_ids = array();
foreach ( $categories as $slug => $def ) {
	$term = get_category_by_slug( $slug );
	if ( ! $term ) {
		$res  = wp_insert_term( $def[0], 'category', array( 'slug' => $slug, 'description' => $def[1] ) );
		$term = get_term( $res['term_id'], 'category' );
	}
	$cat_ids[ $slug ] = (int) $term->term_id;
}
WP_CLI::log( 'Categories: ' . count( $cat_ids ) );

// ---------- Pages ----------
$placeholder = bhr_note( '<strong>Placeholder.</strong> This page still has to be written by the owner of The Black History Room. Nothing here is legal advice.' );

// The blog page is "News" (/news/); /stories/ is the Story archive.
if ( ( $old = get_page_by_path( 'stories' ) ) && ! get_page_by_path( 'news' ) ) {
	wp_update_post( array( 'ID' => $old->ID, 'post_name' => 'news', 'post_title' => 'News' ) );
}

$pages = array(
	'home'    => array( 'Home', '' ),
	'news'    => array( 'News', '' ),
	'african-american-history' => array(
		'African American History',
		bhr_p( 'The history of Black Americans, from the colonial era to today: leaders, inventors, soldiers, artists and ordinary people who changed the country.' ),
	),
	'global-african-history' => array(
		'Global African History',
		bhr_p( 'Africa and the African diaspora around the world. Choose a country on the map or in the list, or browse all stories below.' ),
	),
	'donate' => array(
		'Donate',
		bhr_p( 'Researching and editing these stories takes real time and effort. Every story is checked against reliable sources before it is published, and every image is checked for its rights.' )
		. bhr_p( 'If you value this work, please support The Black History Room so we can keep bringing these stories to light. Thank you!' )
		. "<!-- wp:buttons -->\n<div class=\"wp-block-buttons\"><!-- wp:button -->\n<div class=\"wp-block-button\"><a class=\"wp-block-button__link wp-element-button\" href=\"https://ko-fi.com/theblackhistoryroom\" target=\"_blank\" rel=\"noreferrer noopener\">Support us on Ko-fi</a></div>\n<!-- /wp:button --></div>\n<!-- /wp:buttons -->\n\n"
		. bhr_p( 'Donations are handled by Ko-fi. No payment information is collected or stored on this website.' ),
	),
	'videos'    => array( 'Reels & Videos', '' ),
	'this-week' => array( 'This Week in Black History', '' ),
	'sources'   => array(
		'Sources & Bibliography',
		bhr_p( 'Every story lists its own sources at the end. These are the archives and institutions we rely on most:' )
		. bhr_list( array(
			'<a href="https://www.loc.gov/">Library of Congress</a>',
			'<a href="https://www.archives.gov/">National Archives (US)</a>',
			'<a href="https://nmaahc.si.edu/">Smithsonian National Museum of African American History and Culture</a>',
			'<a href="https://history.house.gov/">US House of Representatives: History, Art &amp; Archives</a>',
			'<a href="https://www.nps.gov/">National Park Service</a>',
			'<a href="https://www.britannica.com/">Encyclopaedia Britannica</a>',
		) )
		. bhr_p( 'See our <a href="/editorial-policy/">Editorial Policy</a> for how we choose and check sources.' ),
	),
	'about'   => array(
		'About',
		bhr_p( 'The Black History Room shares powerful people, moments, struggles and achievements from Black history: from African kingdoms to the civil rights movement, from inventors and explorers to the stories most history books left out.' )
		. bhr_p( 'Every story is researched from reliable sources, such as archives, museums, universities and published scholarship. Each important fact is checked against at least two of them. Read our <a href="/editorial-policy/">Editorial Policy</a> to see how we work.' )
		. bhr_p( 'We also make the podcast <a href="/podcast/">Black History in 10 Minutes</a> and short videos on social media. If you value this work, you can support it on <a href="https://ko-fi.com/theblackhistoryroom">Ko-fi</a>.' )
		. bhr_note( '<strong>To complete:</strong> who is behind The Black History Room, and how to reach us.' ),
	),
	'contact' => array(
		'Contact',
		bhr_p( 'Questions, story ideas or corrections are welcome.' )
		. bhr_note( '<strong>Placeholder.</strong> The owner will add a contact email address here. For corrections, see our <a href="/corrections-policy/">Corrections Policy</a>.' ),
	),
	'editorial-policy' => array(
		'Editorial Policy',
		bhr_p( 'The Black History Room is a history publication. Accuracy comes first: a story that is not well sourced is not published.' )
		. bhr_h( 'Sources' )
		. bhr_p( 'Every important factual claim is checked against at least two independent, reliable sources. We prefer:' )
		. bhr_list( array(
			'primary sources: letters, records, newspapers, photographs and official documents of the time;',
			'archives and libraries, such as the Library of Congress and the National Archives;',
			'museums, such as the Smithsonian and the National Museum of African American History and Culture;',
			'universities, peer-reviewed research and reputable books by historians.',
		) )
		. bhr_p( 'Wikipedia can help us find sources, but it is never the only source for an important claim. Each article lists its sources at the end.' )
		. bhr_h( 'Fact, interpretation, dispute and legend' )
		. bhr_p( 'We keep these apart and label them in the text when it matters:' )
		. bhr_list( array(
			'<strong>Verified facts</strong> are supported by reliable sources.',
			'<strong>Historical interpretation</strong> is how historians explain or judge the facts; we say whose view it is.',
			'<strong>Disputed claims</strong> are points where sources or historians disagree; we say so and give both sides.',
			'<strong>Legends and myths</strong> are stories that are widely repeated but not supported by evidence; we label them clearly.',
		) )
		. bhr_p( 'We do not publish quotes we cannot trace to a reliable source. Many popular quotes attributed to famous figures are not genuine.' )
		. bhr_h( 'Images' )
		. bhr_p( 'We use real historical photographs and documents that are in the public domain or properly licensed, and we credit them. We do not use AI-generated images of real historical people.' )
		. bhr_h( 'AI-assisted work and human review' )
		. bhr_p( 'We may use software, including AI tools, to help find sources, organise research, draft text or prepare images that do not depict real people. AI is never treated as a source. Every story is fact-checked and approved by a person before it is published; automated tools can only create drafts.' )
		. bhr_h( 'Corrections' )
		. bhr_p( 'When we get something wrong, we fix it and say so. See our <a href="/corrections-policy/">Corrections Policy</a>.' ),
	),
	'corrections-policy' => array(
		'Corrections Policy',
		bhr_p( 'We work hard to get every fact right, but mistakes can happen. When they do, we correct them openly.' )
		. bhr_list( array(
			'If you believe a story contains an error, please tell us and include a source if you can (see <a href="/contact/">Contact</a>).',
			'We check every report against reliable sources.',
			'Factual errors are corrected in the article, with a short correction note at the end saying what was changed and when.',
			'Spelling and small wording fixes that do not change the meaning are made without a note.',
		) )
		. $placeholder,
	),
	'privacy-policy' => array( 'Privacy Policy', $placeholder ),
	'terms'          => array( 'Terms of Use', $placeholder ),
	'cookie-policy'  => array( 'Cookie Policy', $placeholder ),
);

$page_ids = array();
foreach ( $pages as $slug => $def ) {
	$existing = get_page_by_path( $slug );
	if ( 'privacy-policy' === $slug && ! $existing && ( $privacy = (int) get_option( 'wp_page_for_privacy_policy' ) ) ) {
		$existing = get_post( $privacy );
	}
	$data = array(
		'post_type'      => 'page',
		'post_status'    => 'publish',
		'post_title'     => $def[0],
		'post_name'      => $slug,
		'post_content'   => $def[1],
		'comment_status' => 'closed',
		'ping_status'    => 'closed',
	);
	if ( $existing ) {
		$data['ID'] = $existing->ID;
		$page_ids[ $slug ] = wp_update_post( $data, true );
	} else {
		$page_ids[ $slug ] = wp_insert_post( $data, true );
	}
	if ( is_wp_error( $page_ids[ $slug ] ) ) {
		WP_CLI::error( $slug . ': ' . $page_ids[ $slug ]->get_error_message() );
	}
}
WP_CLI::log( 'Pages: ' . count( $page_ids ) );

// ---------- Settings ----------
update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $page_ids['home'] );
update_option( 'page_for_posts', $page_ids['news'] );
update_option( 'wp_page_for_privacy_policy', $page_ids['privacy-policy'] );
update_option( 'posts_per_page', 12 );
update_option( 'category_base', 'topics' );
update_option( 'thumbnail_size_w', 300 );
update_option( 'thumbnail_size_h', 300 );
update_option( 'medium_size_w', 800 );
update_option( 'medium_size_h', 0 );
update_option( 'large_size_w', 1600 );
update_option( 'large_size_h', 0 );

// ---------- Menus ----------
function bhr_menu( $name, $location, array $items ) {
	$menu = wp_get_nav_menu_object( $name );
	$id   = $menu ? $menu->term_id : wp_create_nav_menu( $name );
	foreach ( wp_get_nav_menu_items( $id ) ?: array() as $old ) {
		wp_delete_post( $old->ID, true );
	}
	foreach ( $items as $i => $item ) {
		$args = array( 'menu-item-status' => 'publish', 'menu-item-position' => $i + 1, 'menu-item-title' => $item[0] );
		if ( 'page' === $item[1] || 'category' === $item[1] ) {
			$args += array( 'menu-item-type' => 'page' === $item[1] ? 'post_type' : 'taxonomy', 'menu-item-object' => $item[1], 'menu-item-object-id' => $item[2] );
		} else {
			$args += array( 'menu-item-type' => 'custom', 'menu-item-url' => $item[2] );
		}
		wp_update_nav_menu_item( $id, 0, $args );
	}
	$locations              = get_theme_mod( 'nav_menu_locations', array() );
	$locations[ $location ] = $id;
	set_theme_mod( 'nav_menu_locations', $locations );
	return count( $items );
}

$main = bhr_menu( 'Main menu', 'primary', array(
	array( 'Home', 'custom', home_url( '/' ) ),
	array( 'Stories', 'custom', home_url( '/stories/' ) ),
	array( 'People', 'category', $cat_ids['historical-figures'] ),
	array( 'Africa', 'category', $cat_ids['african-history'] ),
	array( 'African-American History', 'category', $cat_ids['african-american-history'] ),
	array( 'Civil Rights', 'category', $cat_ids['civil-rights'] ),
	array( 'Culture', 'category', $cat_ids['arts-culture'] ),
	array( 'Science & Innovation', 'category', $cat_ids['science-innovation'] ),
	array( 'Timelines', 'category', $cat_ids['timelines'] ),
	array( 'Podcast', 'custom', home_url( '/podcast/' ) ),
	array( 'About', 'page', $page_ids['about'] ),
) );
$footer = bhr_menu( 'Footer menu', 'footer', array(
	array( 'About', 'page', $page_ids['about'] ),
	array( 'Contact', 'page', $page_ids['contact'] ),
	array( 'Editorial Policy', 'page', $page_ids['editorial-policy'] ),
	array( 'Corrections Policy', 'page', $page_ids['corrections-policy'] ),
	array( 'Privacy Policy', 'page', $page_ids['privacy-policy'] ),
	array( 'Terms of Use', 'page', $page_ids['terms'] ),
	array( 'Cookie Policy', 'page', $page_ids['cookie-policy'] ),
	array( 'Donate', 'page', $page_ids['donate'] ),
) );
WP_CLI::log( "Menus: main {$main} items, footer {$footer} items" );

if ( function_exists( 'bhr_create_terms' ) ) {
	bhr_create_terms();
}
flush_rewrite_rules( false );
WP_CLI::success( 'Site structure ready.' );

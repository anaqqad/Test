<?php
/**
 * Story display: cards, title with years, citations, "Discover more". Data model is in mu-plugins/bhr-core.
 */

defined( 'ABSPATH' ) || exit;

/**
 * "Robert Smalls (1839–1915)" or the plain title.
 */
function bhr_story_title( $post = null ) {
	$post  = get_post( $post );
	$years = function_exists( 'bhr_story_years' ) ? bhr_story_years( $post ) : '';
	return get_the_title( $post ) . ( $years ? ' (' . $years . ')' : '' );
}

function bhr_story_term( $post, $taxonomy ) {
	$terms = get_the_terms( $post, $taxonomy );
	return ( $terms && ! is_wp_error( $terms ) ) ? $terms[0] : null;
}

/**
 * Story card: square image, name + years, two-line excerpt, Read more, date.
 */
function bhr_story_card( $heading = 'h3' ) {
	$heading = in_array( $heading, array( 'h2', 'h3' ), true ) ? $heading : 'h3';
	$years   = function_exists( 'bhr_story_years' ) ? bhr_story_years() : '';
	$domain  = bhr_story_term( get_post(), 'domain' );
	echo '<article class="scard">';
	echo '<a class="scard-media" href="' . esc_url( get_permalink() ) . '" tabindex="-1" aria-hidden="true">';
	if ( has_post_thumbnail() ) {
		the_post_thumbnail( 'bhr-square', array( 'sizes' => '(min-width: 64em) 360px, (min-width: 40em) 45vw, 100vw' ) );
	} else {
		echo '<span class="scard-placeholder">' . esc_html( mb_substr( get_the_title(), 0, 1 ) ) . '</span>';
	}
	echo '</a><div class="scard-body">';
	if ( $domain ) {
		echo '<p class="kicker kicker--static">' . esc_html( $domain->name ) . '</p>';
	}
	printf( '<%1$s class="scard-title"><a href="%2$s">%3$s</a></%1$s>', $heading, esc_url( get_permalink() ), esc_html( get_the_title() ) );
	if ( $years ) {
		echo '<p class="scard-years">' . esc_html( $years ) . '</p>';
	}
	if ( has_excerpt() ) {
		echo '<p class="scard-excerpt">' . esc_html( get_the_excerpt() ) . '</p>';
	}
	echo '<p class="scard-foot"><a class="scard-more" href="' . esc_url( get_permalink() ) . '">Read more<span class="screen-reader-text"> about ' . esc_html( get_the_title() ) . '</span></a>';
	echo '<time datetime="' . esc_attr( get_the_date( 'c' ) ) . '">' . esc_html( get_the_date() ) . '</time></p>';
	echo '</div></article>';
}

function bhr_story_grid( WP_Query $query, $heading = 'h3' ) {
	echo '<div class="grid grid--card">';
	while ( $query->have_posts() ) {
		$query->the_post();
		bhr_story_card( $heading );
	}
	wp_reset_postdata();
	echo '</div>';
}

/**
 * Citation parts: author (organisation unless the author has a last name), dates, title, URL.
 */
function bhr_citation_parts( $post = null ) {
	$post  = get_post( $post );
	$first = get_the_author_meta( 'first_name', $post->post_author );
	$last  = get_the_author_meta( 'last_name', $post->post_author );
	$ts    = get_post_timestamp( $post, 'date' ) ?: time();
	return array(
		'person' => $last ? array( $first, $last ) : null,
		'org'    => 'The Black History Room',
		'ts'     => $ts,
		'title'  => bhr_story_title( $post ),
		'url'    => get_permalink( $post ),
	);
}

function bhr_citations( $post = null ) {
	$c       = bhr_citation_parts( $post );
	$initial = $c['person'] && $c['person'][0] ? ' ' . mb_substr( $c['person'][0], 0, 1 ) . '.' : '';
	$apa_who = $c['person'] ? $c['person'][1] . ',' . $initial : $c['org'] . '.';
	$mla_who = $c['person'] ? $c['person'][1] . ( $c['person'][0] ? ', ' . $c['person'][0] : '' ) . '. ' : '';
	$chi_who = $c['person'] ? $c['person'][1] . ( $c['person'][0] ? ', ' . $c['person'][0] : '' ) . '.' : $c['org'] . '.';
	$mla_mon = array( 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.' );
	$m       = (int) wp_date( 'n', $c['ts'] ) - 1;
	return array(
		'APA'     => sprintf( '%s (%s). %s. %s. %s', $apa_who, wp_date( 'Y, F j', $c['ts'] ), $c['title'], $c['org'], $c['url'] ),
		'MLA'     => sprintf( '%s“%s.” %s, %s %s %s, %s.', $mla_who, $c['title'], $c['org'], wp_date( 'j', $c['ts'] ), $mla_mon[ $m ], wp_date( 'Y', $c['ts'] ), $c['url'] ),
		'Chicago' => sprintf( '%s “%s.” %s. %s. %s.', $chi_who, $c['title'], $c['org'], wp_date( 'F j, Y', $c['ts'] ), $c['url'] ),
	);
}

/**
 * Three related stories: same Country first, then same Domain, then same Section.
 */
function bhr_discover_more( $post = null, $count = 3 ) {
	$post  = get_post( $post );
	$found = array();
	foreach ( array( 'country', 'domain', 'section' ) as $taxonomy ) {
		if ( count( $found ) >= $count ) {
			break;
		}
		$terms = wp_get_post_terms( $post->ID, $taxonomy, array( 'fields' => 'ids' ) );
		if ( ! $terms || is_wp_error( $terms ) ) {
			continue;
		}
		$ids   = get_posts( array(
			'post_type'      => 'story',
			'posts_per_page' => $count - count( $found ),
			'post__not_in'   => array_merge( array( $post->ID ), $found ),
			'tax_query'      => array( array( 'taxonomy' => $taxonomy, 'terms' => $terms ) ),
			'fields'         => 'ids',
			'no_found_rows'  => true,
		) );
		$found = array_merge( $found, $ids );
	}
	return $found ? new WP_Query( array( 'post_type' => 'story', 'post__in' => $found, 'orderby' => 'post__in', 'no_found_rows' => true ) ) : null;
}

/**
 * The mega-menu structure. Links are built from the fixed term lists in bhr-core.
 */
function bhr_mega_menu() {
	$domains_aa = array();
	$domains_ga = array();
	foreach ( defined( 'BHR_DOMAINS' ) ? BHR_DOMAINS : array() as $slug => $name ) {
		$domains_aa[ $name ] = home_url( "/african-american-history/{$slug}/" );
		$domains_ga[ $name ] = home_url( "/global-african-history/topic/{$slug}/" );
	}
	return array(
		'african-american' => array(
			'label'   => 'African American History',
			'columns' => array(
				'Explore' => array( 'All African American history' => home_url( '/african-american-history/' ), 'All stories A–Z' => home_url( '/african-american-history/?bhr_letter=A' ) ),
				'By subject' => $domains_aa,
			),
		),
		'global' => array(
			'label'   => 'Global African History',
			'columns' => array(
				'Explore' => array( 'World map' => home_url( '/global-african-history/' ), 'Countries A–Z' => home_url( '/global-african-history/#countries' ) ),
				'By subject' => $domains_ga,
			),
		),
		'features' => array(
			'label'    => 'Special Features',
			'columns'  => array(
				'Collections' => array(
					'Podcast: ' . BHR_PODCAST_NAME => get_post_type_archive_link( 'bhr_episode' ),
					'Reels & videos'               => home_url( '/videos/' ),
					'This week in Black history'   => home_url( '/this-week/' ),
					'Timelines'                    => home_url( '/tag/timelines/' ),
					'Myths vs facts'               => home_url( '/tag/myths-vs-facts/' ),
				),
			),
			'featured' => true,
		),
		'resources' => array(
			'label'   => 'Resources',
			'columns' => array(
				'Resources' => array(
					'Sources & bibliography' => home_url( '/sources/' ),
					'Editorial policy'       => home_url( '/editorial-policy/' ),
					'Corrections'            => home_url( '/corrections-policy/' ),
					'News & updates'         => home_url( '/news/' ),
				),
			),
		),
		'about' => array(
			'label'   => 'About',
			'columns' => array(
				'About us' => array(
					'About'   => home_url( '/about/' ),
					'Contact' => home_url( '/contact/' ),
					'Donate'  => home_url( '/donate/' ),
				),
			),
		),
	);
}

<?php
/**
 * Small template helpers shared by the templates.
 */

defined( 'ABSPATH' ) || exit;

const BHR_KOFI = 'https://ko-fi.com/theblackhistoryroom';

function bhr_kicker( $post = null ) {
	$cat = bhr_primary_category( $post );
	if ( $cat ) {
		printf( '<a class="kicker" href="%s">%s</a>', esc_url( get_category_link( $cat ) ), esc_html( $cat->name ) );
	}
}

/**
 * Story card. $variant: "card" (image on top), "row" (image left), "text" (no image).
 */
function bhr_card( $variant = 'card', $heading = 'h3', $size = 'bhr-card' ) {
	$heading = in_array( $heading, array( 'h2', 'h3', 'h4' ), true ) ? $heading : 'h3';
	echo '<article class="story story--' . esc_attr( $variant ) . '">';
	if ( 'text' !== $variant && has_post_thumbnail() ) {
		echo '<a class="story-media" href="' . esc_url( get_permalink() ) . '" tabindex="-1" aria-hidden="true">';
		the_post_thumbnail( $size, array( 'sizes' => '(min-width: 64em) 380px, (min-width: 40em) 45vw, 100vw' ) );
		echo '</a>';
	}
	echo '<div class="story-body">';
	bhr_kicker();
	printf( '<%1$s class="story-title"><a href="%2$s">%3$s</a></%1$s>', $heading, esc_url( get_permalink() ), esc_html( get_the_title() ) );
	if ( 'text' !== $variant && has_excerpt() ) {
		echo '<p class="story-excerpt">' . esc_html( get_the_excerpt() ) . '</p>';
	}
	echo '<p class="story-meta"><time datetime="' . esc_attr( get_the_date( 'c' ) ) . '">' . esc_html( get_the_date() ) . '</time> · ' . esc_html( bhr_reading_time() ) . ' min read</p>';
	echo '</div></article>';
}

/**
 * A homepage section: heading, optional "see all" link, grid of cards. Prints nothing if the query is empty.
 */
function bhr_section( $title, WP_Query $query, $link = '', $variant = 'card', $class = '', $intro = '', $size = 'bhr-card' ) {
	if ( ! $query->have_posts() ) {
		return;
	}
	echo '<section class="home-section ' . esc_attr( $class ) . '"><div class="wrap">';
	echo '<header class="section-head"><h2 class="section-title">' . esc_html( $title ) . '</h2>';
	if ( $link ) {
		echo '<a class="section-more" href="' . esc_url( $link ) . '">See all</a>';
	}
	echo '</header>';
	if ( $intro ) {
		echo '<p class="section-intro">' . esc_html( $intro ) . '</p>';
	}
	echo '<div class="grid grid--' . esc_attr( $variant ) . '">';
	while ( $query->have_posts() ) {
		$query->the_post();
		bhr_card( $variant, 'h3', $size );
	}
	wp_reset_postdata();
	echo '</div></div></section>';
}

function bhr_category_url( $slug ) {
	$term = get_category_by_slug( $slug );
	return $term ? get_category_link( $term ) : '';
}

function bhr_share_links() {
	$url   = rawurlencode( get_permalink() );
	$title = rawurlencode( get_the_title() );
	$links = array(
		'X'        => "https://twitter.com/intent/tweet?url={$url}&text={$title}",
		'Facebook' => "https://www.facebook.com/sharer/sharer.php?u={$url}",
		'WhatsApp' => "https://wa.me/?text={$title}%20{$url}",
		'Email'    => "mailto:?subject={$title}&body={$url}",
	);
	echo '<div class="share"><span class="share-label">Share</span>';
	foreach ( $links as $name => $href ) {
		printf( '<a href="%s" rel="noopener nofollow" target="_blank">%s</a>', esc_url( $href ), esc_html( $name ) );
	}
	echo '</div>';
}

/**
 * Newsletter box. Shows a real form only once an email provider's form URL is set
 * (wp option update bhr_newsletter_action <url>); until then, a "coming soon" note.
 */
function bhr_newsletter( $compact = false ) {
	static $n = 0;
	$n++;
	$id      = 'nl-' . $n;
	$action  = get_option( 'bhr_newsletter_action' ) ?: admin_url( 'admin-post.php' );
	$own     = ! get_option( 'bhr_newsletter_action' );
	$status  = isset( $_GET['newsletter'] ) ? sanitize_key( wp_unslash( $_GET['newsletter'] ) ) : '';
	$message = array(
		'ok'      => 'Thank you! You are on the list for our newsletter.',
		'invalid' => 'Please enter a valid email address.',
		'consent' => 'Please tick the box to agree to receive the newsletter.',
		'limit'   => 'Too many sign-ups from your connection. Please try again later.',
	);
	echo '<aside class="newsletter' . ( $compact ? ' newsletter--compact' : '' ) . '" id="' . ( 1 === $n ? 'newsletter' : esc_attr( $id ) ) . '" aria-labelledby="' . esc_attr( $id ) . '-title">';
	echo '<h2 id="' . esc_attr( $id ) . '-title" class="newsletter-title">One story from Black history, in your inbox</h2>';
	echo '<p>Carefully researched stories, sent now and then. Free, and you can unsubscribe at any time.</p>';
	if ( $status && isset( $message[ $status ] ) ) {
		echo '<p class="newsletter-msg" role="status">' . esc_html( $message[ $status ] ) . '</p>';
	}
	if ( 'ok' !== $status ) {
		echo '<form class="newsletter-form" method="post" action="' . esc_url( $action ) . '">';
		if ( $own ) {
			echo '<input type="hidden" name="action" value="bhr_subscribe">';
			echo '<input class="hp-field" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">';
		}
		echo '<label class="screen-reader-text" for="' . esc_attr( $id ) . '-email">Email address</label>';
		echo '<input id="' . esc_attr( $id ) . '-email" type="email" name="email" required placeholder="Your email address" autocomplete="email">';
		echo '<button class="btn btn--primary" type="submit">Subscribe</button>';
		if ( $own ) {
			echo '<label class="newsletter-consent"><input type="checkbox" name="consent" value="1" required> I agree to receive the newsletter from The Black History Room. See our <a href="' . esc_url( home_url( '/privacy-policy/' ) ) . '">Privacy Policy</a>.</label>';
		}
		echo '</form>';
	}
	echo '</aside>';
}

function bhr_posted_meta() {
	$published = get_the_date( 'c' );
	$modified  = get_the_modified_date( 'c' );
	echo '<p class="article-meta">';
	if ( get_the_author() ) {
		echo '<span class="byline">By ' . esc_html( get_the_author() ) . '</span>';
	}
	echo '<span><time datetime="' . esc_attr( $published ) . '">' . esc_html( get_the_date() ) . '</time></span>';
	if ( strtotime( $modified ) - strtotime( $published ) > DAY_IN_SECONDS ) {
		echo '<span>Updated <time datetime="' . esc_attr( $modified ) . '">' . esc_html( get_the_modified_date() ) . '</time></span>';
	}
	echo '<span>' . esc_html( bhr_reading_time() ) . ' min read</span>';
	echo '</p>';
}

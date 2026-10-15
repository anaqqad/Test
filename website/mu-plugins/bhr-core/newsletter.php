<?php
/**
 * Newsletter sign-ups stored on our own site (free, no third party). Each subscriber is a private
 * "bhr_subscriber" post: title = email, meta = consent date and consent text version. No IP address is stored.
 * Export: Subscribers → "Export CSV" (admins only), to import into a mail service later (e.g. MailerLite / Brevo).
 * Spam protection: honeypot field, valid email, consent required, max 5 sign-ups per IP per hour (hashed, temporary).
 */

defined( 'ABSPATH' ) || exit;

const BHR_CONSENT_VERSION = '2026-10-15';

add_action( 'init', function () {
	register_post_type( 'bhr_subscriber', array(
		'labels'              => array( 'name' => 'Subscribers', 'singular_name' => 'Subscriber', 'menu_name' => 'Newsletter' ),
		'public'              => false,
		'show_ui'             => true,
		'show_in_menu'        => true,
		'show_in_rest'        => false,
		'menu_icon'           => 'dashicons-email-alt',
		'menu_position'       => 25,
		'supports'            => array( 'title' ),
		'capability_type'     => 'post',
		'capabilities'        => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'        => true,
		'exclude_from_search' => true,
	) );
} );

function bhr_subscribe_redirect( $status ) {
	$back = wp_get_referer() ?: home_url( '/' );
	wp_safe_redirect( add_query_arg( 'newsletter', $status, remove_query_arg( 'newsletter', $back ) ) . '#newsletter' );
	exit;
}

function bhr_handle_subscribe() {
	// Honeypot: real people leave this hidden field empty.
	if ( ! empty( $_POST['website'] ) ) {
		bhr_subscribe_redirect( 'ok' );
	}
	$email = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
	if ( ! is_email( $email ) ) {
		bhr_subscribe_redirect( 'invalid' );
	}
	if ( empty( $_POST['consent'] ) ) {
		bhr_subscribe_redirect( 'consent' );
	}
	$key   = 'bhr_nl_' . substr( hash( 'sha256', ( $_SERVER['REMOTE_ADDR'] ?? '' ) . wp_salt() ), 0, 20 );
	$count = (int) get_transient( $key );
	if ( $count >= 5 ) {
		bhr_subscribe_redirect( 'limit' );
	}
	set_transient( $key, $count + 1, HOUR_IN_SECONDS );

	$email = strtolower( $email );
	$found = get_posts( array( 'post_type' => 'bhr_subscriber', 'post_status' => 'any', 'title' => $email, 'fields' => 'ids', 'posts_per_page' => 1 ) );
	if ( ! $found ) {
		$id = wp_insert_post( array( 'post_type' => 'bhr_subscriber', 'post_status' => 'private', 'post_title' => $email ) );
		update_post_meta( $id, 'bhr_consent_at', current_time( 'mysql', true ) );
		update_post_meta( $id, 'bhr_consent_version', BHR_CONSENT_VERSION );
	}
	bhr_subscribe_redirect( 'ok' );
}
add_action( 'admin_post_nopriv_bhr_subscribe', 'bhr_handle_subscribe' );
add_action( 'admin_post_bhr_subscribe', 'bhr_handle_subscribe' );

// Admin: consent date column + CSV export.
add_filter( 'manage_bhr_subscriber_posts_columns', function ( $cols ) {
	return array( 'cb' => $cols['cb'], 'title' => 'Email', 'consent' => 'Consent (UTC)' );
} );
add_action( 'manage_bhr_subscriber_posts_custom_column', function ( $col, $id ) {
	if ( 'consent' === $col ) {
		echo esc_html( get_post_meta( $id, 'bhr_consent_at', true ) );
	}
}, 10, 2 );
add_action( 'admin_notices', function () {
	$screen = get_current_screen();
	if ( $screen && 'edit-bhr_subscriber' === $screen->id && current_user_can( 'manage_options' ) ) {
		$url = wp_nonce_url( admin_url( 'admin-post.php?action=bhr_export_subscribers' ), 'bhr_export' );
		echo '<div class="notice notice-info"><p>Sign-ups are stored here; no emails are sent from this site. <a class="button" href="' . esc_url( $url ) . '">Export CSV</a></p></div>';
	}
} );
add_action( 'admin_post_bhr_export_subscribers', function () {
	if ( ! current_user_can( 'manage_options' ) || ! check_admin_referer( 'bhr_export' ) ) {
		wp_die( 'Not allowed.' );
	}
	header( 'Content-Type: text/csv; charset=utf-8' );
	header( 'Content-Disposition: attachment; filename=bhr-subscribers-' . gmdate( 'Y-m-d' ) . '.csv' );
	$out = fopen( 'php://output', 'w' );
	fputcsv( $out, array( 'email', 'consent_at_utc', 'consent_version' ) );
	foreach ( get_posts( array( 'post_type' => 'bhr_subscriber', 'post_status' => 'any', 'posts_per_page' => -1 ) ) as $p ) {
		fputcsv( $out, array( $p->post_title, get_post_meta( $p->ID, 'bhr_consent_at', true ), get_post_meta( $p->ID, 'bhr_consent_version', true ) ) );
	}
	exit;
} );

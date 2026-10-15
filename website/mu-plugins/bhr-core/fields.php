<?php
/**
 * Story fields: stored as post meta, editable in a small "Story details" box under the editor, and readable /
 * writable through the REST API (for n8n drafts).
 *
 * bhr_sources format, one source per line:   Title | Publisher | https://url     (Publisher and URL optional)
 */

defined( 'ABSPATH' ) || exit;

const BHR_STORY_FIELDS = array(
	'bhr_full_name'    => array( 'Full name', 'text', 'e.g. Robert Smalls' ),
	'bhr_birth_year'   => array( 'Birth year', 'text', 'e.g. 1839 (use a minus sign for BCE; "c. 1280" allowed)' ),
	'bhr_death_year'   => array( 'Death year', 'text', 'Blank if living' ),
	'bhr_event_date'   => array( 'Key date (YYYY-MM-DD)', 'text', 'Feeds "This week in Black history". Optional.' ),
	'bhr_sources'      => array( 'Sources (at least two)', 'textarea', 'One per line: Title | Publisher | https://url' ),
	'bhr_image_credit' => array( 'Image credits', 'textarea', 'e.g. Library of Congress, Brady-Handy collection. Public domain, via Wikimedia Commons.' ),
	'bhr_reel_url'     => array( 'Related reel / video URL', 'url', 'Facebook, YouTube or Instagram link' ),
	'bhr_podcast_url'  => array( 'Related podcast episode URL', 'url', 'Episode page on this site or on Spotify' ),
);

add_action( 'init', function () {
	foreach ( BHR_STORY_FIELDS as $key => $def ) {
		register_post_meta( 'story', $key, array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'textarea' === $def[1] ? 'sanitize_textarea_field' : ( 'url' === $def[1] ? 'esc_url_raw' : 'sanitize_text_field' ),
			'auth_callback'     => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}
} );

// Hide these keys from the generic "Custom fields" panel; they have their own box.
add_filter( 'is_protected_meta', function ( $protected, $key ) {
	return isset( BHR_STORY_FIELDS[ $key ] ) ? true : $protected;
}, 10, 2 );

add_action( 'add_meta_boxes_story', function () {
	add_meta_box( 'bhr-story-details', 'Story details', 'bhr_story_box', 'story', 'normal', 'high' );
} );

function bhr_story_box( $post ) {
	wp_nonce_field( 'bhr_story_save', 'bhr_story_nonce' );
	echo '<p>The excerpt (about 40 words) is the summary on cards. Each important fact needs at least two reliable sources.</p>';
	echo '<table class="form-table" role="presentation">';
	foreach ( BHR_STORY_FIELDS as $key => $def ) {
		$value = get_post_meta( $post->ID, $key, true );
		echo '<tr><th scope="row"><label for="' . esc_attr( $key ) . '">' . esc_html( $def[0] ) . '</label></th><td>';
		if ( 'textarea' === $def[1] ) {
			printf( '<textarea class="large-text" rows="4" id="%1$s" name="%1$s">%2$s</textarea>', esc_attr( $key ), esc_textarea( $value ) );
		} else {
			printf( '<input class="regular-text" type="%3$s" id="%1$s" name="%1$s" value="%2$s">', esc_attr( $key ), esc_attr( $value ), 'url' === $def[1] ? 'url' : 'text' );
		}
		echo '<p class="description">' . esc_html( $def[2] ) . '</p></td></tr>';
	}
	echo '</table>';
}

add_action( 'save_post_story', function ( $post_id ) {
	if ( ! isset( $_POST['bhr_story_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['bhr_story_nonce'] ), 'bhr_story_save' ) ) {
		return;
	}
	if ( ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) || ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	foreach ( BHR_STORY_FIELDS as $key => $def ) {
		if ( isset( $_POST[ $key ] ) ) {
			// Sanitized by the callback registered with register_post_meta().
			update_post_meta( $post_id, $key, wp_unslash( $_POST[ $key ] ) ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput
		}
	}
} );

/**
 * Years label, e.g. "1839–1915", "born 1942", or "" when unknown.
 */
function bhr_story_years( $post = null ) {
	$id    = get_post( $post )->ID;
	$birth = trim( (string) get_post_meta( $id, 'bhr_birth_year', true ) );
	$death = trim( (string) get_post_meta( $id, 'bhr_death_year', true ) );
	$fmt   = function ( $y ) {
		return preg_match( '/^-\d+$/', $y ) ? ltrim( $y, '-' ) . ' BCE' : $y;
	};
	if ( $birth && $death ) {
		return $fmt( $birth ) . '–' . $fmt( $death );
	}
	if ( $birth ) {
		return 'born ' . $fmt( $birth );
	}
	return $death ? 'died ' . $fmt( $death ) : '';
}

/**
 * Sources as arrays of [title, publisher, url].
 */
function bhr_story_sources( $post = null ) {
	$raw = (string) get_post_meta( get_post( $post )->ID, 'bhr_sources', true );
	$out = array();
	foreach ( preg_split( '/\R/', $raw ) as $line ) {
		$line = trim( $line );
		if ( '' === $line ) {
			continue;
		}
		$parts = array_map( 'trim', explode( '|', $line ) );
		$url   = '';
		foreach ( $parts as $i => $part ) {
			if ( preg_match( '#^https?://#', $part ) ) {
				$url = $part;
				unset( $parts[ $i ] );
			}
		}
		$parts = array_values( $parts );
		$out[] = array( $parts[0] ?? '', $parts[1] ?? '', $url );
	}
	return $out;
}

<?php
/**
 * Applies feature-length texts to live stories: content (H2 sections + paragraphs), excerpt and sources.
 * The previous text is kept as a WordPress revision. Also deletes the older "<slug>-expanded" review drafts.
 *   BHR_JSON=<file>   one of the features JSON files; BHR_ONLY=slug1,slug2 limits it.
 *   BHR_DRY=1         report only, change nothing.
 * Run: wp eval-file - < apply_features.php
 */
$data = json_decode( (string) file_get_contents( getenv( 'BHR_JSON' ) ), true );
$only = array_filter( explode( ',', (string) getenv( 'BHR_ONLY' ) ) );
$dry  = (bool) getenv( 'BHR_DRY' );
if ( ! $data ) {
	WP_CLI::error( 'No data.' );
}
foreach ( $data['stories'] as $slug => $s ) {
	if ( $only && ! in_array( $slug, $only, true ) ) {
		continue;
	}
	$live = get_page_by_path( $slug, OBJECT, 'story' );
	if ( ! $live ) {
		WP_CLI::warning( "no live story $slug" );
		continue;
	}
	$html = '';
	foreach ( $s['sections'] as $sec ) {
		$html .= "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">" . esc_html( $sec[0] ) . "</h2>\n<!-- /wp:heading -->\n\n";
		foreach ( $sec[1] as $p ) {
			$html .= "<!-- wp:paragraph -->\n<p>" . esc_html( $p ) . "</p>\n<!-- /wp:paragraph -->\n\n";
		}
	}
	$words = str_word_count( wp_strip_all_tags( $html ) );
	if ( ! $dry ) {
		wp_update_post( array( 'ID' => $live->ID, 'post_content' => $html, 'post_excerpt' => $s['excerpt'] ) );
		update_post_meta( $live->ID, 'bhr_sources', implode( "\n", $s['sources'] ) );
		$old = get_page_by_path( $slug . '-expanded', OBJECT, 'story' );
		if ( $old && 'draft' === $old->post_status ) {
			wp_delete_post( $old->ID, true );
		}
	}
	WP_CLI::log( sprintf( '%-26s %4d words, %d sections, %d sources%s', $slug, $words, count( $s['sections'] ), count( $s['sources'] ), $dry ? ' (dry run)' : '' ) );
}
WP_CLI::success( $dry ? 'Dry run complete.' : 'Applied.' );

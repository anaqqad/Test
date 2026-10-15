<?php
/**
 * Expanded story texts, reviewed before going live.
 *   BHR_MODE=create  (default) creates one DRAFT per entry in the JSON, linked to the live story:
 *                    title "<name>", slug "<slug>-expanded", meta bhr_revision_of = live story ID; same terms,
 *                    fields and featured image; sources = live sources + extra_sources (no duplicates).
 *   BHR_MODE=apply   copies text, excerpt and sources from each "-expanded" draft into its live story (a WordPress
 *                    revision of the old text is kept), then deletes the draft. Only run after the owner approves.
 *   BHR_ONLY=slug1,slug2  limits either mode to some stories.
 * Run: wp eval-file - < story_expansions.php   with BHR_JSON=<path inside the container>
 */

$mode = getenv( 'BHR_MODE' ) ?: 'create';
$only = array_filter( explode( ',', (string) getenv( 'BHR_ONLY' ) ) );

if ( 'apply' === $mode ) {
	$drafts = get_posts( array( 'post_type' => 'story', 'post_status' => 'draft', 'meta_key' => 'bhr_revision_of', 'posts_per_page' => -1 ) );
	foreach ( $drafts as $d ) {
		$live = get_post( (int) get_post_meta( $d->ID, 'bhr_revision_of', true ) );
		if ( ! $live || ( $only && ! in_array( $live->post_name, $only, true ) ) ) {
			continue;
		}
		wp_update_post( array( 'ID' => $live->ID, 'post_content' => $d->post_content, 'post_excerpt' => $d->post_excerpt ) );
		update_post_meta( $live->ID, 'bhr_sources', get_post_meta( $d->ID, 'bhr_sources', true ) );
		wp_delete_post( $d->ID, true );
		WP_CLI::log( "applied {$live->post_name}" );
	}
	WP_CLI::success( 'Done.' );
	return;
}

$data = json_decode( (string) file_get_contents( getenv( 'BHR_JSON' ) ), true );
foreach ( $data['stories'] as $slug => $s ) {
	if ( $only && ! in_array( $slug, $only, true ) ) {
		continue;
	}
	$live = get_page_by_path( $slug, OBJECT, 'story' );
	if ( ! $live ) {
		WP_CLI::warning( "no live story $slug" );
		continue;
	}
	if ( get_page_by_path( $slug . '-expanded', OBJECT, 'story' ) ) {
		WP_CLI::log( "skip $slug (draft exists)" );
		continue;
	}
	$content = '';
	foreach ( $s['paragraphs'] as $p ) {
		$content .= "<!-- wp:paragraph -->\n<p>" . esc_html( $p ) . "</p>\n<!-- /wp:paragraph -->\n\n";
	}
	$id = wp_insert_post( array(
		'post_type'    => 'story',
		'post_status'  => 'draft',
		'post_title'   => $live->post_title,
		'post_name'    => $slug . '-expanded',
		'post_excerpt' => $live->post_excerpt,
		'post_content' => $content,
		'post_author'  => $live->post_author,
	), true );
	if ( is_wp_error( $id ) ) {
		WP_CLI::warning( $slug . ': ' . $id->get_error_message() );
		continue;
	}
	foreach ( array( 'section', 'domain', 'country', 'era', 'post_tag' ) as $tax ) {
		wp_set_object_terms( $id, wp_get_object_terms( $live->ID, $tax, array( 'fields' => 'ids' ) ), $tax );
	}
	foreach ( get_post_meta( $live->ID ) as $key => $values ) {
		if ( 0 === strpos( $key, 'bhr_' ) || '_thumbnail_id' === $key ) {
			update_post_meta( $id, $key, maybe_unserialize( $values[0] ) );
		}
	}
	$sources = array_filter( array_map( 'trim', preg_split( '/\R/', (string) get_post_meta( $live->ID, 'bhr_sources', true ) ) ) );
	foreach ( $s['extra_sources'] as $extra ) {
		if ( ! in_array( $extra, $sources, true ) ) {
			$sources[] = $extra;
		}
	}
	update_post_meta( $id, 'bhr_sources', implode( "\n", $sources ) );
	update_post_meta( $id, 'bhr_revision_of', $live->ID );
	WP_CLI::log( sprintf( '%-26s draft %d (%d words, %d sources)', $slug, $id, str_word_count( wp_strip_all_tags( $content ) ), count( $sources ) ) );
}
WP_CLI::success( 'Expanded drafts ready for review. Live stories unchanged.' );

<?php
/**
 * Lists of stories: the Stories page, categories, tags, authors, dates and search results.
 */

get_header();

if ( is_search() ) {
	/* translators: %s: search terms */
	$title = sprintf( 'Search results for “%s”', get_search_query() );
	$intro = '';
} elseif ( is_home() ) {
	$title = get_the_title( get_option( 'page_for_posts' ) ) ?: 'News';
	$intro = 'News and updates from The Black History Room.';
} else {
	$title = wp_strip_all_tags( get_the_archive_title() );
	$intro = wp_strip_all_tags( get_the_archive_description() );
}
?>
<header class="page-header">
	<div class="wrap">
		<?php if ( function_exists( 'yoast_breadcrumb' ) && ! is_home() ) : ?>
			<?php yoast_breadcrumb( '<nav class="breadcrumbs" aria-label="Breadcrumb">', '</nav>' ); ?>
		<?php endif; ?>
		<h1 class="page-title"><?php echo esc_html( $title ); ?></h1>
		<?php if ( $intro ) : ?>
			<p class="page-intro"><?php echo esc_html( $intro ); ?></p>
		<?php endif; ?>
		<?php if ( is_search() ) : ?>
			<?php get_search_form(); ?>
		<?php endif; ?>
	</div>
</header>

<div class="wrap list-wrap">
	<?php if ( have_posts() ) : ?>
		<div class="grid grid--card">
			<?php
			while ( have_posts() ) :
				the_post();
				'story' === get_post_type() ? bhr_story_card( 'h2' ) : bhr_card( 'card', 'h2' );
			endwhile;
			?>
		</div>
		<?php
		the_posts_pagination( array(
			'mid_size'  => 1,
			'prev_text' => 'Newer',
			'next_text' => 'Older',
		) );
		?>
	<?php else : ?>
		<p class="empty-note">
			<?php echo is_search() ? 'No stories match your search. Try other words.' : 'No stories here yet. New stories are on the way.'; ?>
		</p>
	<?php endif; ?>
</div>
<?php
get_footer();

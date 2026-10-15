<?php
/**
 * Story lists: all stories (/stories/) and Country, Domain, Era and Section archives.
 */

get_header();

$term  = is_tax() ? get_queried_object() : null;
$title = $term ? $term->name : 'All stories';
$intro = $term ? term_description( $term ) : 'Every story in The Black History Room, newest first.';
?>
<header class="page-header">
	<div class="wrap">
		<nav class="breadcrumbs" aria-label="Breadcrumb">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
			<?php if ( $term && 'country' === $term->taxonomy ) : ?>
				› <a href="<?php echo esc_url( home_url( '/global-african-history/' ) ); ?>">Global African History</a>
			<?php endif; ?>
		</nav>
		<?php if ( $term && 'country' === $term->taxonomy ) : ?>
			<p class="kicker kicker--static">Country</p>
		<?php endif; ?>
		<h1 class="page-title"><?php echo esc_html( $title ); ?></h1>
		<?php if ( $intro ) : ?>
			<div class="page-intro"><?php echo wp_kses_post( wpautop( $intro ) ); ?></div>
		<?php endif; ?>
	</div>
</header>
<div class="wrap list-wrap">
	<?php if ( have_posts() ) : ?>
		<?php bhr_story_grid( $GLOBALS['wp_query'], 'h2' ); ?>
		<?php the_posts_pagination( array( 'mid_size' => 1, 'prev_text' => 'Newer', 'next_text' => 'Older' ) ); ?>
	<?php else : ?>
		<p class="empty-note">No stories here yet. New stories are on the way.</p>
	<?php endif; ?>
</div>
<?php
get_footer();

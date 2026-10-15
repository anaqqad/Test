<?php
/**
 * This week in Black history: stories whose key date falls in the next 7 days (any year).
 */

get_header();
$query = bhr_this_week_query( 24 );
?>
<header class="page-header">
	<div class="wrap">
		<h1 class="page-title"><?php the_title(); ?></h1>
		<p class="page-intro">Events that happened on these dates, in years past.</p>
	</div>
</header>
<div class="wrap list-wrap">
	<?php if ( $query->have_posts() ) : ?>
		<?php bhr_story_grid( $query, 'h2' ); ?>
	<?php else : ?>
		<p class="empty-note">No stories for this week yet.</p>
	<?php endif; ?>
</div>
<?php
get_footer();

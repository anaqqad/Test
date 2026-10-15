<?php
/**
 * Reels & videos: every published story that has a reel/video link.
 */

get_header();
$query = new WP_Query( array(
	'post_type'      => 'story',
	'posts_per_page' => 24,
	'meta_query'     => array( array( 'key' => 'bhr_reel_url', 'value' => '', 'compare' => '!=' ) ),
) );
?>
<header class="page-header">
	<div class="wrap">
		<h1 class="page-title"><?php the_title(); ?></h1>
		<p class="page-intro">Short videos from The Black History Room. Each one has a full written story with sources.</p>
	</div>
</header>
<div class="wrap list-wrap">
	<?php if ( $query->have_posts() ) : ?>
		<?php bhr_story_grid( $query, 'h2' ); ?>
	<?php else : ?>
		<p class="empty-note">Videos will be listed here as their stories are published.</p>
	<?php endif; ?>
</div>
<?php
get_footer();

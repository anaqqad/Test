<?php
/**
 * Not found.
 */

get_header();
?>
<header class="page-header">
	<div class="wrap">
		<p class="kicker">Error 404</p>
		<h1 class="page-title">This page is not in the archive</h1>
		<p class="page-intro">The link may be old or mistyped. Try a search, or start with our latest stories.</p>
		<?php get_search_form(); ?>
	</div>
</header>
<?php
bhr_section( 'Latest stories', new WP_Query( array( 'posts_per_page' => 3, 'no_found_rows' => true, 'ignore_sticky_posts' => true ) ), '', 'card' );
get_footer();

<?php
/**
 * Plain page (About, policies, contact).
 */

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<article <?php post_class( 'article article--page' ); ?>>
		<header class="article-header wrap wrap--text">
			<h1 class="article-title"><?php the_title(); ?></h1>
		</header>
		<div class="article-body wrap wrap--text entry-content">
			<?php the_content(); ?>
		</div>
	</article>
	<?php
endwhile;

get_footer();

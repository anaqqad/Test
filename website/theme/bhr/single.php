<?php
/**
 * Article.
 */

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<article <?php post_class( 'article' ); ?>>
		<header class="article-header wrap wrap--text">
			<?php if ( function_exists( 'yoast_breadcrumb' ) ) : ?>
				<?php yoast_breadcrumb( '<nav class="breadcrumbs" aria-label="Breadcrumb">', '</nav>' ); ?>
			<?php endif; ?>
			<?php bhr_kicker(); ?>
			<h1 class="article-title"><?php the_title(); ?></h1>
			<?php if ( has_excerpt() ) : ?>
				<p class="article-deck"><?php echo esc_html( get_the_excerpt() ); ?></p>
			<?php endif; ?>
			<?php bhr_posted_meta(); ?>
		</header>

		<?php if ( has_post_thumbnail() ) : ?>
			<figure class="article-figure wrap wrap--wide">
				<?php the_post_thumbnail( 'bhr-hero', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'sizes' => '(min-width: 75em) 1200px, 100vw' ) ); ?>
				<?php $caption = wp_get_attachment_caption( get_post_thumbnail_id() ); ?>
				<?php if ( $caption ) : ?>
					<figcaption><?php echo wp_kses_post( $caption ); ?></figcaption>
				<?php endif; ?>
			</figure>
		<?php endif; ?>

		<div class="article-body wrap wrap--text entry-content">
			<?php the_content(); ?>
		</div>

		<footer class="article-footer wrap wrap--text">
			<?php $sources = bhr_sources(); ?>
			<?php if ( $sources ) : ?>
				<section class="sources" aria-labelledby="sources-title">
					<h2 id="sources-title">Sources</h2>
					<ol>
						<?php foreach ( $sources as $source ) : ?>
							<li>
								<?php if ( $source[1] ) : ?>
									<a href="<?php echo esc_url( $source[1] ); ?>" rel="noopener"><?php echo esc_html( $source[0] ); ?></a>
								<?php else : ?>
									<?php echo esc_html( $source[0] ); ?>
								<?php endif; ?>
							</li>
						<?php endforeach; ?>
					</ol>
				</section>
			<?php endif; ?>

			<?php bhr_share_links(); ?>
			<?php bhr_newsletter( true ); ?>

			<?php
			the_post_navigation( array(
				'prev_text' => '<span class="nav-label">Previous story</span><span class="nav-title">%title</span>',
				'next_text' => '<span class="nav-label">Next story</span><span class="nav-title">%title</span>',
			) );
			?>
		</footer>
	</article>

	<?php
	$related = bhr_related_query();
	if ( $related && $related->have_posts() ) :
		?>
		<section class="home-section related" aria-labelledby="related-title">
			<div class="wrap">
				<h2 id="related-title" class="section-title">Related stories</h2>
				<div class="grid grid--card">
					<?php
					while ( $related->have_posts() ) :
						$related->the_post();
						bhr_card( 'card' );
					endwhile;
					wp_reset_postdata();
					?>
				</div>
			</div>
		</section>
		<?php
	endif;
endwhile;

get_footer();

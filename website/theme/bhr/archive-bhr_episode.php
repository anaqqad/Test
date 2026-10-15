<?php
/**
 * Podcast page: /podcast/
 */

get_header();
?>
<header class="page-header page-header--podcast">
	<div class="wrap">
		<p class="kicker kicker--gold">The podcast</p>
		<h1 class="page-title"><?php echo esc_html( BHR_PODCAST_NAME ); ?></h1>
		<p class="page-intro">One story from Black history, told in about ten minutes. Researched with the same sourcing rules as our articles.</p>
		<p><a class="button button--gold" href="<?php echo esc_url( BHR_PODCAST_SPOTIFY ); ?>" rel="noopener">Listen on Spotify</a></p>
	</div>
</header>

<div class="wrap list-wrap">
	<?php if ( have_posts() ) : ?>
		<ol class="episodes">
			<?php
			while ( have_posts() ) :
				the_post();
				$number = (int) get_post_meta( get_the_ID(), 'bhr_episode_number', true );
				?>
				<li class="episode">
					<?php if ( has_post_thumbnail() ) : ?>
						<a class="episode-cover" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true"><?php the_post_thumbnail( 'thumbnail' ); ?></a>
					<?php endif; ?>
					<div>
						<?php if ( $number ) : ?>
							<p class="kicker">Episode <?php echo esc_html( $number ); ?></p>
						<?php endif; ?>
						<h2 class="story-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
						<?php if ( has_excerpt() ) : ?>
							<p class="story-excerpt"><?php echo esc_html( get_the_excerpt() ); ?></p>
						<?php endif; ?>
					</div>
				</li>
			<?php endwhile; ?>
		</ol>
		<?php the_posts_pagination(); ?>
	<?php else : ?>
		<p class="empty-note">Episodes will be listed here. Meanwhile, every episode is on Spotify.</p>
	<?php endif; ?>
</div>
<?php
get_footer();

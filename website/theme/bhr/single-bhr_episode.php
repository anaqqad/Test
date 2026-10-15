<?php
/**
 * One podcast episode: description, listen links, related articles, transcript.
 */

get_header();

while ( have_posts() ) :
	the_post();
	$number  = (int) get_post_meta( get_the_ID(), 'bhr_episode_number', true );
	$links   = bhr_episode_links();
	$related = bhr_episode_related();
	?>
	<article <?php post_class( 'article' ); ?>>
		<header class="article-header wrap wrap--text">
			<p class="kicker kicker--plain">
				<a href="<?php echo esc_url( get_post_type_archive_link( 'bhr_episode' ) ); ?>"><?php echo esc_html( BHR_PODCAST_NAME ); ?></a>
				<?php echo $number ? ' · Episode ' . esc_html( $number ) : ''; ?>
			</p>
			<h1 class="article-title"><?php the_title(); ?></h1>
			<?php if ( has_excerpt() ) : ?>
				<p class="article-deck"><?php echo esc_html( get_the_excerpt() ); ?></p>
			<?php endif; ?>
			<?php if ( $links ) : ?>
				<p class="listen">
					<?php foreach ( $links as $name => $url ) : ?>
						<a class="button" href="<?php echo esc_url( $url ); ?>" rel="noopener">Listen on <?php echo esc_html( $name ); ?></a>
					<?php endforeach; ?>
				</p>
			<?php endif; ?>
		</header>

		<?php if ( has_post_thumbnail() ) : ?>
			<figure class="article-figure wrap wrap--text"><?php the_post_thumbnail( 'large' ); ?></figure>
		<?php endif; ?>

		<?php
		$chapters = array_filter( array_map( 'trim', preg_split( '/\R/', (string) get_post_meta( get_the_ID(), 'bhr_chapters', true ) ) ) );
		if ( $chapters ) :
			?>
			<section class="wrap wrap--text" aria-labelledby="chapters-title">
				<h2 id="chapters-title" class="end-title">Chapters</h2>
				<ol class="chapters">
					<?php foreach ( $chapters as $line ) : ?>
						<?php if ( preg_match( '/^(\d+:\d\d)\s+(.+)$/', $line, $m ) ) : ?>
							<li><time><?php echo esc_html( $m[1] ); ?></time> <?php echo esc_html( $m[2] ); ?></li>
						<?php endif; ?>
					<?php endforeach; ?>
				</ol>
			</section>
		<?php endif; ?>

		<?php if ( $related ) : ?>
			<section class="wrap wrap--text episode-related">
				<h2>Read the stories</h2>
				<ul>
					<?php foreach ( $related as $item ) : ?>
						<li><a href="<?php echo esc_url( get_permalink( $item ) ); ?>"><?php echo esc_html( get_the_title( $item ) ); ?></a></li>
					<?php endforeach; ?>
				</ul>
			</section>
		<?php endif; ?>

		<?php if ( get_the_content() ) : ?>
			<details class="wrap wrap--text transcript">
				<summary>Read the transcript</summary>
				<div class="entry-content"><?php the_content(); ?></div>
			</details>
		<?php endif; ?>
	</article>
	<?php
endwhile;

get_footer();

<?php
/**
 * Homepage: hero, latest, untold stories, people, this week, Africa, African-American history, podcast, newsletter.
 * Sections with no stories are not shown.
 */

get_header();

// Hero: newest sticky post, else newest post.
$sticky = get_option( 'sticky_posts' );
$hero   = new WP_Query( $sticky
	? array( 'post__in' => $sticky, 'posts_per_page' => 1, 'ignore_sticky_posts' => true, 'no_found_rows' => true )
	: array( 'posts_per_page' => 1, 'no_found_rows' => true ) );
$hero_id = $hero->have_posts() ? $hero->posts[0]->ID : 0;

if ( $hero->have_posts() ) :
	$hero->the_post();
	?>
	<section class="hero">
		<div class="wrap hero-grid">
			<?php if ( has_post_thumbnail() ) : ?>
				<a class="hero-media" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true">
					<?php the_post_thumbnail( 'bhr-hero', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'sizes' => '(min-width: 64em) 760px, 100vw' ) ); ?>
				</a>
			<?php endif; ?>
			<div class="hero-body">
				<?php bhr_kicker(); ?>
				<h2 class="hero-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
				<?php if ( has_excerpt() ) : ?>
					<p class="hero-excerpt"><?php echo esc_html( get_the_excerpt() ); ?></p>
				<?php endif; ?>
				<a class="button" href="<?php the_permalink(); ?>">Read the story</a>
			</div>
		</div>
	</section>
	<?php
	wp_reset_postdata();
else :
	?>
	<section class="hero hero--empty">
		<div class="wrap">
			<p class="kicker">Coming soon</p>
			<h2 class="hero-title">Powerful people, moments, struggles and achievements from Black history.</h2>
			<p class="hero-excerpt">Carefully researched stories, every fact checked against at least two reliable sources.</p>
		</div>
	</section>
	<?php
endif;
?>
<h1 class="screen-reader-text"><?php bloginfo( 'name' ); ?></h1>
<?php

$exclude = $hero_id ? array( $hero_id ) : array();
$base    = array( 'post__not_in' => $exclude, 'ignore_sticky_posts' => true, 'no_found_rows' => true );
$stories = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : '';

bhr_section( 'Latest stories', new WP_Query( $base + array( 'posts_per_page' => 6 ) ), $stories, 'card', 'section--latest' );

bhr_section( 'Untold stories', new WP_Query( $base + array( 'posts_per_page' => 3, 'category_name' => 'forgotten-history' ) ),
	bhr_category_url( 'forgotten-history' ), 'card', 'section--dark', 'The people and events most history books left out.' );

bhr_section( 'People who changed history', new WP_Query( $base + array( 'posts_per_page' => 4, 'category_name' => 'historical-figures' ) ),
	bhr_category_url( 'historical-figures' ), 'card', 'section--people', '', 'bhr-portrait' );

bhr_section( 'This week in Black history', bhr_this_week_query( 4 ), '', 'row', 'section--week',
	'Events that happened on these dates, in years past.' );

bhr_section( 'Africa', new WP_Query( $base + array( 'posts_per_page' => 3, 'category_name' => 'african-history' ) ),
	bhr_category_url( 'african-history' ), 'card' );

bhr_section( 'African-American history', new WP_Query( $base + array( 'posts_per_page' => 3, 'category_name' => 'african-american-history' ) ),
	bhr_category_url( 'african-american-history' ), 'card' );

// Podcast
$episode = new WP_Query( array( 'post_type' => 'bhr_episode', 'posts_per_page' => 1, 'no_found_rows' => true ) );
?>
<section class="home-section section--podcast">
	<div class="wrap podcast-promo">
		<div>
			<p class="kicker kicker--gold">The podcast</p>
			<h2 class="section-title"><?php echo esc_html( BHR_PODCAST_NAME ); ?></h2>
			<p>One story from Black history, told in about ten minutes.</p>
			<?php if ( $episode->have_posts() ) : $episode->the_post(); ?>
				<p class="podcast-latest">Latest episode: <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></p>
				<?php wp_reset_postdata(); ?>
			<?php endif; ?>
		</div>
		<p class="podcast-actions">
			<a class="button button--gold" href="<?php echo esc_url( BHR_PODCAST_SPOTIFY ); ?>" rel="noopener">Listen on Spotify</a>
			<a class="button button--ghost" href="<?php echo esc_url( get_post_type_archive_link( 'bhr_episode' ) ); ?>">All episodes</a>
		</p>
	</div>
</section>

<div class="wrap home-newsletter"><?php bhr_newsletter(); ?></div>

<?php
get_footer();

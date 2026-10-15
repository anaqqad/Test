<?php
/**
 * Homepage: featured story, latest stories, the two sections, untold stories, this week, map teaser,
 * podcast, newsletter. Empty sections are skipped.
 */

get_header();

$sticky = array_filter( (array) get_option( 'sticky_posts' ) );
$hero   = new WP_Query( array( 'post_type' => 'story', 'posts_per_page' => 1, 'no_found_rows' => true ) + ( $sticky ? array( 'post__in' => $sticky ) : array() ) );
if ( ! $hero->have_posts() && $sticky ) {
	$hero = new WP_Query( array( 'post_type' => 'story', 'posts_per_page' => 1, 'no_found_rows' => true ) );
}
$hero_id = $hero->have_posts() ? $hero->posts[0]->ID : 0;
?>
<h1 class="screen-reader-text"><?php bloginfo( 'name' ); ?></h1>
<?php if ( $hero->have_posts() ) : $hero->the_post(); ?>
	<section class="hero">
		<div class="wrap hero-grid">
			<?php if ( has_post_thumbnail() ) : ?>
				<a class="hero-media" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true">
					<?php the_post_thumbnail( 'bhr-hero', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'sizes' => '(min-width: 64em) 760px, 100vw' ) ); ?>
				</a>
			<?php endif; ?>
			<div class="hero-body">
				<p class="kicker kicker--static">Featured story</p>
				<h2 class="hero-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
				<?php $years = bhr_story_years(); ?>
				<?php if ( $years ) : ?><p class="hero-years"><?php echo esc_html( $years ); ?></p><?php endif; ?>
				<?php if ( has_excerpt() ) : ?><p class="hero-excerpt"><?php echo esc_html( get_the_excerpt() ); ?></p><?php endif; ?>
				<a class="button" href="<?php the_permalink(); ?>">Read the story</a>
			</div>
		</div>
	</section>
	<?php wp_reset_postdata(); ?>
<?php else : ?>
	<section class="hero hero--empty">
		<div class="wrap">
			<p class="kicker kicker--static">Coming soon</p>
			<h2 class="hero-title">Powerful people, moments, struggles and achievements from Black history.</h2>
			<p class="hero-excerpt">Carefully researched stories, every fact checked against at least two reliable sources.</p>
		</div>
	</section>
<?php endif; ?>

<?php
$base = array( 'post_type' => 'story', 'post__not_in' => $hero_id ? array( $hero_id ) : array(), 'ignore_sticky_posts' => true, 'no_found_rows' => true );

function bhr_home_block( $title, WP_Query $q, $link = '', $class = '', $intro = '' ) {
	if ( ! $q->have_posts() ) {
		return;
	}
	echo '<section class="home-section ' . esc_attr( $class ) . '"><div class="wrap"><header class="section-head"><h2 class="section-title">' . esc_html( $title ) . '</h2>';
	if ( $link ) {
		echo '<a class="section-more" href="' . esc_url( $link ) . '">See all</a>';
	}
	echo '</header>';
	if ( $intro ) {
		echo '<p class="section-intro">' . esc_html( $intro ) . '</p>';
	}
	bhr_story_grid( $q );
	echo '</div></section>';
}

$section = function ( $slug ) {
	return array( array( 'taxonomy' => 'section', 'field' => 'slug', 'terms' => $slug ) );
};

bhr_home_block( 'Latest stories', new WP_Query( $base + array( 'posts_per_page' => 6 ) ), get_post_type_archive_link( 'story' ) );
bhr_home_block( 'African American History', new WP_Query( $base + array( 'posts_per_page' => 3, 'tax_query' => $section( 'african-american-history' ) ) ), home_url( '/african-american-history/' ) );
?>

<section class="home-section section--dark section--map-teaser">
	<div class="wrap map-teaser">
		<div>
			<p class="kicker kicker--gold">Global African History</p>
			<h2 class="section-title">Explore the map</h2>
			<p>Stories from Africa and the African diaspora, country by country.</p>
			<p><a class="button button--gold" href="<?php echo esc_url( home_url( '/global-african-history/' ) ); ?>">Open the world map</a></p>
		</div>
		<?php
		$counts = bhr_country_counts();
		if ( $counts ) :
			?>
			<ul class="teaser-countries">
				<?php foreach ( array_slice( $counts, 0, 12 ) as $c ) : ?>
					<li><a href="<?php echo esc_url( $c[2] ); ?>"><?php echo esc_html( $c[0] ); ?></a></li>
				<?php endforeach; ?>
			</ul>
		<?php endif; ?>
	</div>
</section>

<?php
bhr_home_block( 'Global African History', new WP_Query( $base + array( 'posts_per_page' => 3, 'tax_query' => $section( 'global-african-history' ) ) ), home_url( '/global-african-history/' ) );
bhr_home_block( 'Untold stories', new WP_Query( $base + array( 'posts_per_page' => 3, 'tag' => 'untold-stories' ) ), home_url( '/tag/untold-stories/' ), 'section--week', 'The people and events most history books left out.' );
bhr_home_block( 'This week in Black history', bhr_this_week_query( 3 ), home_url( '/this-week/' ), '', 'Events that happened on these dates, in years past.' );

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

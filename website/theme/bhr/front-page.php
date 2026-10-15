<?php
/**
 * Homepage. Order: featured story (dark), then light sections alternating cream / white:
 * latest stories, people who changed history, map teaser, Africa, African American history, untold stories,
 * this week, podcast, who we are, newsletter. A section with no stories is not shown.
 */

get_header();

$GLOBALS['bhr_shown'] = array();
$hero  = new WP_Query( array( 'post_type' => 'story', 'posts_per_page' => 1, 'no_found_rows' => true ) );
?>
<h1 class="screen-reader-text"><?php bloginfo( 'name' ); ?></h1>
<?php if ( $hero->have_posts() ) : $hero->the_post(); $GLOBALS['bhr_shown'][] = get_the_ID(); ?>
	<section class="hero">
		<div class="wrap hero-grid">
			<a class="hero-media" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true">
				<?php the_post_thumbnail( 'bhr-hero43', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'sizes' => '(min-width: 1440px) 820px, (min-width: 1024px) 58vw, 92vw' ) ); ?>
			</a>
			<div class="hero-body">
				<?php $domain = bhr_story_term( get_post(), 'domain' ); ?>
				<p class="kicker kicker--gold kicker--static"><?php echo esc_html( $domain ? $domain->name : 'Featured story' ); ?></p>
				<h2 class="hero-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
				<?php $years = bhr_story_years(); ?>
				<?php if ( $years ) : ?><p class="hero-years"><?php echo esc_html( $years ); ?></p><?php endif; ?>
				<?php if ( has_excerpt() ) : ?><p class="hero-excerpt"><?php echo esc_html( get_the_excerpt() ); ?></p><?php endif; ?>
				<a class="btn btn--primary btn--lg" href="<?php the_permalink(); ?>">Read the story</a>
			</div>
		</div>
	</section>
	<?php wp_reset_postdata(); ?>
<?php else : ?>
	<section class="hero hero--empty">
		<div class="wrap">
			<p class="kicker kicker--gold kicker--static">Coming soon</p>
			<h2 class="hero-title">Powerful people, moments, struggles and achievements from Black history.</h2>
			<p class="hero-excerpt">Carefully researched stories, every fact checked against at least two reliable sources.</p>
		</div>
	</section>
<?php endif; ?>

<?php
/**
 * One story row. Skips stories already shown higher up; prints nothing when empty. Backgrounds alternate.
 */
function bhr_home_block( $title, array $args, $link = '', $intro = '', $count = 3, $exclude_shown = true ) {
	$shown = &$GLOBALS['bhr_shown'];
	static $n = 0;
	$q = new WP_Query( $args + array(
		'post_type'      => 'story',
		'posts_per_page' => $count,
		'post__not_in'   => $exclude_shown ? $shown : array(),
		'no_found_rows'  => true,
	) );
	if ( ! $q->have_posts() ) {
		return;
	}
	$bg = ( $n++ % 2 ) ? 'bg-white' : 'bg-cream';
	echo '<section class="home-section ' . esc_attr( $bg ) . '"><div class="wrap"><header class="section-head"><div><h2 class="section-title">' . esc_html( $title ) . '</h2>';
	if ( $intro ) {
		echo '<p class="section-intro">' . esc_html( $intro ) . '</p>';
	}
	echo '</div>';
	if ( $link ) {
		echo '<a class="btn btn--outline" href="' . esc_url( $link ) . '">See all</a>';
	}
	echo '</header>';
	$shown = array_merge( $shown, wp_list_pluck( $q->posts, 'ID' ) );
	bhr_story_grid( $q );
	echo '</div></section>';
}

$section = function ( $slug ) {
	return array( 'tax_query' => array( array( 'taxonomy' => 'section', 'field' => 'slug', 'terms' => $slug ) ) );
};

bhr_home_block( 'Latest stories', array(), get_post_type_archive_link( 'story' ), '', 6 );
bhr_home_block( 'People who changed history', array( 'meta_key' => 'bhr_birth_year', 'meta_compare' => '!=', 'meta_value' => '', 'orderby' => 'title', 'order' => 'ASC' ), home_url( '/stories/' ), 'Leaders, inventors, athletes and artists whose lives changed the story of a nation.' );
?>

<section class="home-section bg-dark map-teaser-section">
	<div class="wrap map-teaser">
		<div class="map-teaser-text">
			<p class="kicker kicker--gold kicker--static">Global African History</p>
			<h2 class="section-title">Explore the map</h2>
			<p>Stories from Africa and the African diaspora, country by country.</p>
			<p><a class="btn btn--primary" href="<?php echo esc_url( home_url( '/global-african-history/' ) ); ?>">Open the world map</a></p>
		</div>
		<a class="map-teaser-image" href="<?php echo esc_url( home_url( '/global-african-history/' ) ); ?>" aria-label="Open the world map">
			<img src="<?php echo esc_url( bhr_map_preview_url() ); ?>" width="960" height="500" alt="World map: countries with stories are highlighted in red" loading="lazy" decoding="async">
		</a>
	</div>
</section>

<?php
bhr_home_block( 'Africa', $section( 'global-african-history' ), home_url( '/global-african-history/' ), 'Kingdoms, empires and people from the African continent and its diaspora.', 3, false );
bhr_home_block( 'African American History', $section( 'african-american-history' ), home_url( '/african-american-history/' ) );
bhr_home_block( 'Untold stories', array( 'tag' => 'untold-stories' ), home_url( '/tag/untold-stories/' ), 'The people and events most history books left out.' );

$week = bhr_this_week_query( 3 );
if ( $week->have_posts() ) :
	?>
	<section class="home-section bg-cream">
		<div class="wrap">
			<header class="section-head"><div><h2 class="section-title">This week in Black history</h2><p class="section-intro">Events that happened on these dates, in years past.</p></div><a class="btn btn--outline" href="<?php echo esc_url( home_url( '/this-week/' ) ); ?>">See all</a></header>
			<?php bhr_story_grid( $week ); ?>
		</div>
	</section>
	<?php
endif;

$episode = new WP_Query( array( 'post_type' => 'bhr_episode', 'posts_per_page' => 1, 'no_found_rows' => true ) );
?>
<section class="home-section bg-white">
	<div class="wrap">
		<div class="podcast-promo">
			<div>
				<p class="kicker kicker--static">The podcast</p>
				<h2 class="section-title"><?php echo esc_html( BHR_PODCAST_NAME ); ?></h2>
				<p class="lead">One story from Black history, told in about ten minutes.</p>
				<?php if ( $episode->have_posts() ) : $episode->the_post(); ?>
					<p class="podcast-latest">Latest episode: <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></p>
					<?php wp_reset_postdata(); ?>
				<?php endif; ?>
			</div>
			<p class="podcast-actions">
				<a class="btn btn--primary" href="<?php echo esc_url( BHR_PODCAST_SPOTIFY ); ?>" rel="noopener">Listen on Spotify</a>
				<a class="btn btn--outline" href="<?php echo esc_url( get_post_type_archive_link( 'bhr_episode' ) ); ?>">All episodes</a>
			</p>
		</div>
	</div>
</section>

<?php
// Who we are: archival photo (public domain) + mission text.
$who_img = 0;
$who     = get_page_by_path( 'harriet-tubman', OBJECT, 'story' );
if ( $who ) {
	$who_img = (int) get_post_thumbnail_id( $who );
}
?>
<section class="home-section bg-cream">
	<div class="wrap">
		<div class="who">
			<?php if ( $who_img ) : ?>
				<figure class="who-media">
					<?php echo wp_get_attachment_image( $who_img, 'bhr-hero43', false, array( 'loading' => 'lazy', 'sizes' => '(min-width: 1024px) 640px, 92vw', 'alt' => 'Harriet Tubman, portrait by Horatio Seymour Squyer' ) ); ?>
					<figcaption>Harriet Tubman, photographed by H. S. Squyer. Public domain.</figcaption>
				</figure>
			<?php endif; ?>
			<div class="who-body">
				<h2 class="section-title">Who we are</h2>
				<p class="who-sub">Our mission</p>
				<p>The Black History Room shares powerful people, moments, struggles and achievements from Black history: from African kingdoms to the civil rights movement, from inventors and explorers to the stories most history books left out.</p>
				<p>Every story is researched from archives, museums, universities and published scholarship, and every important fact is checked against at least two reliable sources.</p>
				<p class="who-actions">
					<a class="btn btn--primary" href="<?php echo esc_url( home_url( '/about/#mission' ) ); ?>">Our Mission</a>
					<a class="btn btn--outline" href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About Us</a>
				</p>
			</div>
		</div>
	</div>
</section>

<section class="home-section bg-white">
	<div class="wrap"><?php bhr_newsletter(); ?></div>
</section>

<?php
get_footer();

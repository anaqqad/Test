<?php
/**
 * One Story. Ends with: Cite this entry, Sources, Discover more, Support our work.
 */

get_header();

while ( have_posts() ) :
	the_post();
	$section = bhr_story_term( get_post(), 'section' );
	$domain  = bhr_story_term( get_post(), 'domain' );
	$country = bhr_story_term( get_post(), 'country' );
	$years   = function_exists( 'bhr_story_years' ) ? bhr_story_years() : '';
	?>
	<article <?php post_class( 'article story-entry' ); ?>>
		<header class="article-header wrap wrap--text">
			<nav class="breadcrumbs" aria-label="Breadcrumb">
				<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
				<?php if ( $section ) : ?>
					› <a href="<?php echo esc_url( home_url( '/' . $section->slug . '/' ) ); ?>"><?php echo esc_html( $section->name ); ?></a>
				<?php endif; ?>
				<?php if ( $country && $section && 'global-african-history' === $section->slug ) : ?>
					› <a href="<?php echo esc_url( get_term_link( $country ) ); ?>"><?php echo esc_html( $country->name ); ?></a>
				<?php elseif ( $domain && $section && 'african-american-history' === $section->slug ) : ?>
					› <a href="<?php echo esc_url( home_url( '/african-american-history/' . $domain->slug . '/' ) ); ?>"><?php echo esc_html( $domain->name ); ?></a>
				<?php endif; ?>
			</nav>
			<?php if ( $domain ) : ?>
				<p class="kicker kicker--static"><?php echo esc_html( $domain->name ); ?><?php echo $country ? ' · ' . esc_html( $country->name ) : ''; ?></p>
			<?php endif; ?>
			<h1 class="article-title"><?php the_title(); ?><?php if ( $years ) : ?> <span class="title-years">(<?php echo esc_html( $years ); ?>)</span><?php endif; ?></h1>
			<?php if ( has_excerpt() ) : ?>
				<p class="article-deck"><?php echo esc_html( get_the_excerpt() ); ?></p>
			<?php endif; ?>
			<?php bhr_posted_meta(); ?>
		</header>

		<?php if ( has_post_thumbnail() ) : ?>
			<figure class="article-figure wrap wrap--text">
				<?php the_post_thumbnail( 'large', array( 'loading' => 'eager', 'fetchpriority' => 'high', 'sizes' => '(min-width: 45em) 672px, 100vw' ) ); ?>
				<?php $caption = wp_get_attachment_caption( get_post_thumbnail_id() ); ?>
				<?php if ( $caption ) : ?>
					<figcaption><?php echo wp_kses_post( $caption ); ?></figcaption>
				<?php endif; ?>
			</figure>
		<?php endif; ?>

		<div class="article-body wrap wrap--text entry-content">
			<?php the_content(); ?>
		</div>

		<footer class="entry-end wrap wrap--text">
			<?php if ( 'publish' === get_post_status() || is_preview() ) : ?>
				<section class="cite" aria-labelledby="cite-title">
					<h2 id="cite-title" class="end-title">Cite this entry</h2>
					<div class="cite-tabs">
						<?php
						$first = true;
						foreach ( bhr_citations() as $style => $text ) :
							$id = 'cite-' . strtolower( $style );
							?>
							<input class="cite-radio" type="radio" name="cite-style" id="<?php echo esc_attr( $id ); ?>-tab" <?php checked( $first ); ?>>
							<label class="cite-label" for="<?php echo esc_attr( $id ); ?>-tab"><?php echo esc_html( $style ); ?></label>
							<div class="cite-panel">
								<p class="cite-format"><?php echo 'APA' === $style ? 'Cite this entry in APA format:' : 'Cite this entry in ' . esc_html( $style ) . ' format:'; ?></p>
								<p class="cite-text" id="<?php echo esc_attr( $id ); ?>"><?php echo esc_html( $text ); ?></p>
								<button class="cite-copy" type="button" data-copy="<?php echo esc_attr( $id ); ?>" hidden>Copy</button>
							</div>
							<?php
							$first = false;
						endforeach;
						?>
					</div>
					<?php if ( strtotime( get_the_modified_date( 'c' ) ) - strtotime( get_the_date( 'c' ) ) > DAY_IN_SECONDS ) : ?>
						<p class="cite-updated">Last updated <?php echo esc_html( get_the_modified_date() ); ?>.</p>
					<?php endif; ?>
				</section>
			<?php endif; ?>

			<?php $sources = function_exists( 'bhr_story_sources' ) ? bhr_story_sources() : array(); ?>
			<?php if ( $sources ) : ?>
				<section class="sources" aria-labelledby="sources-title">
					<h2 id="sources-title" class="end-title">Sources of the author's information</h2>
					<ul>
						<?php foreach ( $sources as $s ) : ?>
							<li>
								<?php
								// “Title,” Publisher, URL   — a source given only by name is printed as plain text.
								$rest  = array_filter( array( $s[1], $s[2] ) );
								$title = $s[0] ? ( $rest ? '“' . $s[0] . ',” ' : $s[0] ) : '';
								echo esc_html( $title . $s[1] );
								if ( $s[2] ) {
									echo ( $s[1] ? ', ' : '' ) . '<a href="' . esc_url( $s[2] ) . '" target="_blank" rel="noopener">' . esc_html( preg_replace( '#^https?://(www\.)?#', '', $s[2] ) ) . '</a>';
								}
								?>
							</li>
						<?php endforeach; ?>
					</ul>
					<?php $credit = get_post_meta( get_the_ID(), 'bhr_image_credit', true ); ?>
					<?php if ( $credit ) : ?>
						<p class="image-credit"><strong>Images:</strong> <?php echo esc_html( $credit ); ?></p>
					<?php endif; ?>
				</section>
			<?php endif; ?>

			<?php
			$reel    = get_post_meta( get_the_ID(), 'bhr_reel_url', true );
			$podcast = get_post_meta( get_the_ID(), 'bhr_podcast_url', true );
			if ( $reel || $podcast ) :
				?>
				<p class="watch-listen">
					<?php if ( $reel ) : ?><a class="button" href="<?php echo esc_url( $reel ); ?>" target="_blank" rel="noopener">Watch the reel</a><?php endif; ?>
					<?php if ( $podcast ) : ?><a class="button" href="<?php echo esc_url( $podcast ); ?>">Listen to the podcast episode</a><?php endif; ?>
				</p>
			<?php endif; ?>

			<?php bhr_share_links(); ?>
		</footer>
	</article>

	<?php $more = bhr_discover_more(); ?>
	<?php if ( $more && $more->have_posts() ) : ?>
		<section class="home-section related" aria-labelledby="discover-title">
			<div class="wrap">
				<h2 id="discover-title" class="section-title">Discover more</h2>
				<?php bhr_story_grid( $more ); ?>
			</div>
		</section>
	<?php endif; ?>

	<div class="wrap wrap--text support-line">
		<p>Researching these stories takes real time and effort. <a href="<?php echo esc_url( BHR_KOFI ); ?>" target="_blank" rel="noopener">Support our work on Ko-fi</a>.</p>
	</div>
	<?php
endwhile;
?>
<script>
document.querySelectorAll('.cite-copy').forEach(function (b) {
	if (!navigator.clipboard) return;
	b.hidden = false;
	b.addEventListener('click', function () {
		navigator.clipboard.writeText(document.getElementById(b.dataset.copy).textContent).then(function () {
			b.textContent = 'Copied';
			setTimeout(function () { b.textContent = 'Copy'; }, 2000);
		});
	});
});
</script>
<?php
get_footer();

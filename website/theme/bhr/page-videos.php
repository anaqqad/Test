<?php
/**
 * Reels & videos: a light grid of our reels. Each card shows the reel's cover still (no video is loaded).
 * If the story has a YouTube link (bhr_reel_url), clicking the cover loads the YouTube player in place
 * (youtube-nocookie, no autoplay before the click). Other links (Facebook, Instagram) open in a new tab.
 */

get_header();
$query = new WP_Query( array(
	'post_type'      => 'story',
	'posts_per_page' => 60,
	'meta_key'       => 'bhr_reel_cover',
	'orderby'        => 'date',
	'order'          => 'DESC',
) );

function bhr_youtube_id( $url ) {
	return preg_match( '#(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([A-Za-z0-9_-]{11})#', (string) $url, $m ) ? $m[1] : '';
}
?>
<header class="page-header">
	<div class="wrap">
		<h1 class="page-title"><?php the_title(); ?></h1>
		<p class="page-intro">Short videos from The Black History Room. Every reel has a full written story with sources.</p>
	</div>
</header>
<div class="wrap list-wrap">
	<?php if ( $query->have_posts() ) : ?>
		<div class="reels">
			<?php
			while ( $query->have_posts() ) :
				$query->the_post();
				$cover = (int) get_post_meta( get_the_ID(), 'bhr_reel_cover', true );
				$url   = (string) get_post_meta( get_the_ID(), 'bhr_reel_url', true );
				$yt    = bhr_youtube_id( $url );
				?>
				<article class="reel">
					<div class="reel-frame"<?php echo $yt ? ' data-yt="' . esc_attr( $yt ) . '"' : ''; ?>>
						<?php echo wp_get_attachment_image( $cover, 'medium', false, array( 'loading' => 'lazy', 'alt' => 'Reel cover: ' . get_the_title() ) ); ?>
						<?php if ( $yt ) : ?>
							<button class="reel-play" type="button" aria-label="Play the reel about <?php echo esc_attr( get_the_title() ); ?>"><span></span></button>
						<?php endif; ?>
					</div>
					<div class="reel-body">
						<h2 class="reel-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
						<p class="reel-links">
							<a href="<?php the_permalink(); ?>">Read the story</a>
							<?php if ( $url && ! $yt ) : ?> · <a href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener">Watch</a><?php endif; ?>
						</p>
					</div>
				</article>
			<?php endwhile; ?>
			<?php wp_reset_postdata(); ?>
		</div>
	<?php else : ?>
		<p class="empty-note">Videos will be listed here as their stories are published.</p>
	<?php endif; ?>
</div>
<script>
document.querySelectorAll('.reel-frame[data-yt] .reel-play').forEach(function (b) {
	b.addEventListener('click', function () {
		var box = b.parentNode, f = document.createElement('iframe');
		f.src = 'https://www.youtube-nocookie.com/embed/' + box.getAttribute('data-yt') + '?autoplay=1&rel=0';
		f.title = b.getAttribute('aria-label');
		f.allow = 'autoplay; encrypted-media; picture-in-picture';
		f.allowFullscreen = true;
		box.innerHTML = '';
		box.appendChild(f);
	});
});
</script>
<?php
get_footer();

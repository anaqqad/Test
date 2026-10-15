</main>
<footer class="site-footer">
	<div class="wrap footer-grid">
		<div class="footer-brand">
			<p class="brand-name">The Black History Room</p>
			<p><?php echo esc_html( get_bloginfo( 'description' ) ); ?></p>
			<p><a class="button button--gold" href="<?php echo esc_url( BHR_KOFI ); ?>" rel="noopener">Support us on Ko-fi</a></p>
		</div>
		<nav class="footer-nav" aria-label="Footer">
			<?php
			wp_nav_menu( array(
				'theme_location' => 'footer',
				'container'      => false,
				'menu_class'     => 'footer-menu',
				'depth'          => 1,
				'fallback_cb'    => false,
			) );
			?>
		</nav>
		<div class="footer-podcast">
			<p class="footer-label">Podcast</p>
			<p><a href="<?php echo esc_url( get_post_type_archive_link( 'bhr_episode' ) ); ?>"><?php echo esc_html( BHR_PODCAST_NAME ); ?></a></p>
			<p><a href="<?php echo esc_url( BHR_PODCAST_SPOTIFY ); ?>" rel="noopener">Listen on Spotify</a></p>
		</div>
	</div>
	<div class="wrap footer-base">
		<p>&copy; <?php echo esc_html( wp_date( 'Y' ) ); ?> The Black History Room</p>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>

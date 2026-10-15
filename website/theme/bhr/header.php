<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#141210">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
	<div class="wrap masthead">
		<a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
			<span class="brand-small">The</span>
			<span class="brand-name">Black History <span class="brand-gold">Room</span></span>
		</a>
		<div class="masthead-tools">
			<div class="masthead-search"><?php get_search_form(); ?></div>
			<a class="donate" href="<?php echo esc_url( BHR_KOFI ); ?>" target="_blank" rel="noopener">Donate</a>
			<button class="nav-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" hidden>Menu</button>
		</div>
	</div>
	<nav id="primary-nav" class="primary-nav" aria-label="Main">
		<div class="wrap">
			<div class="nav-search"><?php get_search_form(); ?></div>
			<ul class="mega">
				<?php
				$featured = new WP_Query( array( 'post_type' => 'story', 'posts_per_page' => 1, 'no_found_rows' => true, 'ignore_sticky_posts' => false ) );
				foreach ( bhr_mega_menu() as $key => $item ) :
					$panel = 'mega-' . $key;
					?>
					<li class="mega-item">
						<button class="mega-toggle" type="button" aria-expanded="false" aria-controls="<?php echo esc_attr( $panel ); ?>"><?php echo esc_html( $item['label'] ); ?></button>
						<div class="mega-panel" id="<?php echo esc_attr( $panel ); ?>">
							<div class="mega-inner">
								<?php foreach ( $item['columns'] as $heading => $links ) : ?>
									<div class="mega-col<?php echo count( $links ) > 6 ? ' mega-col--wide' : ''; ?>">
										<p class="mega-heading"><?php echo esc_html( $heading ); ?></p>
										<ul>
											<?php foreach ( $links as $label => $url ) : ?>
												<li><a href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $label ); ?></a></li>
											<?php endforeach; ?>
										</ul>
									</div>
								<?php endforeach; ?>
								<?php if ( ! empty( $item['featured'] ) && $featured->have_posts() ) : $featured->the_post(); ?>
									<a class="mega-feature" href="<?php the_permalink(); ?>">
										<?php the_post_thumbnail( 'bhr-card', array( 'loading' => 'lazy' ) ); ?>
										<span class="mega-heading">Featured story</span>
										<span class="mega-feature-title"><?php echo esc_html( bhr_story_title() ); ?></span>
									</a>
									<?php wp_reset_postdata(); ?>
								<?php endif; ?>
							</div>
						</div>
					</li>
				<?php endforeach; ?>
			</ul>
		</div>
	</nav>
</header>
<script>
(function () {
	var d = document, toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('primary-nav');
	d.documentElement.classList.add('js');
	if (toggle && nav) {
		toggle.hidden = false;
		toggle.addEventListener('click', function () {
			var open = toggle.getAttribute('aria-expanded') === 'true';
			toggle.setAttribute('aria-expanded', String(!open));
			nav.classList.toggle('is-open', !open);
		});
	}
	var buttons = d.querySelectorAll('.mega-toggle');
	function closeAll(except) {
		buttons.forEach(function (b) { if (b !== except) b.setAttribute('aria-expanded', 'false'); });
	}
	buttons.forEach(function (b) {
		b.addEventListener('click', function () {
			var open = b.getAttribute('aria-expanded') === 'true';
			closeAll(b);
			b.setAttribute('aria-expanded', String(!open));
		});
	});
	d.addEventListener('keydown', function (e) {
		if (e.key === 'Escape') {
			var open = d.querySelector('.mega-toggle[aria-expanded="true"]');
			closeAll();
			if (open) open.focus();
		}
	});
	d.addEventListener('click', function (e) {
		if (!e.target.closest('.mega-item')) closeAll();
	});
})();
</script>
<main id="main" class="site-main">

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
			<span class="brand-name">Black History Room</span>
		</a>
		<div class="masthead-tools">
			<?php get_search_form(); ?>
			<button class="nav-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" hidden>Menu</button>
		</div>
	</div>
	<nav id="primary-nav" class="primary-nav" aria-label="Main">
		<div class="wrap">
			<div class="nav-search"><?php get_search_form(); ?></div>
			<?php
			wp_nav_menu( array(
				'theme_location' => 'primary',
				'container'      => false,
				'menu_class'     => 'menu',
				'depth'          => 1,
				'fallback_cb'    => false,
			) );
			?>
		</div>
	</nav>
</header>
<script>
(function () {
	var b = document.querySelector('.nav-toggle'), n = document.getElementById('primary-nav');
	if (!b || !n) return;
	b.hidden = false;
	document.documentElement.classList.add('js');
	b.addEventListener('click', function () {
		var open = b.getAttribute('aria-expanded') === 'true';
		b.setAttribute('aria-expanded', String(!open));
		n.classList.toggle('is-open', !open);
	});
})();
</script>
<main id="main" class="site-main">

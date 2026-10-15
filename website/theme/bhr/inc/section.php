<?php
/**
 * Section pages (/african-american-history/, /global-african-history/): filters, A–Z, story grid, and the map.
 */

defined( 'ABSPATH' ) || exit;

function bhr_section_url( $section, array $args = array() ) {
	$base = home_url( '/' . $section . '/' );
	return $args ? add_query_arg( array_filter( $args ), $base ) : $base;
}

function bhr_term_options( $taxonomy, $selected, $hide_empty = false ) {
	$terms = get_terms( array( 'taxonomy' => $taxonomy, 'hide_empty' => $hide_empty, 'meta_key' => 'bhr_order', 'orderby' => 'meta_value_num' ) );
	if ( is_wp_error( $terms ) || ! $terms ) {
		$terms = get_terms( array( 'taxonomy' => $taxonomy, 'hide_empty' => $hide_empty, 'orderby' => 'name' ) );
	}
	foreach ( is_wp_error( $terms ) ? array() : $terms as $term ) {
		printf( '<option value="%s"%s>%s</option>', esc_attr( $term->slug ), selected( $selected, $term->slug, false ), esc_html( $term->name ) );
	}
}

function bhr_render_filters( $section ) {
	$domain  = sanitize_title( (string) get_query_var( 'bhr_domain' ) );
	$country = sanitize_title( (string) get_query_var( 'bhr_country' ) );
	$era     = sanitize_title( (string) get_query_var( 'bhr_era' ) );
	$letter  = strtoupper( substr( (string) get_query_var( 'bhr_letter' ), 0, 1 ) );
	?>
	<form class="filters" method="get" action="<?php echo esc_url( bhr_section_url( $section ) ); ?>">
		<label>Subject
			<select name="bhr_domain"><option value="">All subjects</option><?php bhr_term_options( 'domain', $domain ); ?></select>
		</label>
		<label>Country
			<select name="bhr_country"><option value="">All countries</option><?php bhr_term_options( 'country', $country, true ); ?></select>
		</label>
		<label>Era
			<select name="bhr_era"><option value="">All eras</option><?php bhr_term_options( 'era', $era ); ?></select>
		</label>
		<button type="submit">Filter</button>
		<?php if ( $domain || $country || $era || $letter ) : ?>
			<a class="filters-reset" href="<?php echo esc_url( bhr_section_url( $section ) ); ?>">Clear filters</a>
		<?php endif; ?>
	</form>
	<nav class="az" aria-label="Stories A to Z">
		<?php foreach ( range( 'A', 'Z' ) as $l ) : ?>
			<a href="<?php echo esc_url( bhr_section_url( $section, array( 'bhr_letter' => $l, 'bhr_domain' => $domain, 'bhr_country' => $country, 'bhr_era' => $era ) ) ); ?>"<?php echo $l === $letter ? ' aria-current="true"' : ''; ?>><?php echo esc_html( $l ); ?></a>
		<?php endforeach; ?>
	</nav>
	<?php
}

function bhr_render_section_list( $section ) {
	$query = bhr_section_query( $section, 12 );
	if ( $query->have_posts() ) {
		bhr_story_grid( $query, 'h2' );
		$pages = (int) $query->max_num_pages;
		if ( $pages > 1 ) {
			$current = max( 1, (int) get_query_var( 'bhr_pg' ) );
			echo '<nav class="pagination" aria-label="Pages"><div class="nav-links">';
			for ( $i = 1; $i <= $pages; $i++ ) {
				$url = add_query_arg( 'bhr_pg', $i > 1 ? $i : false );
				printf( $i === $current ? '<span class="page-numbers current" aria-current="page">%2$d</span>' : '<a class="page-numbers" href="%1$s">%2$d</a>', esc_url( $url ), $i );
			}
			echo '</div></nav>';
		}
	} else {
		echo '<p class="empty-note">No stories match these filters yet. New stories are on the way.</p>';
	}
}

/**
 * World map (inline SVG built from Natural Earth) + alphabetical country list. Works without JavaScript.
 */
function bhr_render_map() {
	$file = get_theme_file_path( 'assets/map/world-110m.json' );
	$map  = json_decode( (string) file_get_contents( $file ), true );
	if ( ! $map ) {
		return;
	}
	$counts = bhr_country_counts();
	?>
	<div class="map-layout">
		<section class="country-list" id="countries" aria-labelledby="countries-title">
			<h2 id="countries-title" class="map-heading">Countries A–Z</h2>
			<?php if ( $counts ) : ?>
				<ul>
					<?php foreach ( $counts as $iso => $c ) : ?>
						<li><a href="<?php echo esc_url( $c[2] ); ?>"><?php echo esc_html( $c[0] ); ?> <span class="count">(<?php echo (int) $c[1]; ?>)</span></a></li>
					<?php endforeach; ?>
				</ul>
			<?php else : ?>
				<p class="empty-note">Countries will appear here as stories are published.</p>
			<?php endif; ?>
		</section>
		<figure class="world-map">
			<div class="map-zoom" hidden>
				<button type="button" data-zoom="in" aria-label="Zoom in">+</button>
				<button type="button" data-zoom="out" aria-label="Zoom out">−</button>
				<button type="button" data-zoom="reset" aria-label="Reset zoom">Reset</button>
			</div>
			<svg viewBox="<?php echo esc_attr( $map['viewBox'] ); ?>" role="group" aria-label="World map. Countries with stories are links." focusable="false">
				<?php
				foreach ( $map['countries'] as $row ) {
					list( $iso, $name, $d ) = $row;
					if ( $iso && isset( $counts[ $iso ] ) ) {
						$c     = $counts[ $iso ];
						$label = sprintf( '%s: %d %s', $c[0], $c[1], 1 === $c[1] ? 'story' : 'stories' );
						printf(
							'<a href="%s" aria-label="%s"><title>%s</title><path class="has-stories" d="%s"/></a>',
							esc_url( $c[2] ),
							esc_attr( $label ),
							esc_html( $label ),
							esc_attr( $d )
						);
					} else {
						printf( '<path d="%s" aria-hidden="true"><title>%s</title></path>', esc_attr( $d ), esc_html( $name ) );
					}
				}
				?>
			</svg>
			<figcaption>Coloured countries have stories. Boundaries: Natural Earth (public domain).</figcaption>
		</figure>
	</div>
	<script>
	(function () {
		var svg = document.querySelector('.world-map svg'), ui = document.querySelector('.map-zoom');
		if (!svg || !ui) return;
		ui.hidden = false;
		var base = svg.viewBox.baseVal, full = [base.x, base.y, base.width, base.height], z = 1;
		function apply() {
			var w = full[2] / z, h = full[3] / z;
			svg.setAttribute('viewBox', [full[0] + (full[2] - w) / 2, full[1] + (full[3] - h) / 2, w, h].join(' '));
		}
		ui.addEventListener('click', function (e) {
			var a = e.target.getAttribute('data-zoom');
			if (!a) return;
			z = a === 'in' ? Math.min(z * 1.5, 6) : a === 'out' ? Math.max(z / 1.5, 1) : 1;
			apply();
		});
	})();
	</script>
	<?php
}

function bhr_render_section_page( $section, $with_map = false ) {
	$domain_slug = sanitize_title( (string) get_query_var( 'bhr_domain' ) );
	$domain      = $domain_slug ? get_term_by( 'slug', $domain_slug, 'domain' ) : null;
	$title       = BHR_SECTIONS[ $section ] ?? get_the_title();
	?>
	<header class="page-header page-header--section">
		<div class="wrap">
			<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a><?php if ( $domain ) : ?> › <a href="<?php echo esc_url( bhr_section_url( $section ) ); ?>"><?php echo esc_html( $title ); ?></a><?php endif; ?></nav>
			<h1 class="page-title"><?php echo esc_html( $domain ? $domain->name : $title ); ?></h1>
			<?php
			while ( have_posts() ) {
				the_post();
				if ( ! $domain && get_the_content() ) {
					echo '<div class="page-intro">';
					the_content();
					echo '</div>';
				}
			}
			?>
		</div>
	</header>
	<?php if ( $with_map && ! $domain ) : ?>
		<section class="map-section"><div class="wrap"><?php bhr_render_map(); ?></div></section>
	<?php endif; ?>
	<div class="wrap list-wrap">
		<?php if ( $with_map && ! $domain ) : ?>
			<h2 class="section-title list-title">All Global African History stories</h2>
		<?php endif; ?>
		<?php bhr_render_filters( $section ); ?>
		<?php bhr_render_section_list( $section ); ?>
	</div>
	<?php
}

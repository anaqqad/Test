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
 * World map + alphabetical country list. The country list is plain HTML (works without JavaScript and for screen
 * readers). The map itself is a static, browser-cached SVG file (assets/map/world-110m.svg) fetched only on this page;
 * a small script colours the countries that have stories and turns them into links.
 */
function bhr_render_map() {
	$counts = bhr_country_counts();
	$data   = array();
	foreach ( $counts as $iso => $c ) {
		$data[ $iso ] = array( 'n' => $c[0], 'c' => $c[1], 'u' => $c[2] );
	}
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
			<div class="map-canvas" data-src="<?php echo esc_url( add_query_arg( 'ver', BHR_VERSION, get_theme_file_uri( 'assets/map/world-110m.svg' ) ) ); ?>">
				<img src="<?php echo esc_url( bhr_map_preview_url() ); ?>" width="960" height="500" alt="World map. Use the country list to open a country." decoding="async">
			</div>
			<figcaption>Coloured countries have stories. Boundaries: Natural Earth (public domain).</figcaption>
		</figure>
	</div>
	<script>
	(function () {
		var box = document.querySelector('.map-canvas'), ui = document.querySelector('.map-zoom');
		var counts = <?php echo wp_json_encode( (object) $data ); ?>;
		if (!box || !window.fetch) return;
		fetch(box.getAttribute('data-src')).then(function (r) { return r.text(); }).then(function (text) {
			box.innerHTML = text;
			var svg = box.querySelector('svg'), ns = 'http://www.w3.org/2000/svg';
			svg.setAttribute('role', 'group');
			svg.setAttribute('aria-label', 'World map. Countries with stories are links.');
			svg.querySelectorAll('path').forEach(function (p) {
				var c = counts[p.getAttribute('data-iso')];
				if (!c) { p.setAttribute('aria-hidden', 'true'); return; }
				var a = document.createElementNS(ns, 'a'), label = c.n + ': ' + c.c + (c.c === 1 ? ' story' : ' stories');
				a.setAttribute('href', c.u);
				a.setAttribute('aria-label', label);
				p.querySelector('title').textContent = label;
				p.setAttribute('class', 'has-stories');
				p.parentNode.insertBefore(a, p);
				a.appendChild(p);
			});
			if (!ui) return;
			ui.hidden = false;
			var b = svg.viewBox.baseVal, full = [b.x, b.y, b.width, b.height], z = 1;
			ui.addEventListener('click', function (e) {
				var act = e.target.getAttribute('data-zoom');
				if (!act) return;
				z = act === 'in' ? Math.min(z * 1.5, 6) : act === 'out' ? Math.max(z / 1.5, 1) : 1;
				var w = full[2] / z, h = full[3] / z;
				svg.setAttribute('viewBox', [full[0] + (full[2] - w) / 2, full[1] + (full[3] - h) / 2, w, h].join(' '));
			});
		});
	})();
	</script>
	<?php
}

/**
 * Static preview image of the map (countries with stories in deep red). Written to uploads/bhr/ and rebuilt only
 * when the set of countries with stories changes. Used on the homepage and as the map page's first paint.
 */
function bhr_map_preview_url() {
	$counts = bhr_country_counts();
	$key    = substr( md5( implode( ',', array_keys( $counts ) ) ), 0, 10 );
	$up     = wp_upload_dir();
	$dir    = trailingslashit( $up['basedir'] ) . 'bhr/';
	$file   = "map-preview-{$key}.svg";
	if ( ! file_exists( $dir . $file ) ) {
		$map = json_decode( (string) file_get_contents( get_theme_file_path( 'assets/map/world-110m.json' ) ), true );
		if ( $map ) {
			wp_mkdir_p( $dir );
			$svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="' . esc_attr( $map['viewBox'] ) . '"><rect width="100%" height="100%" fill="#1c1916"/>';
			foreach ( $map['countries'] as $row ) {
				$fill = ( $row[0] && isset( $counts[ $row[0] ] ) ) ? '#8e1b1b' : '#3a3631';
				$svg .= '<path fill="' . $fill . '" stroke="#1c1916" stroke-width="0.5" d="' . esc_attr( $row[2] ) . '"/>';
			}
			file_put_contents( $dir . $file, $svg . '</svg>' );
			foreach ( glob( $dir . 'map-preview-*.svg' ) as $old ) {
				if ( basename( $old ) !== $file ) {
					unlink( $old );
				}
			}
		}
	}
	return trailingslashit( $up['baseurl'] ) . 'bhr/' . $file;
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
		<?php bhr_render_explorer(); ?>
	<?php endif; ?>
	<div class="wrap list-wrap<?php echo $with_map && ! $domain ? ' no-js-only' : ''; ?>">
		<?php if ( $with_map && ! $domain ) : ?>
			<h2 class="section-title list-title">All Global African History stories</h2>
		<?php endif; ?>
		<?php bhr_render_filters( $section ); ?>
		<?php bhr_render_section_list( $section ); ?>
	</div>
	<?php
}

/**
 * Interactive story map (Leaflet + Natural Earth boundaries). Assets are enqueued by the page template only.
 * Without JavaScript the A–Z country list (links to country pages) and the server-rendered list below still work.
 */
function bhr_render_explorer() {
	$counts = bhr_country_counts();
	$eras   = array( '1300-1499' => '1300s–1400s', '1800-1899' => '1800s', '1900-1999' => '1900s', '2000-2099' => '2000s' );
	?>
	<section class="explorer" id="explorer"
		data-api="<?php echo esc_url( rest_url( 'bhr/v1/map' ) ); ?>"
		data-geo="<?php echo esc_url( add_query_arg( 'ver', BHR_VERSION, get_theme_file_uri( 'assets/map/world-110m.geojson' ) ) ); ?>">
		<div class="wrap">
			<div class="explorer-layout">
				<aside class="explorer-side">
					<details class="explorer-filters" open>
						<summary class="explorer-heading">Filters: time, person, subject</summary>
						<fieldset class="ex-group">
							<legend>Time</legend>
							<div class="ex-range">
								<label>From <output class="ex-from-out"></output><input id="ex-from" type="range" step="10" aria-label="From year"></label>
								<label>To <output class="ex-to-out"></output><input id="ex-to" type="range" step="10" aria-label="To year"></label>
							</div>
							<div class="ex-chips">
								<?php foreach ( $eras as $range => $label ) : ?>
									<button type="button" class="ex-chip" data-era="<?php echo esc_attr( $range ); ?>" aria-pressed="false"><?php echo esc_html( $label ); ?></button>
								<?php endforeach; ?>
							</div>
						</fieldset>
						<fieldset class="ex-group">
							<legend>Person</legend>
							<div class="ex-chips">
								<button type="button" class="ex-chip" data-gender="" aria-pressed="true">Everyone</button>
								<button type="button" class="ex-chip" data-gender="woman" aria-pressed="false">Women</button>
								<button type="button" class="ex-chip" data-gender="man" aria-pressed="false">Men</button>
								<button type="button" class="ex-chip" data-gender="group" aria-pressed="false">Groups / events</button>
							</div>
						</fieldset>
						<div class="ex-selects">
							<label>Subject<select id="ex-domain"></select></label>
							<label>Section<select id="ex-section"></select></label>
							<label>Country<select id="ex-country"></select></label>
						</div>
						<button type="button" class="btn btn--outline explorer-reset">Reset filters</button>
					</details>
					<section class="country-list" id="countries" aria-labelledby="countries-title">
						<h2 id="countries-title" class="map-heading">Countries A–Z</h2>
						<?php if ( $counts ) : ?>
							<ul>
								<?php foreach ( $counts as $iso => $c ) : ?>
									<li><a data-iso="<?php echo esc_attr( $iso ); ?>" href="<?php echo esc_url( $c[2] ); ?>"><?php echo esc_html( $c[0] ); ?> <span class="count">(<?php echo (int) $c[1]; ?>)</span></a></li>
								<?php endforeach; ?>
							</ul>
						<?php else : ?>
							<p class="empty-note">Countries will appear here as stories are published.</p>
						<?php endif; ?>
					</section>
				</aside>
				<div class="explorer-main">
					<div class="explorer-map" role="region" aria-label="Interactive map of stories. Click a red country to list its stories below; gold pins mark places.">
						<img class="explorer-fallback" src="<?php echo esc_url( bhr_map_preview_url() ); ?>" width="960" height="500" alt="World map: countries with stories are highlighted in red" decoding="async">
					</div>
					<p class="explorer-legend"><span class="lg lg-red"></span> Country with stories <span class="lg lg-gold"></span> Place in a story · Drag to move, use + / − to zoom.</p>
				</div>
			</div>
			<div class="explorer-results" aria-live="polite">
				<header class="section-head">
					<div>
						<h2 class="section-title explorer-results-title">All stories</h2>
						<p class="section-intro explorer-count"></p>
					</div>
					<button type="button" class="btn btn--outline explorer-clear-country" hidden>Show all countries</button>
				</header>
				<div class="grid grid--card explorer-grid"></div>
				<p class="empty-note explorer-empty" hidden>No stories match these filters yet. Try a wider time range or another subject.</p>
			</div>
		</div>
	</section>
	<?php
}

/*
 * The Black History Room: interactive story map (Leaflet).
 * Countries with matching stories are red; story places are gold pins. Clicking a country keeps the map and shows
 * that country's stories below. Filters: time range, gender, subject, section, country. State lives in the URL hash
 * (#country=us&from=1800&to=1900&gender=woman&domain=sports&section=...) so a view can be shared.
 * Data: /wp-json/bhr/v1/map (stories) + world-110m.geojson (Natural Earth boundaries, public domain).
 */
(function () {
	'use strict';
	var root = document.getElementById('explorer');
	if (!root || !window.L || !window.fetch) return;
	document.documentElement.classList.add('has-explorer');
	// Phones: filters start folded so the map is visible sooner.
	var det = root.querySelector('details.explorer-filters');
	if (det && window.matchMedia('(max-width: 1023px)').matches) det.open = false;

	var $ = function (sel) { return root.querySelector(sel); };
	var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
	var data, geoLayer, pins = L.layerGroup(), layersByIso = {};
	var MIN = 1300, MAX = Math.ceil(new Date().getFullYear() / 10) * 10; // on the 10-year slider grid
	var state = { country: '', from: MIN, to: MAX, gender: '', domain: '', section: '' };

	// ---------- URL hash <-> state ----------
	function readHash() {
		var h = new URLSearchParams(location.hash.replace(/^#/, ''));
		state.country = h.get('country') || '';
		state.gender = h.get('gender') || '';
		state.domain = h.get('domain') || '';
		state.section = h.get('section') || '';
		state.from = clampYear(parseInt(h.get('from'), 10), MIN);
		state.to = clampYear(parseInt(h.get('to'), 10), MAX);
	}
	function writeHash() {
		var h = new URLSearchParams();
		if (state.country) h.set('country', state.country);
		if (state.from > MIN) h.set('from', state.from);
		if (state.to < MAX) h.set('to', state.to);
		['gender', 'domain', 'section'].forEach(function (k) { if (state[k]) h.set(k, state[k]); });
		var s = h.toString();
		history.replaceState(null, '', s ? '#' + s : location.pathname + location.search);
	}
	function clampYear(v, d) { return isNaN(v) ? d : Math.min(MAX, Math.max(MIN, v)); }

	// ---------- filtering ----------
	function matches(s, ignoreCountry) {
		if (!ignoreCountry && state.country && s.c !== state.country) return false;
		if (state.gender && s.g.indexOf(state.gender) < 0) return false;
		if (state.domain && s.d.indexOf(state.domain) < 0) return false;
		if (state.section && s.s.indexOf(state.section) < 0) return false;
		if (s.from == null) return state.from === MIN && state.to === MAX;
		return s.to >= state.from && s.from <= state.to;
	}

	// ---------- rendering ----------
	function card(s) {
		return '<article class="scard">' +
			'<a class="scard-media" href="' + esc(s.u) + '" tabindex="-1" aria-hidden="true">' +
			(s.img ? '<img src="' + esc(s.img) + '" srcset="' + esc(s.img) + ' 480w, ' + esc(s.img2) + ' 800w" sizes="(min-width: 1024px) 31vw, (min-width: 640px) 46vw, 92vw" width="480" height="360" alt="" loading="lazy" decoding="async">' : '<span class="scard-placeholder">' + esc(s.t.charAt(0)) + '</span>') +
			'</a><div class="scard-body">' +
			(s.dn ? '<p class="kicker kicker--static">' + esc(s.dn) + '</p>' : '') +
			'<h3 class="scard-title"><a href="' + esc(s.u) + '">' + esc(s.t) + '</a>' + (s.y ? ' <span class="scard-years">' + esc(s.y) + '</span>' : '') + '</h3>' +
			(s.e ? '<p class="scard-excerpt">' + esc(s.e) + '</p>' : '') +
			'<a class="btn btn--primary scard-more" href="' + esc(s.u) + '">Read more<span class="screen-reader-text"> about ' + esc(s.t) + '</span></a>' +
			'</div></article>';
	}

	function render() {
		var visible = data.stories.filter(function (s) { return matches(s, false); });
		var perCountry = {};
		data.stories.forEach(function (s) { if (s.c && matches(s, true)) perCountry[s.c] = (perCountry[s.c] || 0) + 1; });

		// Countries: red when they have matching stories; gold outline when selected.
		geoLayer.eachLayer(function (layer) {
			var iso = layer.feature.properties.iso2, n = perCountry[iso] || 0, sel = iso && iso === state.country;
			layer.setStyle({
				fillColor: n ? '#8e1b1b' : '#3a3631',
				fillOpacity: 1,
				color: sel ? '#e0a93b' : '#1c1916',
				weight: sel ? 2.5 : 0.6,
			});
			if (sel) layer.bringToFront();
			layer.setTooltipContent(esc(layer.feature.properties.name) + (n ? ' — ' + n + (n === 1 ? ' story' : ' stories') : ''));
		});

		// Pins: one per place, listing the matching stories there.
		pins.clearLayers();
		var places = {};
		visible.forEach(function (s) {
			if (!s.place) return;
			var k = s.place.lat + ',' + s.place.lng;
			(places[k] = places[k] || { p: s.place, list: [] }).list.push(s);
		});
		Object.keys(places).forEach(function (k) {
			var g = places[k];
			L.circleMarker([g.p.lat, g.p.lng], { radius: g.list.length > 1 ? 9 : 7, color: '#141210', weight: 2, fillColor: '#e0a93b', fillOpacity: 1 })
				.bindPopup('<p class="pin-place">' + esc(g.p.n) + '</p><ul class="pin-list">' + g.list.map(function (s) {
					return '<li><a href="' + esc(s.u) + '">' + esc(s.t) + '</a>' + (s.y ? ' <span>' + esc(s.y) + '</span>' : '') + '</li>';
				}).join('') + '</ul>')
				.addTo(pins);
		});

		// Results below the map.
		var title = state.country ? 'Stories in ' + (data.countries[state.country] || state.country.toUpperCase()) : 'All stories';
		$('.explorer-results-title').textContent = title;
		$('.explorer-count').textContent = visible.length + (visible.length === 1 ? ' story' : ' stories');
		$('.explorer-clear-country').hidden = !state.country;
		$('.explorer-grid').innerHTML = visible.length ? visible.map(card).join('') : '';
		$('.explorer-empty').hidden = visible.length > 0;

		// Controls reflect state.
		$('#ex-from').value = state.from; $('#ex-to').value = state.to;
		$('.ex-from-out').textContent = state.from; $('.ex-to-out').textContent = state.to;
		$('#ex-domain').value = state.domain; $('#ex-section').value = state.section; $('#ex-country').value = state.country;
		root.querySelectorAll('[data-gender]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-gender') === state.gender)); });
		root.querySelectorAll('[data-era]').forEach(function (b) {
			var r = b.getAttribute('data-era').split('-');
			b.setAttribute('aria-pressed', String(+r[0] === state.from && +r[1] === state.to));
		});
		writeHash();
	}

	function selectCountry(iso, fly) {
		state.country = iso;
		render();
		if (fly && iso && layersByIso[iso]) map.flyToBounds(layersByIso[iso].getBounds(), { maxZoom: 4, duration: 0.6 });
		if (fly === 'scroll') $('.explorer-results').scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	// ---------- controls ----------
	function options(sel, obj, all) {
		sel.innerHTML = '<option value="">' + all + '</option>' + Object.keys(obj).map(function (k) { return '<option value="' + esc(k) + '">' + esc(obj[k]) + '</option>'; }).join('');
	}
	function wire() {
		options($('#ex-domain'), data.domains, 'All subjects');
		options($('#ex-section'), data.sections, 'All sections');
		options($('#ex-country'), data.countries, 'All countries');
		['#ex-from', '#ex-to'].forEach(function (id) {
			var el = $(id);
			el.min = MIN; el.max = MAX;
			el.addEventListener('input', function () {
				var a = +$('#ex-from').value, b = +$('#ex-to').value;
				if (a > b) { if (id === '#ex-from') b = a; else a = b; }
				state.from = a; state.to = b; render();
			});
		});
		root.querySelectorAll('[data-era]').forEach(function (b) {
			b.addEventListener('click', function () {
				var r = b.getAttribute('data-era').split('-');
				var on = b.getAttribute('aria-pressed') === 'true';
				state.from = on ? MIN : Math.max(MIN, +r[0]); state.to = on ? MAX : Math.min(MAX, +r[1]); render();
			});
		});
		root.querySelectorAll('[data-gender]').forEach(function (b) {
			b.addEventListener('click', function () { state.gender = b.getAttribute('data-gender'); render(); });
		});
		$('#ex-domain').addEventListener('change', function (e) { state.domain = e.target.value; render(); });
		$('#ex-section').addEventListener('change', function (e) { state.section = e.target.value; render(); });
		$('#ex-country').addEventListener('change', function (e) { selectCountry(e.target.value, true); });
		$('.explorer-clear-country').addEventListener('click', function () { selectCountry('', false); map.flyToBounds(WORLD, { duration: 0.6 }); });
		$('.explorer-reset').addEventListener('click', function () {
			state = { country: '', from: MIN, to: MAX, gender: '', domain: '', section: '' };
			render(); map.flyToBounds(WORLD, { duration: 0.6 });
		});
		// The A–Z country list (also the no-JS fallback) selects instead of leaving the page.
		document.querySelectorAll('.country-list a[data-iso]').forEach(function (a) {
			a.addEventListener('click', function (e) { e.preventDefault(); selectCountry(a.getAttribute('data-iso'), 'scroll'); });
		});
	}

	// ---------- map ----------
	var WORLD = [[-50, -165], [75, 175]];
	var map = L.map($('.explorer-map'), { zoomSnap: 0.5, minZoom: 1, maxZoom: 6, worldCopyJump: false, maxBounds: [[-75, -200], [88, 200]], attributionControl: true, scrollWheelZoom: false });
	map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
	map.attributionControl.addAttribution('Boundaries: Natural Earth (public domain)');
	map.fitBounds(WORLD);
	map.on('focus', function () { map.scrollWheelZoom.enable(); });
	map.on('blur', function () { map.scrollWheelZoom.disable(); });

	Promise.all([
		fetch(root.getAttribute('data-api'), { credentials: 'omit' }).then(function (r) { return r.json(); }),
		fetch(root.getAttribute('data-geo')).then(function (r) { return r.json(); }),
	]).then(function (res) {
		data = res[0];
		data.stories.forEach(function (s) { if (s.from != null && s.from < MIN) MIN = Math.floor(s.from / 100) * 100; });
		readHash();
		geoLayer = L.geoJSON(res[1], {
			style: { fillColor: '#3a3631', fillOpacity: 1, color: '#1c1916', weight: 0.6 },
			onEachFeature: function (f, layer) {
				var iso = f.properties.iso2;
				if (iso) layersByIso[iso] = layer;
				layer.bindTooltip(esc(f.properties.name), { sticky: true, direction: 'top', className: 'map-tip' });
				layer.on('click', function () {
					var has = data.stories.some(function (s) { return s.c === iso; });
					if (has) selectCountry(state.country === iso ? '' : iso, state.country !== iso);
				});
				layer.on('mouseover', function () { if (iso !== state.country) layer.setStyle({ color: '#e0a93b', weight: 1.5 }); });
				layer.on('mouseout', function () { if (iso !== state.country) layer.setStyle({ color: '#1c1916', weight: 0.6 }); });
			},
		}).addTo(map);
		pins.addTo(map);
		wire();
		render();
		if (state.country && layersByIso[state.country]) map.fitBounds(layersByIso[state.country].getBounds(), { maxZoom: 4 });
		// A pasted/shared link or Back/Forward changes only the hash: re-read it.
		window.addEventListener('hashchange', function () {
			readHash();
			render();
			map.flyToBounds(state.country && layersByIso[state.country] ? layersByIso[state.country].getBounds() : WORLD, { maxZoom: 4, duration: 0.6 });
		});
		root.classList.add('is-ready');
	}).catch(function () {
		root.classList.add('is-failed');
	});
})();

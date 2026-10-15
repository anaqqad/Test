<?php $bhr_search_id = wp_unique_id( 'search-' ); ?>
<form role="search" method="get" class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
	<label class="screen-reader-text" for="<?php echo esc_attr( $bhr_search_id ); ?>">Search stories</label>
	<input id="<?php echo esc_attr( $bhr_search_id ); ?>" type="search" name="s" value="<?php echo esc_attr( get_search_query() ); ?>" placeholder="Search stories">
	<button type="submit">Search</button>
</form>

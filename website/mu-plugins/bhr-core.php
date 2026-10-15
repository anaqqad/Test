<?php
/**
 * Plugin Name: The Black History Room core
 * Description: Story post type, Section / Domain / Country / Era taxonomies, story fields, section URLs. Content model
 *              lives here (not in the theme) so it survives a theme change. Must-use plugin, loaded automatically.
 * Version: 1.0.0
 */

defined( 'ABSPATH' ) || exit;

require __DIR__ . '/bhr-core/story.php';
require __DIR__ . '/bhr-core/fields.php';
require __DIR__ . '/bhr-core/routes.php';

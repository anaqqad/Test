<?php
/**
 * Default social sharing image (1200 x 630): black background, BHR monogram, cream site name, gold rules, tagline.
 * Usage: php make_og.php <Cinzel.ttf> <site-icon.png (512)> <out.jpg>
 */
[ , $font, $icon, $out ] = $argv;
$W  = 1200;
$H  = 630;
$im = imagecreatetruecolor( $W, $H );
$ink   = imagecolorallocate( $im, 0x14, 0x12, 0x10 );
$gold  = imagecolorallocate( $im, 0xe0, 0xa9, 0x3b );
$cream = imagecolorallocate( $im, 0xf5, 0xef, 0xe3 );
$soft  = imagecolorallocate( $im, 0xd9, 0xcf, 0xbd );
imagefilledrectangle( $im, 0, 0, $W, $H, $ink );
imagefilledrectangle( $im, 0, 0, $W, 10, $gold );
imagefilledrectangle( $im, 0, $H - 10, $W, $H, $gold );

// Monogram on the left.
$m = imagecreatefrompng( $icon );
imagecopyresampled( $im, $m, 90, 165, 0, 0, 300, 300, imagesx( $m ), imagesy( $m ) );

// Text block on the right.
$x = 450;
imagettftext( $im, 26, 0, $x, 228, $gold, $font, 'THE' );
imagettftext( $im, 56, 0, $x - 4, 306, $cream, $font, 'BLACK HISTORY' );
imagettftext( $im, 56, 0, $x - 4, 380, $gold, $font, 'ROOM' );
imagefilledrectangle( $im, $x, 420, $x + 120, 425, $gold );
imagettftext( $im, 21, 0, $x, 470, $soft, $font, 'Powerful people, moments, struggles' );
imagettftext( $im, 21, 0, $x, 505, $soft, $font, 'and achievements from Black history' );

imagejpeg( $im, $out, 88 );
fwrite( STDERR, "wrote $out\n" );

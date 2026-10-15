<?php
/**
 * Draws the site icon (512 x 512 PNG): black square, muted-gold frame, cream "BHR" monogram in Cinzel Bold.
 * Usage: php make_icon.php <Cinzel.ttf> <out.png>      (needs PHP GD with FreeType; the WordPress image has it)
 */
[ , $font, $out ] = $argv;
$s  = 512;
$im = imagecreatetruecolor( $s, $s );
imagesavealpha( $im, true );
$ink   = imagecolorallocate( $im, 0x14, 0x12, 0x10 );
$gold  = imagecolorallocate( $im, 0xa8, 0x84, 0x4a );
$cream = imagecolorallocate( $im, 0xf5, 0xef, 0xe3 );
imagefilledrectangle( $im, 0, 0, $s, $s, $ink );

// Gold frame: outer rule and a thin inner rule.
imagesetthickness( $im, 14 );
imagerectangle( $im, 34, 34, $s - 35, $s - 35, $gold );
imagesetthickness( $im, 4 );
imagerectangle( $im, 62, 62, $s - 63, $s - 63, $gold );

// "BHR", sized to fit the inner frame and centred optically.
$text = 'BHR';
$size = 200;
do {
	$box = imagettfbbox( $size, 0, $font, $text );
	$w   = $box[2] - $box[0];
	$size -= 2;
} while ( $w > 330 && $size > 40 );
$h = $box[1] - $box[7];
$x = (int) ( ( $s - $w ) / 2 - $box[0] );
$y = (int) ( ( $s + $h ) / 2 - $box[1] ) + 4;
imagettftext( $im, $size, 0, $x, $y, $cream, $font, $text );

// Short gold underline below the letters.
imagefilledrectangle( $im, 196, $y + 26, $s - 197, $y + 33, $gold );

imagepng( $im, $out, 9 );
echo "wrote $out ({$size}pt)\n";

// Smaller PNGs next to it: site-icon-<px>.png (favicon 32, Apple touch 180, Android 192, Windows tile 270).
foreach ( array( 32, 180, 192, 270 ) as $px ) {
	$small = imagecreatetruecolor( $px, $px );
	imagecopyresampled( $small, $im, 0, 0, 0, 0, $px, $px, $s, $s );
	$file = preg_replace( '/\.png$/', "-{$px}.png", $out );
	imagepng( $small, $file, 9 );
	echo "wrote $file\n";
}

<?php
/**
 * Draws the site icon: black square, big heavy cream "BHR" filling most of the square (letters stretched taller so
 * they stay readable at 16-32 px in browser tabs), gold bar at the bottom.
 * One 1024 px master is drawn, then each size is resampled from it (smooth edges).
 * Usage: php make_icon.php <Cinzel.ttf> <out.png>   -> out.png (512) + out-16/-32/-180/-192/-270.png
 */
[ , $font, $out ] = $argv;

$M     = 1024;
$text  = 'BHR';
$size  = 400;
$bold  = 14;                                     // extra weight (drawn around a small circle)
$box   = imagettfbbox( $size, 0, $font, $text );
$tw    = $box[2] - $box[0] + 2 * $bold + 8;
$th    = $box[1] - $box[7] + 2 * $bold + 8;

// 1. The word on its own transparent canvas, cropped tight.
$word = imagecreatetruecolor( $tw, $th );
imagealphablending( $word, false );
imagefilledrectangle( $word, 0, 0, $tw, $th, imagecolorallocatealpha( $word, 0, 0, 0, 127 ) );
imagealphablending( $word, true );
$cream = imagecolorallocate( $word, 0xff, 0xf8, 0xea );
$x     = $bold + 4 - $box[0];
$y     = $bold + 4 - $box[7];
for ( $a = 0; $a < 360; $a += 20 ) {
	imagettftext( $word, $size, 0, (int) round( $x + $bold * cos( deg2rad( $a ) ) ), (int) round( $y + $bold * sin( deg2rad( $a ) ) ), $cream, $font, $text );
}
imagettftext( $word, $size, 0, $x, $y, $cream, $font, $text );

// 2. Master icon: black, word stretched into the area above the gold bar.
$m = imagecreatetruecolor( $M, $M );
imagefilledrectangle( $m, 0, 0, $M, $M, imagecolorallocate( $m, 0x14, 0x12, 0x10 ) );
$bar = (int) round( $M * 0.12 );
imagefilledrectangle( $m, 0, $M - $bar, $M, $M, imagecolorallocate( $m, 0xc9, 0xa2, 0x5c ) );
$pad = (int) round( $M * 0.035 );
imagealphablending( $m, true );
imagecopyresampled( $m, $word, $pad, (int) round( $M * 0.10 ), 0, 0, $M - 2 * $pad, (int) round( $M * 0.66 ), $tw, $th );

// 3. Sizes.
foreach ( array( 512 => $out, 16 => null, 32 => null, 180 => null, 192 => null, 270 => null ) as $px => $file ) {
	$file = $file ?: preg_replace( '/\.png$/', "-{$px}.png", $out );
	$im   = imagecreatetruecolor( $px, $px );
	imagecopyresampled( $im, $m, 0, 0, 0, 0, $px, $px, $M, $M );
	imagepng( $im, $file, 9 );
	echo "wrote $file\n";
}

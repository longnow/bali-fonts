# bali-fonts

This repository contains the latest release of three [Balinese Unicode](https://en.wikipedia.org/wiki/Balinese_(Unicode_block)) fonts: Vimala, Pustaka Bali, and Kadiri. These fonts are copyright [Aditya Bayu Perdana](https://www.behance.net/byabay), all rights reserved. The fonts are available under the [SIL OFL 1.1 license](LICENSE). Aditya Bayu Perdana designed the glyphs. [PanLex](https://panlex.org) assisted in developing the OpenType rules. Compiled fonts are in the [release](release) directory.

Vimala has a style similar to Bali Simbar, a non-Unicode font designed by I Made Suatjana that is popular in Bali. Pustaka Bali has a monoline (“sans-serif”) style that is optimized for screens. Kadiri is based on the handwriting of a lontar in the collection of Sugi Lanus, written by Pranda Madhe Kadiri. Below is a sample showing the Balinese greeting ᬒᬁᬲ᭄ᬯᬲ᭄ᬢ᭄ᬬᬲ᭄ᬢᬸ (_om swastyastu_), from top to bottom: Vimala, Pustaka Bali, Kadiri.

PanLex has designed a [Keyman keyboard](https://keyman.com/keyboards/aksarabali_panlex) that can be used with these fonts or other Balinese Unicode fonts.

<img src="sample.png" width="419" height="573" alt="font sample">

## Changelog

### Vimala

* 2.04 (March 6, 2020)
  * changed license to SIL OFL 1.1
  * changed shape of second-stack ra ligatures (wraps around left)
  * shapes such as gantungan wa and suku are completely enclosed
  * nail-like serifs in diagonal strokes (e.g. in cecek) are removed
  * made gantungan ta latik and ta murda mahaprana more compact
  * changed shape of ta, gantungan ta, and associated glyphs
  * changed shape of gantungan na, ca, wa
  * changed shape of pamada
  * added glyph for gantungan wa + gantungan wa
  * added long panti/pamada glyphs
* 2.03 (September 4, 2019)
  * allow combining marks above digits (for modre)
  * fix positioning of surang
  * fix positioning of combining marks above after second- and third-stack ra
  * correctly choose second-stack ra ligature after rerekan
* 2.02 (August 22, 2019)
  * fix rendering of independent vowels containing tedong when text is in NFD
  * fix spacing of gantungan nya + gantungan ya
* 2.01 (August 21, 2019)
  * rebalance bowl on ra repa (U+1B3A)
* 2.00 (August 16, 2019)
  * initial public release

### Pustaka Bali

* 2.04 (March 14, 2020)
  * fix several spacing issues in previous release
* 2.03 (March 6, 2020)
  * changed license to SIL OFL 1.1
  * changed shape of second-stack ra ligatures (wraps around left)
  * shapes such as gantungan wa and suku are completely enclosed
  * added glyph for gantungan wa + gantungan wa
  * added long panti/pamada glyphs
* 2.02 (September 4, 2019)
  * allow combining marks above digits (for modre)
  * fix positioning of surang
  * fix positioning of combining marks above after second- and third-stack ra
  * correctly choose second-stack ra ligature after rerekan
* 2.01 (August 22, 2019)
  * fix rendering of independent vowels containing tedong when text is in NFD
  * fix spacing of gantungan nya + gantungan ya
* 2.00 (August 16, 2019)
  * initial public release

### Kadiri

* 1.00 (March 14, 2020)
  * initial public release

## Compiling the fonts from source

To compile the fonts, you need [FontForge](https://fontforge.org/) Python bindings and [https://github.com/kblomqvist/yasha](yasha). To compile, run `script/compile`, which does the following:

1. Runs `script/dist_calc.py`, which reads glyph metrics from the `.sfd` files in `src/` and uses them to generate various portions of the feature file in `src/feature/include/` that perform spacing adjustments.
2. Runs `yasha` to generate each font's feature file (`features.fea`) in `src/<font>.ufo`.
3. Runs `script/compile.py` to compile each `.ufo` into `release/<font>.ttf`.

If you are on macOS, you can also run `script/preview`, which first runs `script/compile`, installs the compiled fonts for the current user, and relaunches TextEdit. This lets you test that the compiled fonts are working correctly.

# Modifying glyphs

If you modify, add, or remove glyphs, you should do so in the `.ufo` file located in `src/`. Once you have done so, be sure to save a copy of the new version as `src/<font>.sfd`. You can do this in FontForge by opening the `.ufo` file and choosing _Save As…_. The `.sfd` file must be kept up to date for glyph metrics because it is used in `script/dist_calc.py`. (It would be better to read metrics directly from `.ufo`, but we have encountered problems doing this consistently.)

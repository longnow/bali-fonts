#!/usr/bin/env python3

import sys, fontforge

def compile_font(name):
    font = fontforge.open("src/{0}.ufo".format(name))

    for g in font.glyphs():
        if g.glyphclass == "automatic":
            g.glyphclass = "noclass"

    font.generate("release/{0}.ttf".format(name))

if __name__ == '__main__':
    compile_font(sys.argv[1])

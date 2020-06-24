#!/usr/bin/env python3

import fontforge, os, re
from collections import defaultdict

include_path = "src/feature/include"
temp_file = "foo.fea.j2"

glyph_cache = {}

anchors = {
    "cons_conj": {
        "V": ["Anchor-3","Anchor9"],
        "P": ["Anchor-3","Anchor9"],
        "K": ["Anchor-2","Anchor9"],
    }
}

cons = ["uni1B13","uni1B14","uni1B15","uni1B16","uni1B17","uni1B18","uni1B19","uni1B1A","uni1B1A.2","uni1B1B","uni1B1B.2","uni1B1C","uni1B1D","uni1B1E","uni1B1F","uni1B20","uni1B21","uni1B22","uni1B23","uni1B24","uni1B25","uni1B26","uni1B27","uni1B28","uni1B29","uni1B2A","uni1B2B","uni1B2C","uni1B2D","uni1B2E","uni1B2F","uni1B30","uni1B31","uni1B32","uni1B33","uni1B45","uni1B46","uni1B47","uni1B48","uni1B49","uni1B4A","uni1B4B"]

cons_gempelan = [*cons, "uni1B27.conj","uni1B28.conj","uni1B31.conj","uni1B32.conj","uni1B48.conj","uni1B4A.conj"]

cons_ra = ["uni1B13.ra","uni1B14.ra","uni1B15.ra","uni1B16.ra","uni1B17.ra","uni1B18.ra","uni1B19.ra","uni1B1A.ra","uni1B1B.ra","uni1B1C.ra","uni1B1D.ra","uni1B1E.ra","uni1B1F.ra","uni1B20.ra","uni1B21.ra","uni1B22.ra","uni1B23.ra","uni1B24.ra","uni1B25.ra","uni1B26.ra","uni1B27.ra","uni1B28.ra","uni1B29.ra","uni1B2A.ra","uni1B2B.ra","uni1B2C.ra","uni1B2D.ra","uni1B2E.ra","uni1B2F.ra","uni1B30.ra","uni1B31.ra","uni1B32.ra","uni1B33.ra","uni1B45.ra","uni1B46.ra","uni1B47.ra","uni1B48.ra","uni1B49.ra","uni1B4A.ra","uni1B4B.ra","uni1B27.conj.ra","uni1B28.conj.ra","uni1B31.conj.ra","uni1B48.conj.ra"]

base_below = sorted([*cons_ra, "uni1B09","uni1B0A","uni1B0D","uni1B0E","uni1B10","uni1B11","uni1B12","uni1B3E","uni1B3F","uni1B44","uni1B52","uni1B53","uni1B5B","uni1B5E","uni1B5F"])

#mark_other = ["uni1B2D.conj.1"]

sukus = ["uni1B38.3","uni1B38.4","uni1B39.3","uni1B39.4","uni1B0E.conj","uni1B26.conj.u","uni1B26.conj.uu"]

skip_conj = set()

for base in ["uni1B18","uni1B1A","uni1B1F","uni1B20","uni1B23","uni1B24","uni1B26","uni1B27","uni1B28","uni1B2B","uni1B2D","uni1B2F","uni1B31","uni1B32","uni1B48","uni1B49","uni1B4A","uni1B27.conj","uni1B28.conj","uni1B31.conj","uni1B48.conj"]:
    skip_conj.update([(base,"uni1B3A")])

for base in ["uni1B13","uni1B14","uni1B15","uni1B16","uni1B17","uni1B19","uni1B1B","uni1B1C","uni1B1D","uni1B1E","uni1B21","uni1B22","uni1B25","uni1B29","uni1B2A","uni1B2C","uni1B2E","uni1B30","uni1B33","uni1B45","uni1B46","uni1B47","uni1B4B"]:
    skip_conj.update([(base,"uni1B3A.2")])

mark_below = [
    { "glyph": "uni1B0D.conj" },
    { "glyph": "uni1B0E.conj" },
    { "glyph": "uni1B13.conj" },
    { "glyph": "uni1B14.conj" },
    { "glyph": "uni1B15.conj" },
    { "glyph": "uni1B16.conj.1" },
    { "glyph": "uni1B16.conj.2" },
    { "glyph": "uni1B17.conj" },
    { "glyph": "uni1B18.conj" },
    { "glyph": "uni1B19.conj.1" },
    { "glyph": "uni1B19.conj.2" },
    { "glyph": "uni1B1A.conj" },
    { "glyph": "uni1B1B.conj" },
    { "glyph": "uni1B1C.conj", "anchor": "VPK" },
    { "glyph": "uni1B1D.conj" },
    { "glyph": "uni1B1E.conj" },
    { "glyph": "uni1B1F.conj" },
    { "glyph": "uni1B20.conj" },
    { "glyph": "uni1B21.conj.1" },
    { "glyph": "uni1B21.conj.2" },
    { "glyph": "uni1B22.conj" },
    { "glyph": "uni1B23.conj" },
    { "glyph": "uni1B23.conj.ra" },
    { "glyph": "uni1B23.conj.ya" },
    { "glyph": "uni1B23.conj.ya.u" },
    { "glyph": "uni1B23.conj.ya.uu" },
    { "glyph": "uni1B24.conj" },
    { "glyph": "uni1B25.conj" },
    { "glyph": "uni1B26.conj" },
    { "glyph": "uni1B26.conj.u" },
    { "glyph": "uni1B26.conj.uu" },
    { "glyph": "uni1B26.conj.ya" },
    { "glyph": "uni1B26.conj.ya.u" },
    { "glyph": "uni1B26.conj.ya.uu" },
    { "glyph": "uni1B29.conj.1" },
    { "glyph": "uni1B29.conj.2" },
    { "glyph": "uni1B2A.conj" },
    { "glyph": "uni1B2B.conj" },
    { "glyph": "uni1B2C.conj.1" },
    { "glyph": "uni1B2C.conj.u.1" },
    { "glyph": "uni1B2C.conj.uu.1" },
    #{ "glyph": "uni1B2D.conj.1" },
    { "glyph": "uni1B2D.conj.wa" },
    { "glyph": "uni1B2D.conj.ya" },
    { "glyph": "uni1B2D.conj.ya.u" },
    { "glyph": "uni1B2D.conj.ya.uu" },
    { "glyph": "uni1B2E.conj.1" },
    { "glyph": "uni1B2E.conj.2" },
    { "glyph": "uni1B2F.conj.1" },
    { "glyph": "uni1B2F.conj.ra" },
    { "glyph": "uni1B2F.conj.ya" },
    { "glyph": "uni1B2F.conj.ya.u" },
    { "glyph": "uni1B2F.conj.ya.uu" },
    { "glyph": "uni1B30.conj" },
    { "glyph": "uni1B32.conj" },
    { "glyph": "uni1B33.conj" },
    { "glyph": "uni1B38" },
    { "glyph": "uni1B39" },
    { "glyph": "uni1B3A" },
    { "glyph": "uni1B3A.2" },
    { "glyph": "uni1B3C.blw" },
    { "glyph": "uni1B45.conj" },
    { "glyph": "uni1B46.conj", "anchor": "VPK" },
    { "glyph": "uni1B47.conj" },
    { "glyph": "uni1B49.conj" },
    { "glyph": "uni1B49.conj.ra" },
    { "glyph": "uni1B49.conj.ya" },
    { "glyph": "uni1B49.conj.ya.u" },
    { "glyph": "uni1B49.conj.ya.uu" },
    { "glyph": "uni1B4B.conj", "anchor": "VPK" },
]

mark_below2 = [
    { "glyph": "uni1B2D.conj.3" },
    { "glyph": "uni1B2D.conj.3.wa" },
    { "glyph": "uni1B2D.conj.3.ya" },
    { "glyph": "uni1B2D.conj.3.ya.u" },
    { "glyph": "uni1B2D.conj.3.ya.uu" },
    { "glyph": "uni1B2D.conj.4", "only": "V" },
    { "glyph": "uni1B2E.conj.3" },
    { "glyph": "uni1B3A.3" },
    { "glyph": "uni1B3A.4", "only": "V" },
]

def lookup_anchor(anchor_spec):
    return anchors[anchor_spec[0]][anchor_spec[1]]

def get_glyph(font, name):
    key = "{0}_{1}".format(font.fontname, name)

    try:
        return glyph_cache[key]
    except KeyError:
        try:
            font.selection.select(name)
            glyph = list(font.selection.byGlyphs)[0]
            font.selection.none()
            glyph_cache[key] = glyph
            return glyph
        except:
            return None

def get_anchor_x(glyph, anchor_name):
    for anchor in glyph.anchorPoints:
        if anchor[0] == anchor_name:
            return int(anchor[2])

    return None

def print_width(font, anchor_spec, bases, msg = None):
    if msg:
        print("{0}:\n".format(msg))

    anchor = lookup_anchor(anchor_spec)

    for base in bases:
        glyph = get_glyph(font, base)
        print("  pos base [\\{0} ] <anchor {1} 0> mark @{2};".format(glyph.glyphname, glyph.width, anchor[1]))

    print()

def print_left2_diff(f, font, mark, bases, lookup, rules, seen):
    glyph = get_glyph(font, mark)
    mark_x = -1 * int(glyph.left_side_bearing)

    key = "left2_{0}".format(mark_x)

    if key in seen:
        mark = "\\" + mark
        seen[key]["marks"].append(mark)
        return False
    else:
        table = []
        seen_rec = {}
        seen_bases = []

        for base in bases:
            base_glyph = get_glyph(font, base)
            diff = mark_x - base_glyph.width

            if diff > 0:
                base = "\\" + base
                seen_bases.append(base)

                if diff in seen_rec:
                    seen_rec[diff][0].append(base)
                else:
                    rec = [[base], diff]
                    table.append(rec)
                    seen_rec[diff] = rec

        if len(table):
            print("# {0} left2".format(mark), file=f)
            print("lookup {0} {{\n  lookupflag 0;".format(lookup), file=f)

            for rec in table:
                print("  pos [{0} ] <{1} 0 {1} 0>;".format(" ".join(rec[0]), rec[1]), file=f)

            print("}} {0};".format(lookup), file=f)
            print(file=f)

            mark = "\\" + mark
            rule = { "marks": [mark], "lookup": lookup, "bases": seen_bases }
            seen[key] = rule
            rules["left2"].append(rule)

            return True
        else:
            return False

def print_left_rules(f, rules):
    if len(rules):
        for rule in rules:
            marks = " ".join(rule["marks"])
            bases = " ".join(rule["bases"])

            print("  pos @any_below [{0} ]' lookup {1} @conj_below_simple [{2} ];".format(bases, rule["lookup"], marks), file=f)

def print_anchor_left_diff(f, font, anchor_spec, mark, bases, lookup, rules, seen):
    glyph = get_glyph(font, mark)

    if anchor_spec:
        anchor = lookup_anchor(anchor_spec)
        mark_x = -1 * (int(glyph.left_side_bearing) - get_anchor_x(glyph, anchor[0]))
        key = "anchor_left_{0}_{1}".format(anchor[1], mark_x)
    else:
        mark_x = -1 * int(glyph.left_side_bearing)
        key = "anchor_left_none_{0}".format(mark_x)

    if key in seen:
        mark = "\\" + mark
        seen[key]["marks"].append(mark)
        return False
    else:
        table = []
        seen_rec = {}
        seen_bases = []

        for base in bases:
            if (base,mark) in skip_conj:
                continue

            base_glyph = get_glyph(font, base)

            if anchor_spec:
                base_x = get_anchor_x(base_glyph, anchor[0])
            else:
                base_x = base_glyph.width

            if base_x:
                diff = mark_x - base_x

                if diff > 0:
                    base = "\\" + base
                    seen_bases.append(base)

                    if diff in seen_rec:
                        seen_rec[diff][0].append(base)
                    else:
                        rec = [[base], diff]
                        table.append(rec)
                        seen_rec[diff] = rec

        if len(table):
            print("# {0} left".format(mark), file=f)
            print("lookup {0} {{\n  lookupflag 0;".format(lookup), file=f)

            for rec in table:
                print("  pos [{0} ] <{1} 0 {1} 0>;".format(" ".join(rec[0]), rec[1]), file=f)

            print("}} {0};".format(lookup), file=f)
            print(file=f)

            mark = "\\" + mark
            rule = { "marks": [mark], "lookup": lookup, "bases": seen_bases }
            seen[key] = rule
            rules["left"].append(rule)

            return True
        else:
            return False

def print_anchor_left_rules(f, rules):
    if len(rules):
        for rule in rules:
            marks = " ".join(rule["marks"])
            bases = " ".join(rule["bases"])

            print("  pos @any_below [{0} ]' lookup {1} [{2} ];".format(bases, rule["lookup"], marks), file=f)
            #print("  pos \\uni1B44 \\uni200C @cons_gempelan' lookup {0} [{1} ];".format(rule[1], glyphs), file=f)

def print_anchor_right_diff(f, font, anchor_spec, mark, bases, lookup, rules, seen):
    anchor = lookup_anchor(anchor_spec)

    mark_glyph = get_glyph(font, mark)
    mark_x = -1 * get_anchor_x(mark_glyph, anchor[0]) - max(mark_glyph.right_side_bearing, 0)

    key = "anchor_right_{0}_{1}".format(anchor[1], mark_x)

    if key in seen:
        mark = "\\" + mark
        seen[key]["marks"].append(mark)
        seen[seen[key]["mkmk_key"]]["marks"].append(mark)
        return False
    else:
        table = []
        seen_rec = {}
        seen_bases = []

        for base in bases:
            if (base,mark) in skip_conj:
                continue

            base_glyph = get_glyph(font, base)
            base_x = get_anchor_x(base_glyph, anchor[0])

            if base_x:
                diff = int(mark_x + base_x - base_glyph.width)

                if diff > 0:
                    base = "\\" + base
                    seen_bases.append(base)
                    if diff in seen_rec:
                        seen_rec[diff][0].append(base)
                    else:
                        rec = [[base], diff]
                        table.append(rec)
                        seen_rec[diff] = rec

        if len(table):
            print("# {0} right".format(mark), file=f)
            print("lookup {0} {{\n  lookupflag 0;".format(lookup), file=f)

            for rec in table:
                print("  pos [{0} ] {1};".format(" ".join(rec[0]), rec[1]), file=f)

            print("}} {0};".format(lookup), file=f)
            print(file=f)

            mark = "\\" + mark
            mkmk_key = frozenset(seen_bases)
            rule = { "marks": [mark], "lookup": lookup, "bases": seen_bases, "mkmk_key": mkmk_key }
            seen[key] = rule
            rules["right"].append(rule)

            if mkmk_key in seen:
                seen[mkmk_key]["marks"].append(mark)
            else:
                rule = { "marks": [mark], "bases": sorted(mkmk_key) }
                seen[mkmk_key] = rule
                rules["mkmk"].append(rule)

            return True
        else:
            return False

def print_anchor_right_rules(f, rules):
    if len(rules):
        for rule in rules:
            marks = " ".join(rule["marks"])
            bases = " ".join(rule["bases"])
            print("  pos [{0} ]' lookup {1} [{2} ] @GDEF_Base_Simple @mark_below_with_spacing;".format(bases, rule["lookup"], marks), file=f)
            print("  pos [{0} ]' lookup {1} [{2} ] @mark_below @GDEF_Base_Simple @mark_below_with_spacing;".format(bases, rule["lookup"], marks), file=f)
            print("  pos [{0} ]' lookup {1} [{2} ] @base_below_simple_or_conj_right;".format(bases, rule["lookup"], marks), file=f)
            print("  pos [{0} ]' lookup {1} [{2} ] @mark_below @base_below_simple_or_conj_right;".format(bases, rule["lookup"], marks), file=f)
            print(file=f)

def print_mkmk_rules(f, rules, anchor_name):
    if len(rules):
        for rule in rules:
            if len(rule["marks"]):
                print("  pos [{0} ]".format(" ".join(rule["bases"])), file=f)
                print("    mark [{0} ]' <anchor 0 0> mark @{1}';\n".format(" ".join(rule["marks"]), anchor_name), file=f)

def print_suku_spacing(f, font, bases, code):
    suku_sets = defaultdict(lambda: [])
    base_rules = []
    mark1_rules = []
    seen = {}

    for suku in sukus:
        suku_glyph = get_glyph(font, suku)
        suku_width = int(-1 * suku_glyph.right_side_bearing)

        suku = "\\" + suku
        suku_sets[suku_width].append(suku)

    for suku_width, suku_list in suku_sets.items():
        suku_names = " ".join(sorted(suku_list))

        for base in base_below:
            base_glyph = get_glyph(font, base)
            diff = int(suku_width - base_glyph.left_side_bearing)
            if diff > 0:
                key = "base_{0}_{1}".format(suku_names, diff)
                base = "\\" + base

                if key in seen:
                    seen[key]["bases"].append(base)
                else:
                    rule = { "suku": suku_names, "bases": [base], "diff": diff }
                    seen[key] = rule
                    base_rules.append(rule)

        for rec in mark_below:
            if "anchor" in rec and re.search(code, rec["anchor"]):
                anchor = lookup_anchor(["cons_conj",code])
            else:
                anchor = None

            mark = rec["glyph"]
            mark_glyph = get_glyph(font, mark)
            mark_width = mark_glyph.left_side_bearing
            key = "mark_{0}_{1}".format(suku_names, mark_width)

            if key in seen:
                seen[key]["marks"].append("\\" + mark)
            else:
                bases_to_correct = []

                for base in bases:
                    base_glyph = get_glyph(font, base)

                    if anchor:
                        mark_x = mark_width - get_anchor_x(mark_glyph, anchor[0])
                        base_x = get_anchor_x(base_glyph, anchor[0])
                        diff = suku_width - (base_x + mark_x)
                    else:
                        diff = suku_width - (base_glyph.width + mark_width)

                    if diff > 0:
                        bases_to_correct.append("\\" + base)

                if len(bases_to_correct):
                    rule = { "suku": suku_names, "bases": bases_to_correct, "marks": ["\\" + mark], "diff": suku_width }
                    seen[key] = rule
                    mark1_rules.append(rule)

    for rule in base_rules:
        bases = " ".join(rule["bases"])
        print("  pos [{0} ] [{1} ]' <{2} 0 {2} 0>;".format(rule["suku"], bases, rule["diff"]), file=f)

    for rule in mark1_rules:
        bases = " ".join(rule["bases"])
        marks = " ".join(rule["marks"])
        print("  pos [{0} ] [{1} ]' <{2} 0 {2} 0> [{3} ];".format(rule["suku"], bases, rule["diff"], marks), file=f)

def print_font_calcs(fontpath, name, code):
    if name == "vimala":
        filter_cons = set(["uni1B1A.2"])
    else:
        filter_cons = set()

    font_cons = [x for x in cons if x not in filter_cons]
    font_cons_gempelan = [x for x in cons_gempelan if x not in filter_cons]


    font = fontforge.open(fontpath)

    with open("{0}/suku_spacing_{1}.fea.j2".format(include_path, name), "w") as f:
        print_suku_spacing(f, font, font_cons, code)

    rules = { "left": [], "left2": [], "right": [], "mkmk": [] }
    seen = {}

    with open("{0}/left_right_{1}.fea.j2".format(include_path, name), "w") as f:
        idx = 1
        for rec in mark_below:
            if "anchor" in rec and re.search(code, rec["anchor"]):
                anchor_spec = ["cons_conj",code]
            else:
                anchor_spec = None

            if print_anchor_left_diff(f, font, anchor_spec, rec["glyph"], font_cons_gempelan, "SinglePositioninglookup1_" + str(idx), rules, seen):
                idx = idx + 1

            if anchor_spec:
                if print_anchor_right_diff(f, font, anchor_spec, rec["glyph"], font_cons_gempelan, "SinglePositioninglookup1_" + str(idx), rules, seen):
                    idx = idx + 1

    with open("{0}/left2_{1}.fea.j2".format(include_path, name), "w") as f:
        idx = 1
        for rec in mark_below2:
            if "only" in rec and not re.search(code, rec["only"]):
                continue

            if print_left2_diff(f, font, rec["glyph"], font_cons_gempelan, "SinglePositioninglookup5_" + str(idx), rules, seen):
                idx = idx + 1

    with open("{0}/left_rules_{1}.fea.j2".format(include_path, name), "w") as f:
        print_anchor_left_rules(f, rules["left"])

    with open("{0}/right_rules_{1}.fea.j2".format(include_path, name), "w") as f:
        print_anchor_right_rules(f, rules["right"])

    with open("{0}/mkmk_wide_conjunct_{1}.fea.j2".format(include_path, name), "w") as f:
        print_mkmk_rules(f, rules["mkmk"], "Anchor8")

    with open("{0}/left2_rules_{1}.fea.j2".format(include_path, name), "w") as f:
        print_left_rules(f, rules["left2"])

if __name__ == '__main__':
    print_font_calcs("src/Vimala.sfd", "vimala", "V")
    print_font_calcs("src/PustakaBali.sfd", "pustaka", "P")
    print_font_calcs("src/Kadiri.sfd", "kadiri", "K")

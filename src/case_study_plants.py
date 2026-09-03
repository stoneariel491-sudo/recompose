"""The case study's own defect classes and instruments, wired into the planting harness.

This is the adapter, not the harness. `plant.py` knows nothing about LaTeX, about Rudin, or
about this project's tools; it knows a Defect is something you can inject once and an Instrument
is something you can run and question. Everything specific lives here, so a second book needs a
second file of this shape and nothing else.

WHAT IS PLANTED. Six classes, chosen because each is a mechanism the reading has actually met -
five of them repeatedly, over four waves of twelve readers - and because each has an instrument
somewhere that ought to see it. A class nobody claims to cover is worth planting too, and the
harness reports an empty union as exactly that.

WHAT IS NOT MEASURED HERE, and it is half the instruments. Anything that reads the PLATE - the
scan itself - cannot run inside a temporary copy without carrying six hundred megabytes of
images into it, so `indents.py`, `margins.py` and `left_edges.py` are absent from this matrix.
Their absence is a gap in the measurement and not a judgement on them; `margins.py` in
particular saw two faults last wave that the tool named for them did not.

**The instruments here are the ones that read the SOURCE**, and the source is where every one of
these six defects lives.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plant import Defect, Instrument

ROOT = os.path.join(os.path.expanduser("~"), "dev", "active", "rudin-recompose")

# Only what the source-reading instruments open. The plates are deliberately left out - see the
# module docstring - and so is the built PDF, which no instrument here reads.
INCLUDE = ["tex/pages", "tex/rudinstyle.sty", "tools", "ERRATA.md"]

# Enough trials that a single unlucky page cannot decide a row, few enough that the whole matrix
# runs in a couple of minutes. Each trial plants ONE defect on a different page.
TRIALS = 6

# The pages plants are placed on, spread across the book so that a class is not measured on one
# chapter's habits. Chosen for having a display, a page-opening and a CHECK line between them.
PAGES = [66, 96, 130, 168, 209, 244, 262, 290]


def _page_path(root, page):
    return os.path.join(root, "tex", "pages", "p{:03d}.tex".format(page))


def _lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def _write(path, lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


DISPLAY_END = re.compile(r"^\s*(\\\]|\\end\{(equation\*?|align\*?|flalign\*?|gather\*?)\})")


def _first_content(lines):
    for i, l in enumerate(lines):
        if l.strip() and not l.lstrip().startswith("%"):
            return i
    return None


def plant_after_display(root, trial):
    """A blank line after a display where the source has none: LaTeX then indents what runs on."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    for i in range(len(lines) - 1):
        if DISPLAY_END.match(lines[i]) and lines[i + 1].strip() \
                and not lines[i + 1].lstrip().startswith(("%", "\\")):
            lines.insert(i + 1, "")
            _write(path, lines)
            return [(path, i + 2)]
    return []


def plant_run_on(root, trial):
    """The mirror: a blank line after a display REMOVED, so a new paragraph runs on."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    for i in range(len(lines) - 2):
        if DISPLAY_END.match(lines[i]) and not lines[i + 1].strip() \
                and lines[i + 2].strip() and not lines[i + 2].lstrip().startswith(("%", "\\")):
            del lines[i + 1]
            _write(path, lines)
            return [(path, i + 1)]
    return []


def plant_suppressed_join(root, trial):
    """A \\noindent at a page opening that does not want one."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    i = _first_content(lines)
    if i is None or lines[i].lstrip().startswith("\\noindent"):
        return []
    lines[i] = "\\noindent " + lines[i].lstrip()
    _write(path, lines)
    return [(path, i + 1)]


def plant_header_number(root, trial):
    """A digit changed inside a CHECK line, so the header claims what the body does not say."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    for i, l in enumerate(lines):
        if l.lstrip().startswith("%") and "CHECK:" in l and re.search(r"\d", l):
            lines[i] = re.sub(r"(\d)", lambda m: str((int(m.group(1)) + 3) % 10), l, count=1)
            _write(path, lines)
            return [(path, i + 1)]
    return []


def plant_sign_flip(root, trial):
    """An inequality reversed in the body. The header may or may not name it, which is the point."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    for i, l in enumerate(lines):
        if l.lstrip().startswith("%"):
            continue
        if "\\leq" in l:
            lines[i] = l.replace("\\leq", "\\geq", 1)
            _write(path, lines)
            return [(path, i + 1)]
    return []


def plant_lost_emphasis(root, trial):
    """An \\emph stripped: the defined term stops being marked."""
    page = PAGES[trial % len(PAGES)]
    path = _page_path(root, page)
    if not os.path.exists(path):
        return []
    lines = _lines(path)
    for i, l in enumerate(lines):
        if l.lstrip().startswith("%"):
            continue
        m = re.search(r"\\emph\{([^{}]+)\}", l)
        if m:
            lines[i] = l[:m.start()] + m.group(1) + l[m.end():]
            _write(path, lines)
            return [(path, i + 1)]
    return []


DEFECTS = [
    Defect("AFTER-DISPLAY", plant_after_display,
           "a blank line after a display, so a line the plate runs on is indented"),
    Defect("RUN-ON", plant_run_on,
           "a blank line removed, so a paragraph the plate opens runs on"),
    Defect("SUPPRESSED-JOIN", plant_suppressed_join,
           "a noindent at a page opening that does not want one"),
    Defect("HEADER-NUMBER", plant_header_number,
           "a digit changed in a CHECK line, so the header claims what the body denies"),
    Defect("SIGN-FLIP", plant_sign_flip,
           "an inequality reversed in the body"),
    Defect("LOST-EMPHASIS", plant_lost_emphasis,
           "an emph stripped from a defined term"),
]


def _page_of(path):
    return int(os.path.basename(path)[1:-4])


def _runner(script, ranged=True):
    def run(root):
        cmd = [sys.executable, os.path.join(root, "tools", script)]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=root,
                           encoding="utf-8", errors="replace", timeout=600)
        return (r.stdout or "") + (r.stderr or "")
    return run


def _names_page(out, path, line):
    """Did the output name this page? The instruments report pages, not lines."""
    p = _page_of(path)
    return bool(re.search(r"\bp\.?\s?{}\b".format(p), out)
                or re.search(r"\bpage {}\b".format(p), out))


INSTRUMENTS = [
    Instrument("para_census", _runner("para_census.py"), _names_page),
    Instrument("header_vs_body", _runner("header_vs_body.py"), _names_page),
    Instrument("eqnumbers", _runner("eqnumbers.py"), _names_page),
    Instrument("record_check", _runner("record_check.py"), _names_page),
    Instrument("limits_scope", _runner("limits_scope.py"), _names_page),
]

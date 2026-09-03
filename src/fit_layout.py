"""Fit a book's typographic grammar to its own scanned leaves.

STAGE 2 OF THE PIPELINE, ASKED TO DERIVE ITS OWN MEASUREMENTS. Today that stage measures
whatever a person thinks to measure, which makes it the one stage that cannot run alone. A
layout is a small grammar - a text block, a measure, a leading, an indent quantum, a set of
block margins - and fitting a grammar to observations is well posed. E06 states what this is
predicted to recover and what it is predicted to miss.

EVERYTHING COMES OUT AS A FRACTION OF THE LEAF, so that scan resolution cancels and the result
survives a change of scanner. Points come later, from the trim, and the trim is the one thing
this cannot recover: a leaf of ink says nothing about the paper it was cut from.

WHAT IT IS NOT GIVEN. Not the page numbers, not which leaves are body and which are front
matter, not the trim, not the answer. Leaves are chosen by ink fraction alone, because a real
ingest has nothing else to choose by.

    python src/fit_layout.py <directory of page images> [--sample 40] [--json]
"""

import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from geometry import deskew, ink_rows, margins

# A leaf that is mostly ink is a plate, not type; one that is nearly empty is a part title or a
# blank. Neither carries the grammar. The bounds are wide on purpose - this is a filter for
# leaves that cannot possibly be body text, not a classifier.
INK_LOW = 0.02
INK_HIGH = 0.11

# A body leaf is a leaf with many lines. A chapter opening has a drop and a title and fewer.
MIN_LINES = 20


def leaf_lines(path):
    """[(top, bottom, left, right)] for one leaf, plus its height and width."""
    from PIL import Image
    import numpy as np
    a = np.array(Image.open(path).convert("L"))
    rows = ink_rows(a, head_band=0.0, min_height=8)
    return rows, a.shape[0], a.shape[1], float((a < 128).mean())


def body_leaves(paths, want):
    """Leaves that could be body text, chosen by ink fraction and line count alone."""
    out = []
    for p in paths:
        rows, H, W, ink = leaf_lines(p)
        if INK_LOW <= ink <= INK_HIGH and len(rows) >= MIN_LINES:
            out.append((p, rows, H, W))
        if len(out) >= want:
            break
    return out


def running_head(rows, H):
    """Drop a leading band that stands alone above a gap much larger than the line pitch.

    THE HEAD IS NOT A FRACTION OF THE LEAF, IT IS A GAP. Cutting a fixed 7.5 per cent off the
    top - which one tool in the case study does - throws away a body line on any book whose
    head sits higher, and keeps the head on any book whose head sits lower. The head is the
    band that has open space under it, and open space is measurable.
    """
    if len(rows) < 4:
        return rows
    gaps = sorted(rows[i + 1][0] - rows[i][1] for i in range(len(rows) - 1))
    typical = gaps[len(gaps) // 2]
    if rows[1][0] - rows[0][1] > 3 * max(typical, 1):
        return rows[1:]
    return rows


def fit_measure(leaves):
    """(left edge, right edge, measure), as fractions of the leaf's width.

    THE BODY IS SET JUSTIFIED, so its right edge is a hard edge repeated on every full line of
    every leaf, and the left edge likewise except where a paragraph indents. Both are taken as
    a high quantile over many leaves rather than an extremum, because a single line of
    mathematics can reach outside the measure on either side and one such line would set the
    answer on its own.
    """
    import numpy as np
    per_leaf = []
    for _, rows, H, W in leaves:
        body = running_head(rows, H)
        if len(body) < MIN_LINES:
            continue
        lefts = [l / W for _, _, l, _ in body]
        rights = [r / W for _, _, _, r in body]
        per_leaf.append((float(np.percentile(lefts, 10)),
                         float(np.percentile(rights, 90))))
    if not per_leaf:
        return None
    # WITHIN A LEAF FIRST, ACROSS LEAVES SECOND, and the order is the whole correction.
    #
    # The first version pooled every line of every leaf and took one pair of percentiles. That
    # returned a measure of 0.8785 of the leaf against a true 0.8333 - wider than the justified
    # span of ANY single leaf, which was the tell. The leaves are not registered to a common
    # origin: their body margins vary by sixty pixels across this sample while their justified
    # spans agree to one per cent. Pooling positions from unregistered leaves measures the
    # UNION of their text blocks and calls it the block.
    #
    # THE PRINCIPLE, and it is general: a layout parameter that is a DIFFERENCE - a measure, a
    # quantum, a pitch - is a within-leaf quantity and must be computed inside a leaf before
    # anything is pooled. Only a POSITION needs registration, and a position is exactly what
    # this stage cannot recover, since the leaf is not the trim.
    lefts, rights = zip(*per_leaf)
    left, right = float(np.median(lefts)), float(np.median(rights))
    return left, right, right - left


def fit_pitch(leaves):
    """Baseline pitch as a fraction of the leaf's height.

    THE STRONGEST PERIODICITY ON A PAGE OF TYPE, and taken from consecutive row tops rather
    than from a transform: the rows are already segmented, and a median of first differences is
    robust to the displays and blank lines that a transform would have to be told about.
    """
    from collections import Counter
    steps = []
    for _, rows, H, _ in leaves:
        body = running_head(rows, H)
        steps += [(body[i + 1][0] - body[i][0]) / H for i in range(len(body) - 1)]
    steps = [x for x in steps if x > 0]
    if not steps:
        return None
    # THE MODE, NOT A TRUNCATED MEDIAN. The first version took the median of the smallest
    # seventy per cent, meaning to exclude the larger gaps a display or a paragraph break
    # opens - which is the thirty-fifth percentile of the whole and is biased low BY
    # CONSTRUCTION. Measured against a known pitch it came out 12.7 per cent short, and the
    # bias was in the estimator rather than in the page. The pitch is the commonest step, and
    # a mode does not care what the tail contains.
    hist = Counter(round(x, 4) for x in steps)
    return float(max(hist.items(), key=lambda kv: kv[1])[0])


def fit_block(leaves):
    """(top, bottom, height) of the text block, as fractions of the leaf's height.

    THE FOOT IS TAKEN OVER THE MAXIMUM AND THE HEAD OVER THE MINIMUM, across leaves. A page's
    ink ends where its last line ends, not where the block does, so any one leaf understates
    the block; only a leaf that happens to run full measures it. E06 predicts this still comes
    out short, and says so before the run.
    """
    import numpy as np
    tops, spans = [], []
    for _, rows, H, _ in leaves:
        body = running_head(rows, H)
        if len(body) < MIN_LINES:
            continue
        tops.append(body[0][0] / H)
        spans.append((body[-1][1] - body[0][0]) / H)
    if not tops:
        return None
    # THE SPAN IS TAKEN WITHIN A LEAF AND THEN MAXIMISED, for the same reason the measure is.
    # The first version took the minimum top and the maximum foot ACROSS leaves, which on
    # unregistered leaves is the union of their blocks and reported the block 0.5 per cent too
    # LONG - where a page's ink, ending at its last line, should have made it short. Two errors
    # of opposite sign nearly cancelling is the worst way for a number to be right.
    top = float(np.median(tops))
    return top, top + max(spans), max(spans)


def fit_quantum(leaves, left_edge):
    """The indent quantum as a fraction of the measure, or None.

    THIS IS THE HARD ONE AND E06 SAYS SO IN ADVANCE. A histogram of line starts carries the
    body's margin, every open block's margin and every paragraph indent at once, and that
    superposition has already refuted three instruments in this project.

    What is done differently here: the leaf is DESKEWED first, so that a margin is a spike
    rather than a smear; the candidates are the gaps between adjacent margin clusters rather
    than the clusters themselves, because an indent is a DIFFERENCE and only the differences
    are shared between a body paragraph and a block's; and the answer is the gap that recurs
    across leaves, since a book has one quantum and a page has many accidents.
    """
    import numpy as np
    from collections import defaultdict

    # THE LEFT INK EDGE IS NOT THE MARGIN. It is the margin plus the first glyph's left side
    # bearing, and that varies by glyph: a T, an x, an L and a u flush at one margin land at
    # four different ink edges. Two readers hit this independently on one page of the case
    # study, where four lines of a proof measured below a range the header claimed for it.
    #
    # The spread is measured here rather than assumed, because it is a property of the face and
    # the size: within the densest cluster of line starts on a leaf - lines that ARE at one
    # margin - the spread of ink edges is the side bearing's own noise. It sets a floor below
    # which no margin difference recovered from ink can be believed.
    floors = []
    for _, rows, H, W in leaves:
        body = running_head(rows, H)
        if len(body) < MIN_LINES:
            continue
        xs = [l for _, _, l, _ in body]
        ys = [(t + b) / 2 for t, b, _, _ in body]
        flat = np.asarray(deskew(xs, ys))
        base = np.percentile(flat, 20)
        near = flat[np.abs(flat - base) < 0.02 * W]
        if len(near) >= 5:
            floors.append(float(np.percentile(near, 90) - np.percentile(near, 10)) / W)
    floor = float(np.median(floors)) if floors else 0.005

    seen = defaultdict(set)
    total = 0
    for k, (_, rows, H, W) in enumerate(leaves):
        body = running_head(rows, H)
        if len(body) < MIN_LINES:
            continue
        xs = [l for _, _, l, _ in body]
        ys = [(t + b) / 2 for t, b, _, _ in body]
        flat = deskew(xs, ys)
        cl = margins(flat, tol=0.004 * W, cluster=2)
        # EVERY PAIR, NOT ONLY ADJACENT ONES. An indent is a difference between a paragraph's
        # first line and its own block's margin, and those two need not be neighbours in a
        # sorted list of clusters - a block's margin can sit between them.
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                g = (cl[j] - cl[i]) / W
                if g > floor:
                    seen[round(g / 0.005) * 0.005].add(k)
                    total += 1
    if not seen:
        return None
    # THE SUPPORT IS COUNTED IN LEAVES, NOT IN GAPS, and that is the whole correction. Counting
    # gaps, the first version returned 0.0100 of the leaf against a true quantum of 0.059 - it
    # found the small spacings between neighbouring clusters, which are noise and which recur
    # many times on a single crowded page. A BOOK HAS ONE QUANTUM AND A PAGE HAS MANY
    # ACCIDENTS: block margins move from page to page, the quantum does not, so the quantity
    # to maximise is how many DIFFERENT leaves show a gap, and ties break toward the larger.
    best = max(seen.items(), key=lambda kv: (len(kv[1]), kv[0]))
    return best[0], len(best[1]), total, floor


def fit_quantum_by_paragraph(leaves, measure):
    """The indent quantum, taken from paragraphs identified by their RIGHT edge.

    E06 FAILED THIS QUANTITY AND NAMED THE NEXT MOVE. Recovering the quantum from a histogram of
    left edges asks the left edge to do two jobs at once - to say which lines are paragraph
    openings and to say how far they are indented - and the side bearing, a quarter of the
    quantum here, corrupts both. The obstacle is not the clustering. It is that the measurement
    and the identification came from the same evidence.

    THE RIGHT EDGE IDENTIFIES A PARAGRAPH AND KNOWS NOTHING ABOUT INDENTS. The body is set
    justified, so every line but a paragraph's last reaches the measure; a line that falls short
    ENDS a paragraph, and the line after it BEGINS one. That is a hard signal, it is independent
    of the quantity being measured, and it costs nothing.

    THEN THE SIDE BEARING AVERAGES AWAY INSTEAD OF BEING FILTERED. Each pair contributes the
    opening's edge less its own paragraph's margin, and both edges carry a side bearing drawn
    from the same distribution of initial glyphs. The difference is unbiased; only its variance
    is inflated. Over many pairs the standard error falls as the square root, so what is a
    hopeless quarter-quantum on one paragraph is a small fraction of one over two hundred.

    A MEAN IS USED AND NOT A MODE, deliberately, for the same reason: a mode of a noisy quantity
    keeps the noise, an average of an unbiased one removes it.
    """
    import numpy as np
    SHORT = 0.85          # of the measure: a line this short ends a paragraph
    pairs = []
    for _, rows, H, W in leaves:
        body = running_head(rows, H)
        if len(body) < MIN_LINES:
            continue
        xs = [l for _, _, l, _ in body]
        ys = [(t + b) / 2 for t, b, _, _ in body]
        flat = deskew(xs, ys)
        widths = [(r - l) / W for _, _, l, r in body]
        for i in range(1, len(body) - 2):
            if widths[i - 1] >= SHORT * measure:
                continue                      # the line before was not a paragraph's last
            if widths[i] < SHORT * measure:
                continue                      # a one-line paragraph says nothing about a margin
            rest = [flat[j] for j in range(i + 1, min(i + 4, len(body)))
                    if widths[j] >= 0.35 * measure]
            if len(rest) < 2:
                continue                      # no margin to measure the opening against
            pairs.append((flat[i] - float(np.median(rest))) / W)
    if len(pairs) < 20:
        return None
    a = np.asarray(pairs)
    # THE POPULATION IS SEVERAL POPULATIONS AND A THRESHOLD CANNOT SEPARATE THEM. Some openings
    # the right edge finds are flush by design - the line after a display, the first line of a
    # block - and the histogram of differences on the case study is plainly multi-modal: a mass
    # at zero, a second around a third of a quantum, and the indent itself. A first version kept
    # everything above half the median positive difference and pulled the second mass in with
    # the third, reading the quantum 15 per cent low. The clusters have to be found, not cut.
    pos = a[a > 0]
    if len(pos) < 10:
        return None
    step = 0.01
    hist = {}
    for v in pos:
        hist.setdefault(int(v / step), []).append(v)
    top = max(len(v) for v in hist.values())
    # THE INDENT IS THE HIGHEST WELL-POPULATED CLUSTER, not the largest one. A book's paragraphs
    # open flush more often than they indent - after every display, at the head of every block -
    # so the mass at zero can outweigh the quantum and the mode is the wrong statistic.
    peak = max(k for k, v in hist.items() if len(v) >= 0.25 * top)
    near = pos[np.abs(pos - (peak + 0.5) * step) <= step]
    if len(near) < 10:
        return None
    return float(np.mean(near)), len(near), len(pairs)


def main(argv):
    d = next((a for a in argv if not a.startswith("-")), None)
    if not d or not os.path.isdir(d):
        print(__doc__)
        return 2
    want = 40
    if "--sample" in argv:
        want = int(argv[argv.index("--sample") + 1])

    paths = sorted(glob.glob(os.path.join(d, "*.png")) + glob.glob(os.path.join(d, "*.tif")))
    leaves = body_leaves(paths, want)
    if not leaves:
        print("  no leaf in that directory looks like body type")
        return 1

    W = leaves[0][3]
    m = fit_measure(leaves)
    pitch = fit_pitch(leaves)
    block = fit_block(leaves)
    q = fit_quantum(leaves, m[0] if m else 0)

    out = {
        "leaves": len(leaves),
        "leaf_aspect": leaves[0][2] / leaves[0][3],
        "left_margin": m[0], "right_edge": m[1], "measure": m[2],
        "baseline_pitch": pitch,
        "block_top": block[0], "block_bottom": block[1], "block_height": block[2],
        "quantum_of_leaf": q[0] if q else None,
        "quantum_of_measure": (q[0] / m[2]) if (q and m) else None,
    }
    if "--json" in argv:
        print(json.dumps(out, indent=2))
        return 0

    print(f"  fitted on {len(leaves)} leaves chosen by ink fraction alone, {W} px wide")
    print(f"    leaf aspect              {out['leaf_aspect']:.4f}   (height over width)")
    print(f"    left margin              {m[0]:.4f}   of the leaf's width")
    print(f"    measure                  {m[2]:.4f}   of the leaf's width")
    print(f"    right margin             {1 - m[1]:.4f}   of the leaf's width")
    print(f"    baseline pitch           {pitch:.4f}   of the leaf's height")
    print(f"    text block, top          {block[0]:.4f}   of the leaf's height")
    print(f"    text block, height       {block[2]:.4f}   of the leaf's height")
    if q:
        print(f"    indent quantum           {q[0]:.4f}   of the leaf's width"
              f"   ({q[0] / m[2]:.4f} of the measure)")
        print(f"                             on {q[1]} leaves of {len(leaves)}, above a side-bearing floor of {q[3]:.4f}")
    else:
        print("    indent quantum           NOT RECOVERED")
    q2 = fit_quantum_by_paragraph(leaves, m[2])
    if q2:
        print(f"    quantum, by paragraph    {q2[0]:.4f}   of the leaf's width"
              f"   ({q2[0] / m[2]:.4f} of the measure)")
        print(f"                             from {q2[1]} indented openings of {q2[2]} found"
              f" by the right edge")
    print("\n  Fractions of the leaf. Points need the trim, and the trim is not in the ink.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

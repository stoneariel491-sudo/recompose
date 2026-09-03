"""Reading typographic geometry off a scanned page and off a rendered PDF.

Four primitives, each of which exists because an instrument was wrong without it. They are the
part of E03 that survived its refutation, plus the two that E02's corrections turned on.

Nothing here decides anything. These are measurements; the deciding belongs upstream, where the
thing being decided is known.
"""

import re
from collections import Counter


def ink_rows(image, head_band=0.075, min_height=20, threshold=128, min_ink=2):
    """(top, bottom, left, right) for every band of ink on a scanned leaf.

    head_band drops the running head, which is not part of the text and whose left edge is a
    property of the page furniture rather than of any paragraph.
    """
    import numpy as np
    a = np.asarray(image)
    if a.ndim == 3:
        a = a[:, :, :3].min(axis=2)
    H, _ = a.shape
    ink = a < threshold
    on = ink.sum(axis=1) > min_ink
    out, start = [], None
    for i, v in enumerate(list(on) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_height and start > head_band * H:
                cols = np.where(ink[start:i].any(axis=0))[0]
                out.append((start, i, int(cols[0]), int(cols[-1])))
            start = None
    return out


def deskew(xs, ys, keep_frac=0.60, rounds=8):
    """Left edges with the leaf's own tilt removed.

    A SCAN IS NOT SQUARE TO ITS SCANNER, and the amount matters. Measured on one book's index
    leaves, a column's left edge drifts by up to twenty points per thousand down the leaf -
    more than an eighth of an indent quantum over a full page, which is enough to split a
    single margin into two clusters and make every classification downstream unreliable.

    The fit is iterated on the lower envelope rather than on all the points, because every
    indented line pulls an ordinary least squares to the right. Each pass keeps the points at
    or left of the current line.
    """
    import numpy as np
    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    if len(x) < 6:
        return list(x)
    keep = np.ones(len(x), bool)
    coef = np.array([float(x.min()), 0.0])
    for _ in range(rounds):
        coef = np.polyfit(y[keep], x[keep], 1)
        r = x - np.polyval(coef, y)
        nk = r < np.percentile(r, keep_frac * 100)
        if nk.sum() < 5:
            break
        keep = nk
    flat = x - np.polyval(coef, y)
    return list(flat - flat.min())


def pdf_lines(doc, tol=4.0, marker=None):
    """Typographic lines of a rendered PDF, with the fragments of mathematics merged.

    A LINE OF A PDF EXTRACTOR IS NOT A LINE OF TYPE. Mathematics breaks a printed line into a
    fragment per fraction, per superscript, per radical, and counting those gave a median of
    fifty-two rows a page where the book sets thirty-five, with one page reporting seven
    hundred and forty-eight. Fragments within `tol` points of one another in y on the same leaf
    are one line, and the line begins where its leftmost fragment does.

    Returns [(leaf, y, left, text)], and if `marker` is a compiled pattern, also the markers it
    matched as [(leaf, y, match)] - a page-boundary anchor written into the text stream is the
    only reliable way to slice a rendered book back into the source's pages when the pagination
    has drifted.
    """
    out, marks = [], []
    for i in range(doc.page_count):
        frags = []
        for block in doc[i].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line.get("spans", [])).strip()
                if not text:
                    continue
                y0, x0 = line["bbox"][1], line["bbox"][0]
                if marker is not None:
                    m = marker.search(text)
                    if m:
                        marks.append((i, y0, m))
                        continue
                frags.append((y0, x0, text))
        # GROUPED BY THE GAP, NOT BY A BUCKET. Rounding y to a multiple of `tol` merges what
        # falls in one bucket, which is not what "within tol of one another" means: two
        # fragments two points apart straddling a bucket edge come back as two lines. On the
        # constructed page that found this, a sign at y=102 sat between its own line's 100 and
        # 101.5 and was split off from both. The anchor is the group's FIRST fragment rather
        # than its last, so a run of fragments each just under tol apart cannot chain into one
        # line of unbounded height.
        frags.sort()
        groups = []
        for y0, x0, text in frags:
            if groups and y0 - groups[-1][0] <= tol:
                groups[-1][1].append((x0, text))
            else:
                groups.append((y0, [(x0, text)]))
        for y0, parts in groups:
            parts.sort()
            # THE WHOLE LINE'S TEXT, in the order it is set. Keeping only the leftmost
            # fragment returns a line whose text is a fraction's numerator, and the use this
            # primitive was built for is locating a paragraph by the words it opens with.
            out.append((i, y0, parts[0][0], " ".join(t for _, t in parts)))
    out.sort()
    return (out, sorted(marks)) if marker is not None else out


def margins(lefts, tol, cluster=3):
    """The page's own left margins: every edge shared by `cluster` rows or more.

    A PAGE HAS SEVERAL MARGINS, NOT ONE - the body's, and those of whatever proof, example or
    exercise is open on it. Treating the commonest as the margin puts a line that is flush in
    its own block a full quantum out of place, which is how one gate came to report a page
    correct while it was wrong.

    Call this on deskewed edges. On raw ones the clusters smear and the count is meaningless.
    """
    hist = Counter(round(x / tol) * tol for x in lefts)
    return sorted(x for x, n in hist.items() if n >= cluster)


def local_frame(lefts, following=6, tol=None, agreement=0.5):
    """The margin an opening line should be measured against, or None if there is not one.

    Taken from the lines that FOLLOW, because a line's own position is the thing in question.

    AND IT IS RETURNED ONLY IF THOSE LINES AGREE. They routinely cross out of the opening's
    block - into a display, out of a proof, into an exercise - and the modal edge of a mixed
    population is not a margin. Without this test one gate reported a block margin of zero on
    one page and of 276 on another whose visible lines all stood at 434, and three of five
    sampled reports were false. Where fewer than `agreement` of them share an edge, there is no
    frame, and a page with no frame is skipped rather than judged.
    """
    if not lefts:
        return None
    tol = tol if tol is not None else 12
    tail = lefts[1:1 + following] or lefts[:1]
    hist = Counter(round(x / tol) * tol for x in tail)
    best = max(hist.values())
    # STRICTLY MORE THAN `agreement`, AND THE BOUNDARY IS THE WHOLE CASE. The first version of
    # this test read `best < agreement * len(tail)`, which accepts an exact tie - and an exact
    # tie is not a near miss here, it is the failure the test was written for. The page that
    # motivated it splits six following lines into three at the body margin and three inside a
    # block; that is 3 against a threshold of 3, the guard let it through, and min() then
    # returned the body margin for a line that belonged to the block. Found by a unit test on a
    # constructed page, not on a real one, which is the argument for constructing them.
    if best <= agreement * len(tail):
        return None
    return min(x for x, n in hist.items() if n == best)

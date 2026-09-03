"""The local frame: what a line's position is measured AGAINST, on a page that has no origin.

WHY THIS IS A PRIMITIVE AND NOT A DETAIL. Every question this pipeline asks about horizontal
position — is this paragraph indented, is that block set in, does the plate agree with the render —
is a question about a DIFFERENCE. There is no absolute frame to measure in: scanned leaves are not
registered to a common origin, and in the case study consecutive leaves sit up to 75 px apart while
their justified spans agree to one per cent. So the frame has to be built from the page's own lines,
and everything downstream inherits whatever that construction gets wrong.

Three separate instruments in the case study were refuted by their frame before this was written
down. The rules below are each the fix for a measured failure, not a precaution.

    THE FRAME IS THE DENSEST CLUSTER, NEVER THE MINIMUM.
        A numbered display hangs its number in the OPPOSITE margin - a full indent quantum left of
        every line of type - so the minimum takes the number for the body rule. Measured: a tail of
        [443, 608, 446, 287, 604] where 287 is the "(20)" of a display and the body rule is 443-448.
        The minimum also fails the other way: on a page where a false paragraph HAS been inserted,
        the tail alternates flush and indented, so minimum-plus-agreement refuses exactly the page
        the instrument exists to find - [38.0, 61.6, 36.0, 61.6].

    A LINE'S LEFT EDGE IS NOT ITS FIRST INK.
        Where a number hangs in the margin, the row's first ink column is the number. No justified
        line of prose carries a blank of that width inside it, so **the gap is the discriminator**
        and no threshold on position is needed - which matters because a position threshold would
        need the very frame being constructed.

    THE WINDOW IS PROSE LINES, NOT LINES.
        Taking "the prose among the next five rows" and taking "the next five prose rows" differ
        whenever a display sits under the line in question - which is precisely the situation that
        CREATES the fault class being hunted. The first refused those pages; the second reads past
        the display.

    THE WINDOW IS SMALL, AND THAT WAS MEASURED RATHER THAN ARGUED.
        Sweeping it against ground truth established by hand: 5 lines gives 7 right, 7 gives 4,
        9 gives 3, 11 gives 2. **Widening the frame degrades it monotonically**, because a wider
        window crosses block boundaries and the agreement test then refuses. Locality is not a
        preference here; it is the measured optimum.

    A FRAME THAT DOES NOT EXIST IS NOT A FRAME AT ZERO.
        When the lines do not agree on an edge, the answer is None and the caller must refuse.
        Returning a best guess is how an instrument acquires a false positive it cannot explain.
"""

MIN_LINES = 3          # below this a "cluster" is a coincidence
AGREE = 0.6            # of the window that must share an edge for a frame to exist
GAP = 0.06             # of the page width: a blank this wide inside a row is not a word space
NUMBER = 0.09          # of the page width: how wide a hanging number can be


def left_edge(cols, width):
    """Where the line starts, given the sorted ink columns of one row and the page width.

    Returns the first ink column, unless the row opens with a narrow run followed by a wide gap -
    a number hanging in the margin - in which case it returns the start of what follows the gap.
    """
    if len(cols) < 2:
        return int(cols[0]) if len(cols) else None
    for i in range(len(cols) - 1):
        if cols[i + 1] - cols[i] > GAP * width:
            return int(cols[i + 1]) if cols[i] - cols[0] < NUMBER * width else int(cols[0])
    return int(cols[0])


def frame(edges, tol):
    """The edge a window of lines agrees on, or None if they do not agree.

    `edges` are left edges already restricted to prose lines and to the window; `tol` is how far
    apart two lines may be and still count as the same rule. The result is the mean of the largest
    cluster, which is the rule the majority of the window sits on.
    """
    edges = [e for e in edges if e is not None]
    if len(edges) < MIN_LINES:
        return None
    best, size = None, 0
    for c in edges:
        n = sum(1 for e in edges if abs(e - c) <= tol)
        if n > size:
            best, size = c, n
    if size < AGREE * len(edges):
        return None
    return sum(e for e in edges if abs(e - best) <= tol) / float(size)


def window(lines, start, count, is_prose):
    """The next `count` PROSE lines after index `start`, not the prose among the next `count`.

    `lines` is any sequence; `is_prose` decides membership. The distinction is the whole point:
    a display under the line being measured must be read past, not counted against the budget.
    """
    out = []
    for i in range(start + 1, len(lines)):
        if is_prose(lines[i]):
            out.append(lines[i])
            if len(out) == count:
                break
    return out

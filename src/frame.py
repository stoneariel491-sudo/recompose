"""Where a line stands, on a page that has no origin — and the four rules that were wrong first.

WHY THIS IS A PRIMITIVE AND NOT A DETAIL. Every question this pipeline asks about horizontal
position — is this paragraph indented, is that block set in, does the plate agree with the render —
is a question about a DIFFERENCE. There is no absolute frame to measure in: scanned leaves are not
registered to a common origin, and in the case study consecutive leaves sit up to 75 px apart while
their justified spans agree to one per cent. So the reference has to be built from the page's own
lines, and everything downstream inherits whatever that construction gets wrong.

THE ANSWER IS NOT TO BUILD A BETTER REFERENCE. It is to stop building one.

Four versions of this file chose ONE number to call "the frame" and subtracted it from the line
being measured. Each was refuted by a page where that choice was the wrong level, and the sequence
is worth keeping because every fix broke the next page:

    min(tail)             captured by a numbered display's hanging number, which sits a full
                          indent quantum left of every line of type: [443, 608, 446, 287, 604],
                          where 287 is the "(20)".

    the DENSEST cluster   refuted on a page whose window held two INDENTED openings and a display
                          against two flush lines: [595, 579, 413, 413, 580]. The mode is 584.7,
                          the indent rule, so a line at 411 was measured against it and came out
                          "flush" — **the right answer for a reason that had nothing to do with
                          the page.** This version was published as a law in this repository and
                          refuted three hours later by a human reader.

    the LEFTMOST cluster  found two defects four other instruments had missed, then called two
                          settled pages indented by exactly one quantum: their openings sit inside
                          a proof block while the window also holds page-margin lines a level out.
                          **The leftmost rule on the leaf is not the rule the line belongs to.**

    the RIGHTMOST at or   fixed one of those two and left the other, whose own rule carries a
    left of the line      single line inside the window, so no cluster forms on it and the search
                          falls through to the level below — one quantum out, again.

Every one is the same failure. A page in a mathematical book carries THREE rules — equation
numbers, the proof block, the block's own indent — so **"the frame" is not a property of the leaf**,
and any rule that picks one number will pick the wrong level on some page.

What the instrument needs is not the frame but the answer, and the answer has exactly two
admissible values. So `sits` tests both and refuses when neither holds.

A NOTE ON WHY THE CONTROL COULD NOT CATCH THE SECOND VERSION, which is the sharpest thing here.
Its twelve cases had all been settled by hand and all had the same verdict: the plate runs the line
on. A frame displaced one quantum to the RIGHT still returns "flush" on every one of them. **A test
whose cases all share one answer cannot detect an error that preserves that answer** — and the
third version was caught by that same control only because it erred in the other direction.
"""

MIN_LINES = 3          # below this a window is a coincidence, not evidence
GAP = 0.06             # of the page width: a blank this wide inside a row is not a word space
NUMBER = 0.09          # of the page width: how wide a hanging number can be
NEAR = (0.6, 1.4)      # a line is indented if it stands this many quanta right of a rule


def left_edge(cols, width):
    """Where the LINE starts, given the sorted ink columns of one row and the page width.

    A NUMBERED DISPLAY HANGS ITS NUMBER IN THE OPPOSITE MARGIN, so a row's first ink column is the
    number and not the line. **No justified line of prose carries a blank of that width inside it**,
    so the gap is the discriminator — and that matters, because any threshold on POSITION would need
    the very reference being constructed.
    """
    if len(cols) < 2:
        return int(cols[0]) if len(cols) else None
    for i in range(len(cols) - 1):
        if cols[i + 1] - cols[i] > GAP * width:
            return int(cols[i + 1]) if cols[i] - cols[0] < NUMBER * width else int(cols[0])
    return int(cols[0])


def sits(window, tol, edge, quantum):
    """(the line is indented, its offset from the rule it belongs to), or None to refuse.

    `window` are the left edges of the nearby lines that could carry a rule; `edge` is the line
    being measured; `tol` is how far apart two lines may be and still sit on one rule.

        FLUSH     some rule in the window stands level with the line
        INDENTED  some rule stands one quantum to its left
        neither   REFUSE

    A single line is enough to witness a rule, because the hypothesis being tested already says
    where that rule must be. The earlier versions needed a cluster because they were SEARCHING for
    the frame rather than testing for it, and a search needs support where a test needs only a
    witness.

    A line both level with one rule and a quantum right of another is reported flush: that is the
    block-boundary case, and the nearer rule governs.
    """
    window = [w for w in window if w is not None]
    if len(window) < MIN_LINES:
        return None
    level = [w for w in window if abs(w - edge) <= tol]
    if level:
        base = min(level, key=lambda w: abs(w - edge))
        return False, edge - base
    for w in window:
        if NEAR[0] * quantum <= edge - w <= NEAR[1] * quantum:
            return True, edge - w
    return None


def window(lines, start, count, is_prose):
    """The next `count` PROSE lines after index `start`, not the prose among the next `count`.

    The distinction is the whole point: a display under the line being measured must be read past,
    not counted against the budget — and a display under the line is precisely the situation that
    CREATES the fault class these instruments hunt.
    """
    out = []
    for i in range(start + 1, len(lines)):
        if is_prose(lines[i]):
            out.append(lines[i])
            if len(out) == count:
                break
    return out

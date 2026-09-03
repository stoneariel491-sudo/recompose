"""The four primitives, against pages whose truth is constructed rather than observed.

WHY SYNTHETIC AND NOT REAL PAGES. A test that runs a primitive over a scan and checks the
answer against what the primitive said last time is a test of nothing: it locks in whatever
was wrong. Here every page is built from a known geometry, so the expected answer is known
before the function is called, and a wrong answer is a failure rather than a difference.

EACH TEST STATES THE ALTERNATIVE IT RULES OUT. Every one of these primitives exists because a
simpler thing was tried and was wrong - the mode instead of the clusters, the raw edges instead
of the deskewed ones, the extractor's rows instead of the lines of type - and where the simpler
thing can be written down, the test runs it too and shows it failing. A test that only confirms
the code does what the code does is worth less than the time it takes to run.
"""

import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import numpy as np

from geometry import deskew, ink_rows, local_frame, margins, pdf_lines


# The tilt measured on one book's index leaves: twenty points of drift per thousand down.
TILT = 0.020
QUANTUM = 26.0          # one indent
BODY = 100.0


def tilted_page(n=40, indent_every=3, tilt=TILT):
    """Left edges of n lines down a tilted leaf, every third one indented.

    Returns (xs, ys, indented) with `indented` the truth the primitives must recover.
    """
    ys = [float(30 * i) for i in range(n)]
    indented = [i % indent_every == 0 for i in range(n)]
    xs = [BODY + tilt * y + (QUANTUM if ind else 0.0) for y, ind in zip(ys, indented)]
    return xs, ys, indented


class Deskew(unittest.TestCase):

    def test_removes_the_tilt_and_keeps_the_indents(self):
        xs, ys, indented = tilted_page()
        flat = deskew(xs, ys)
        flush = [f for f, ind in zip(flat, indented) if not ind]
        ind = [f for f, ind in zip(flat, indented) if ind]
        self.assertLess(max(flush) - min(flush), 1.0,
                        "flush lines should land on one edge once the tilt is out")
        self.assertLess(max(ind) - min(ind), 1.0)
        self.assertAlmostEqual(sum(ind) / len(ind) - sum(flush) / len(flush), QUANTUM, delta=1.0)

    def test_a_straight_least_squares_fit_is_pulled_by_the_indents(self):
        """The alternative this primitive rules out, run here so the difference is visible.

        Fitting all the points at once puts the line through the middle of two populations, so
        the flush edge comes out negative and the indented one short. The lower envelope is
        fitted instead, iterated, keeping the points at or left of the current line.
        """
        xs, ys, indented = tilted_page()
        coef = np.polyfit(ys, xs, 1)
        naive = np.asarray(xs) - np.polyval(coef, ys)
        flush = naive[[not i for i in indented]]
        self.assertLess(flush.mean(), -5.0,
                        "if this passes, the indents no longer pull the fit and the "
                        "iterated envelope is not needed - check before deleting it")

    def test_too_few_lines_are_returned_untouched(self):
        xs = [10.0, 12.0, 11.0]
        self.assertEqual(deskew(xs, [0.0, 30.0, 60.0]), xs)


class Margins(unittest.TestCase):

    def test_finds_every_margin_and_not_only_the_commonest(self):
        """A page with a body and a proof block open on it has two margins, and a gate that
        takes the commonest puts every flush line of the block one quantum out of place."""
        lefts = [100.0] * 12 + [126.0] * 5 + [152.0] * 4
        self.assertEqual(margins(lefts, tol=6.0), [102.0, 126.0, 150.0])

    def test_an_edge_below_the_cluster_size_is_not_a_margin(self):
        lefts = [100.0] * 12 + [126.0] * 2
        self.assertEqual(margins(lefts, tol=6.0, cluster=3), [102.0])

    def test_raw_edges_smear_and_deskewed_ones_do_not(self):
        """The docstring's claim - 'call this on deskewed edges' - made into a failure.

        On the tilted leaf the two true margins are twenty-six points apart and the tilt drifts
        the edges by twenty-three over the leaf, so on raw edges the clusters overlap and the
        count of margins is wrong; on deskewed edges it is two.
        """
        xs, ys, _ = tilted_page()
        self.assertGreater(len(margins(xs, tol=6.0)), 2)
        self.assertEqual(len(margins(deskew(xs, ys), tol=6.0)), 2)


class LocalFrame(unittest.TestCase):

    def test_takes_the_frame_from_the_lines_below(self):
        lefts = [126.0] + [100.0] * 6
        self.assertEqual(local_frame(lefts, tol=12.0), 96.0)

    def test_refuses_when_the_lines_below_do_not_agree(self):
        """Three lines at the body margin and three inside a block is not a margin, it is two.

        This is the test that separates this primitive from the version before it, which
        returned the mode of a mixed population and reported a block margin of zero on one page
        and of 276 on another whose visible lines all stood at 434.
        """
        lefts = [126.0, 100.0, 101.0, 99.0, 434.0, 435.0, 433.0]
        self.assertIsNone(local_frame(lefts, tol=12.0))

    def test_no_lines_at_all_is_no_frame(self):
        self.assertIsNone(local_frame([]))


class InkRows(unittest.TestCase):

    def band(self, page, top, bottom, left, right):
        page[top:bottom, left:right] = 0

    def test_finds_the_bands_and_their_left_edges(self):
        page = np.full((1000, 800), 255, np.uint8)
        self.band(page, 200, 230, 100, 700)
        self.band(page, 260, 290, 126, 700)
        rows = ink_rows(page, min_height=20)
        self.assertEqual([(t, b, l) for t, b, l, _ in rows], [(200, 230, 100), (260, 290, 126)])

    def test_drops_the_running_head(self):
        """The head's left edge is a property of the page furniture and not of any paragraph,
        so a margin taken with it included is taken against the wrong thing."""
        page = np.full((1000, 800), 255, np.uint8)
        self.band(page, 30, 60, 60, 740)          # inside the head band at 0.075
        self.band(page, 200, 230, 100, 700)
        self.assertEqual(len(ink_rows(page)), 1)

    def test_a_band_thinner_than_a_line_is_not_a_line(self):
        page = np.full((1000, 800), 255, np.uint8)
        self.band(page, 200, 205, 100, 700)       # a rule, not type
        self.assertEqual(ink_rows(page, min_height=20), [])


class FakePage:
    def __init__(self, lines):
        self.lines = lines

    def get_text(self, _):
        return {"blocks": [{"lines": [
            {"bbox": (x, y, x + 10, y + 10), "spans": [{"text": t}]} for y, x, t in self.lines
        ]}]}


class FakeDoc:
    def __init__(self, pages):
        self.pages = pages
        self.page_count = len(pages)

    def __getitem__(self, i):
        return self.pages[i]


class PdfLines(unittest.TestCase):

    def test_merges_the_fragments_of_one_printed_line(self):
        """Mathematics breaks a printed line into a fragment per fraction, per superscript, per
        radical. Counting those gave a median of fifty-two rows a page where the book sets
        thirty-five, and one page reported seven hundred and forty-eight."""
        doc = FakeDoc([FakePage([
            (100.0, 200.0, "n"), (102.0, 180.0, "sum"), (101.5, 260.0, "= 1"),   # one line
            (140.0, 180.0, "and so the series converges"),
        ])])
        out = pdf_lines(doc, tol=4.0)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0][2], 180.0, "a line begins where its leftmost fragment does")

    def test_a_fragment_past_the_tolerance_is_its_own_line(self):
        doc = FakeDoc([FakePage([(100.0, 180.0, "a"), (109.0, 180.0, "b")])])
        self.assertEqual(len(pdf_lines(doc, tol=4.0)), 2)

    def test_markers_come_back_separately_and_not_as_type(self):
        """A page-boundary anchor written into the text stream is the only reliable way to
        slice a rendered book back into the source's pages once the pagination has drifted; it
        is furniture, so it must not be returned among the lines."""
        doc = FakeDoc([FakePage([
            (100.0, 180.0, "Rudin p.42"), (140.0, 180.0, "the body of the page"),
        ])])
        lines, marks = pdf_lines(doc, marker=re.compile(r"Rudin p[.](\d+)"))
        self.assertEqual([l[3] for l in lines], ["the body of the page"])
        self.assertEqual([m[2].group(1) for m in marks], ["42"])

    def test_leaves_come_back_in_order(self):
        doc = FakeDoc([FakePage([(100.0, 10.0, "one")]), FakePage([(100.0, 10.0, "two")])])
        self.assertEqual([l[0] for l in pdf_lines(doc)], [0, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)

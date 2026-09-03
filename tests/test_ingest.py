"""Stage 1's decisions, against leaves whose truth is constructed.

The three that matter are all decisions to REFUSE or to INVERT, and each was got wrong first.
Each test states the wrong answer it rules out, because that is what the test is for: the
primitives are easy to write in a way that runs and lies.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import numpy as np

from ingest import INK_PHOTO, SEPARABLE, ink_fraction, kind, otsu, page_images


class FakePix:
    """The three fields ink_fraction reads off a PyMuPDF pixmap."""

    def __init__(self, a):
        self.height, self.width = a.shape[:2]
        self.n = 1 if a.ndim == 2 else a.shape[2]
        self.samples = a.astype(np.uint8).tobytes()


def leaf(ink_frac, paper=245, ink=20, size=(400, 300), noise=0):
    """A leaf with a stated fraction of ink, and optionally a gradient across it."""
    rng = np.random.default_rng(0)
    a = np.full(size, paper, np.uint8)
    n = int(ink_frac * a.size)
    idx = rng.choice(a.size, n, replace=False)
    a.flat[idx] = ink
    if noise:
        grad = np.linspace(0, noise, size[1])[None, :]
        a = np.clip(a.astype(int) - grad, 0, 255).astype(np.uint8)
    return a


class Otsu(unittest.TestCase):

    def test_splits_a_two_mode_leaf_and_says_it_is_separable(self):
        # k IS THE TOP OF THE LOWER CLASS, so on a leaf whose ink is exactly 20 and whose paper
        # is exactly 245, k IS 20 - and this assertion first read `20 < t`, which is the same
        # off-by-one the code had. The convention has to be stated once and used on both sides.
        t, eta = otsu(leaf(0.05))
        self.assertTrue(20 <= t < 245, t)
        self.assertGreater(eta, SEPARABLE)

    def test_a_single_mode_leaf_is_reported_as_not_separable(self):
        """The case this exists for. A faint leaf lit by a gradient has one broad mode, and
        Otsu cuts through the middle of it and calls a third of the page ink. The separability
        is the tool's own statement that its assumption failed."""
        # A GAUSSIAN, NOT UNIFORM NOISE. Uniform values over a band still split cleanly in
        # the middle and score 0.75; one broad Gaussian mode - which is what a faint leaf lit
        # by a gradient actually looks like - scores 0.64.
        rng = np.random.default_rng(1)
        flat = np.clip(rng.normal(120, 25, size=(400, 300)), 0, 255).astype(np.uint8)
        _, eta = otsu(flat)
        self.assertLess(eta, SEPARABLE)


class InkFraction(unittest.TestCase):

    def test_measures_a_normal_leaf(self):
        f, inverted, _ = ink_fraction(FakePix(leaf(0.06)))
        self.assertFalse(inverted)
        self.assertAlmostEqual(f, 0.06, delta=0.01)

    def test_detects_a_stencil_stored_the_other_way_round(self):
        """A page of type is never more than half ink, in any face, at any size.

        The case study's own scan stores its foreground layer 0.995 dark; taken at face value
        every leaf of a book of type classified as photographic, and stage 2 - which picks its
        sample by ink fraction - would have found no body leaf at all.
        """
        f, inverted, _ = ink_fraction(FakePix(255 - leaf(0.06)))
        self.assertTrue(inverted)
        self.assertAlmostEqual(f, 0.06, delta=0.01)

    def test_refuses_a_leaf_whose_histogram_has_one_mode(self):
        """Not blank, not photographic. A refusal, in its own column.

        Before this, the same leaves were called blank by a fixed threshold and photographic by
        an unguarded Otsu - two wrong answers of opposite sign from one missing question."""
        rng = np.random.default_rng(2)
        flat = np.clip(rng.normal(120, 25, size=(400, 300)), 0, 255).astype(np.uint8)
        f, _, eta = ink_fraction(FakePix(flat))
        self.assertIsNone(f)
        self.assertLess(eta, SEPARABLE)


class Kind(unittest.TestCase):

    def test_type_and_photograph_are_separated_by_the_measured_threshold(self):
        self.assertEqual(kind(0.05), "stencil")
        self.assertEqual(kind(0.40), "photographic")

    def test_a_leaf_near_the_threshold_is_uncertain_and_not_assigned(self):
        """Stage 2 chooses its sample from this classification, so a mislabelled leaf is worse
        than a missing one."""
        self.assertEqual(kind(INK_PHOTO), "uncertain")

    def test_an_empty_leaf_is_blank_rather_than_type(self):
        self.assertEqual(kind(0.001), "blank")


class Rect:
    def __init__(self, w, h):
        self.width, self.height = w, h


class FakePage:
    """A page carrying images at stated pixel sizes, each placed over the whole leaf."""

    def __init__(self, w, h, images):
        self.rect = Rect(w, h)
        self._images = images

    def get_images(self, full=True):
        return [(xref, 0, iw, ih) for xref, iw, ih in self._images]

    def get_image_rects(self, xref):
        return [Rect(self.rect.width, self.rect.height)]


class PageImages(unittest.TestCase):

    def test_a_one_pixel_fill_stretched_over_the_page_is_refused(self):
        """It covers the page perfectly and carries no information at all. Every page of the
        case study's processed PDF holds two of them, and a coverage test alone took them for
        scanned leaves."""
        p = FakePage(324, 485, [(1, 1, 1), (2, 1, 1)])
        self.assertEqual(page_images(p), [])

    def test_a_real_scan_is_taken_at_its_own_resolution(self):
        p = FakePage(324, 485, [(9, 2698, 4038)])
        self.assertEqual([x[1] for x in page_images(p)], [9])

    def test_mixed_raster_content_returns_the_stencil_first(self):
        """A scanned PDF normally holds a background at 200 dpi and a stencil at 600, both
        over the whole leaf. Refusing several page-covering layers would refuse every ordinary
        scan there is; the one with the most pixels is the stencil."""
        p = FakePage(324, 485, [(3, 899, 1346), (4, 2698, 4038)])
        self.assertEqual([x[1] for x in page_images(p)], [4, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Each test is a failure that actually happened, reduced to the numbers that caused it."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import frame as F


W = 2691          # a case-study leaf, in pixels
TOL = 0.006 * W   # 16 px: two lines within this sit on the same rule


def test_frame_is_the_cluster_not_the_minimum():
    # A numbered display's "(20)" at 287, body rule 443-448, block indent 604-610. The minimum
    # takes 287 and one line in five then agrees, so the page is refused. The cluster takes 443.
    assert F.frame([443, 608, 446, 287, 604], TOL) is None      # no majority: this IS two rules
    assert abs(F.frame([443, 446, 444, 287, 604], TOL) - 444.33) < 0.1


def test_a_tail_that_alternates_has_no_frame():
    # A page where a false paragraph HAS been inserted: flush, indent, flush, indent. Refusing is
    # correct - but the caller must be told, not handed a number.
    assert F.frame([38.0, 61.6, 36.0, 61.6], 2.0) is None


def test_frame_refuses_rather_than_guessing():
    assert F.frame([100, 200], TOL) is None                     # too few
    assert F.frame([], TOL) is None
    assert F.frame([100, 400, 700, 1000], TOL) is None          # four rules, no majority


def test_frame_survives_one_outlier():
    assert abs(F.frame([440, 442, 441, 287], TOL) - 441.0) < 0.1


def test_left_edge_skips_a_hanging_number():
    # "(20)" occupying 287-360, then a gap, then the display body at 700.
    cols = list(range(287, 361)) + list(range(700, 1400))
    assert F.left_edge(cols, W) == 700


def test_left_edge_keeps_a_wide_first_run():
    # A prose line that happens to contain a wide gap is NOT a hanging number, because the run
    # before the gap is too wide to be one. The frame must not silently move to mid-line.
    cols = list(range(200, 1000)) + list(range(1300, 2400))
    assert F.left_edge(cols, W) == 200


def test_left_edge_of_ordinary_prose():
    assert F.left_edge(list(range(219, 2400)), W) == 219


def test_left_edge_of_a_one_word_line():
    # A page whose whole first line is the word "since" - 132 px of ink and nothing else.
    assert F.left_edge(list(range(405, 537)), W) == 405


def test_window_reads_past_a_display():
    # 0 is the line being measured, 1-6 are display fragments, 7-9 are the prose that frames it.
    lines = [("prose", 0)] + [("display", i) for i in range(1, 7)] + [("prose", i) for i in (7, 8, 9)]
    got = F.window(lines, 0, 3, lambda l: l[0] == "prose")
    assert [l[1] for l in got] == [7, 8, 9]


def test_window_stops_when_the_page_does():
    lines = [("prose", 0), ("display", 1), ("prose", 2)]
    assert len(F.window(lines, 0, 5, lambda l: l[0] == "prose")) == 1

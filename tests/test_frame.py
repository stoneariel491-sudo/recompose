"""Each test is a failure that actually happened, reduced to the numbers that caused it."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import frame as F


W = 2691           # a case-study leaf, in pixels
TOL = 0.006 * W    # 16 px: two lines within this sit on the same rule
Q = 0.060 * W      # the indent quantum, about 162 px


def test_flush_line_on_its_own_rule():
    # The offset is against the NEAREST level line, which is the rule the line itself sits on.
    assert F.sits([443, 446, 444], TOL, 446, Q) == (False, 0)


def test_indented_line_one_quantum_from_its_rule():
    # 606 against a rule at 443: 163 px, which is the quantum to within the tolerance. The offset
    # is measured against the rule found, not against the nominal quantum.
    ind, off = F.sits([443, 446, 444], TOL, 446 + 160, Q)
    assert ind and abs(off - Q) < TOL


def test_a_hanging_equation_number_no_longer_captures_the_answer():
    # [443, 608, 446, 287, 604], where 287 is a display's "(20)". min() took it for the body rule.
    assert F.sits([443, 608, 446, 287, 604], TOL, 446, Q) == (False, 0)


def test_the_mode_landing_on_the_indent_rule_no_longer_decides():
    # [595, 579, 413, 413, 580]: two indented openings and a display against two flush lines, so
    # the densest cluster is 584.7 - the INDENT rule. A line at 411 is flush, and was called flush
    # for the wrong reason. Now it is flush because 413 is level with it.
    ind, off = F.sits([595, 579, 413, 413, 580], TOL, 411, Q)
    assert ind is False and abs(off + 2) < 1


def test_a_rule_a_level_out_does_not_make_a_flush_line_indented():
    # A line at the proof-block rule, with page-margin lines also in the window. The leftmost rule
    # on the leaf is 267, one quantum out, and taking it reported this line as indented.
    assert F.sits([429, 267, 433, 270], TOL, 429, Q) == (False, 0)


def test_one_line_is_enough_to_witness_the_rule_it_names():
    # The rule the line belongs to carries a single line inside the window. A cluster search finds
    # nothing there and falls through a level; a test asks only whether that one line is level.
    assert F.sits([446, 604, 608], TOL, 446, Q) == (False, 0)


def test_it_refuses_when_neither_hypothesis_holds():
    # 350 is level with nothing in the window and stands 250 px right of 100, which is past the
    # 1.4-quantum ceiling, and to the LEFT of 400 and 700. Neither hypothesis holds. A first
    # version of this test used 200, which is 100 px right of a rule - inside the band, so the
    # answer was INDENTED and the test was asserting the wrong thing about a correct function.
    assert F.sits([100, 400, 700], TOL, 350, Q) is None
    assert F.sits([443, 446], TOL, 446, Q) is None          # too few to be evidence
    assert F.sits([], TOL, 100, Q) is None


def test_the_nearer_rule_governs_at_a_block_boundary():
    # Level with one rule and a quantum right of another: flush, because the nearer rule governs.
    assert F.sits([600, 600 - 160, 601], TOL, 600, Q)[0] is False


def test_left_edge_skips_a_hanging_number():
    cols = list(range(287, 361)) + list(range(700, 1400))
    assert F.left_edge(cols, W) == 700


def test_left_edge_keeps_a_wide_first_run():
    # A prose line containing a wide gap is not a hanging number: the run before it is too wide.
    cols = list(range(200, 1000)) + list(range(1300, 2400))
    assert F.left_edge(cols, W) == 200


def test_left_edge_of_a_one_word_line():
    # A page whose whole first line is one word - 132 px of ink and nothing else.
    assert F.left_edge(list(range(405, 537)), W) == 405


def test_window_reads_past_a_display():
    lines = [("prose", 0)] + [("display", i) for i in range(1, 7)] + [("prose", i) for i in (7, 8, 9)]
    got = F.window(lines, 0, 3, lambda l: l[0] == "prose")
    assert [l[1] for l in got] == [7, 8, 9]


def test_window_stops_when_the_page_does():
    lines = [("prose", 0), ("display", 1), ("prose", 2)]
    assert len(F.window(lines, 0, 5, lambda l: l[0] == "prose")) == 1

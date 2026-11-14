import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

#Example test cases:
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

#Write the rest of the test cases so that the code is 90- 100% covered.

# ---------------------------------
# Additional Lab 6 test cases
# ---------------------------------

# 1. Test different spam scoring conditions
@pytest.mark.parametrize("text,known,links,expected", [
    ("FREE winner!", False, 0, 4),
    ("OFFER TODAY", False, 0, 2),
    ("hello", False, 1, 1),
    ("hello", False, 4, 4),
    ("FREE", True, 0, 0),
    ("FREE WINNER", True, 0, 1),
    ("hello", True, 0, 0),
])
def test_score_message_branches(text, known, links, expected):
    assert score_message(text, known, links) == expected


# 2. Test all classification conditions
@pytest.mark.parametrize("score,expected", [
    (8, "spam"),
    (4, "suspicious"),
    (3, "clean"),
])
def test_classify_thresholds(score, expected):
    assert classify(score) == expected


# 3. Test empty inbox
def test_filter_inbox_empty():
    assert filter_inbox([]) == {
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }


# 4. Test inbox containing different messages
def test_filter_inbox_mixed():
    messages = [
        ("FREE WINNER URGENT", False, 4),
        ("FREE CASH", False, 0),
        ("hello", False, 0),
    ]

    assert filter_inbox(messages) == {
        "spam": 1,
        "suspicious": 1,
        "clean": 1
    }


# 5. Test all inbox status conditions
@pytest.mark.parametrize("counts,expected", [
    ({"spam": 0, "suspicious": 0, "clean": 0}, "empty"),
    ({"spam": 3, "suspicious": 0, "clean": 2}, "flooded"),
    ({"spam": 1, "suspicious": 0, "clean": 3}, "noisy"),
    ({"spam": 1, "suspicious": 1, "clean": 3}, "healthy"),
])
def test_inbox_status(counts, expected):
    assert inbox_status(counts) == expected

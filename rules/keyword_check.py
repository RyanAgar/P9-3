# -----------------------------------------------------------
# This file checks for suspicious words in an email.
# Idea:
#   - Certain words like "urgent" or "password" often show up in scams.
#   - If they are in the SUBJECT line, they are extra suspicious.
#   - If they are in the BODY, they still matter, but less.
#   - If they appear right at the START of the body, we treat it as even riskier.
# Each word can give at most 5 points total.
# In the end, we turn the total into a percentage (0–100%).
# -----------------------------------------------------------

import re
from typing import Tuple, Dict, Any

# List of “red-flag” words and phrases attackers commonly use.
SUSPICIOUS_KEYWORDS = [
    # Urgency
    "urgent", "immediately", "important", "attention", "asap",
    # Verification / Login
    "verify", "update", "login", "sign in", "authenticate",
    # Account / Security
    "account", "password", "credentials", "secure", "suspended", "locked",
    # Financial / Payment
    "payment", "invoice", "transaction", "credit card", "bank",
    # Links
    "click", "link", "http", "https",
]

# Scoring rules:
# - Subject hit = 3 points
# - Body hit = 1 point
# - Bonus if word appears in first 200 chars of body = +1 point
# Max = 5 points per keyword → makes it easy to convert to %
_MAX_PER_KEYWORD = 5
_EARLY_WINDOW = 200  # we call "early" = first 200 characters of the email body


def _regex_for_kw(kw: str) -> re.Pattern:
    """
    Build a search pattern for each keyword.
    - If keyword is 'bank', only match the whole word 'bank'
      (not 'banking' or 'snowbank').
    - If keyword is 'sign in', match that full phrase.
    - Ignore upper/lowercase → 'BANK', 'Bank', 'bank' all match.
    """
    return re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)


def _subject_points(subject: str, kw_pat: re.Pattern) -> int:
    """
    Give 3 points if keyword is found in the subject.
    """
    return 3 if kw_pat.search(subject) else 0


def _body_points(body: str, kw_pat: re.Pattern) -> Tuple[int, int]:
    """
    Check if keyword is in the body.
    - Always gives 1 point if found.
    - Gives +1 extra if it shows up very early (first 200 chars).
    Returns a pair (normal_points, early_bonus).
    """
    match = kw_pat.search(body)
    if not match:
        return 0, 0
    body_points = 1
    early_bonus = 1 if match.start() < _EARLY_WINDOW else 0
    return body_points, early_bonus


def keyword_score(subject: str, body: str) -> float:
    """
    Main function: calculate overall keyword risk as a percentage (0–100).
    - Goes through every suspicious word.
    - Adds points from subject + body + early bonus.
    - Normalizes against max possible points for fairness.
    """
    subject = subject or ""
    body = body or ""

    score = 0
    for kw in SUSPICIOUS_KEYWORDS:
        pattern = _regex_for_kw(kw)
        score += _subject_points(subject, pattern)
        body_pts, bonus = _body_points(body, pattern)
        score += body_pts + bonus

    max_possible = len(SUSPICIOUS_KEYWORDS) * _MAX_PER_KEYWORD
    return round((score / max_possible) * 100, 2)

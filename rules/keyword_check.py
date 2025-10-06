# -----------------------------------------------------------
# This file checks for suspicious words in an email.
# Idea:
#   - Certain words like "urgent" or "password" often appear in scams.
#   - If they are in the SUBJECT line, they are extra suspicious.
#   - If they are in the BODY, they still matter, but less.
#   - If they appear right at the START of the body, we treat it as even riskier.
# Each word can give at most 5 points total.
# In the end, we turn the total into a percentage (0–100%).
# -----------------------------------------------------------

import re
from pathlib import Path

#Load keywords.txt into a list
def load_keywords(path: str) -> list[str]:
    seen = set()
    keyword_list = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"): #Skip comments and empty lines
                continue
            keyword = " ".join(line.split())

            if keyword.lower() in seen: #Prevent duplication by checking with set object O(1)
                continue
            seen.add(keyword.lower())

            keyword_list.append(keyword)
    return keyword_list

KEYWORDS_PATH = Path(__file__).parent / "keywords.txt"
SUSPICIOUS_KEYWORDS = load_keywords(KEYWORDS_PATH)

# Scoring rules:
# - Subject hit = 3 points
# - Body hit = 1 point
# - Bonus if word appears in first 200 chars of body = +1 point
# Max = 5 points per keyword -> makes it easy to convert to %
_MAX_PER_KEYWORD = 6
_EARLY_WINDOW = 200  # we call "early" = first 200 characters of the email body


def _regex_for_kw(kw: str) -> re.Pattern:
    """
    Build a search pattern for each keyword.
    - If keyword is 'bank', only match the whole word 'bank'
      (not 'banking' or 'snowbank').
    - If keyword is 'sign in', match that full phrase.
    - Ignore upper/lowercase -> 'BANK', 'Bank', 'bank' all match.
    """
    return re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)


def _subject_points(subject: str, kw_pat: re.Pattern) -> int:
    """Return 3 if kw_pat matches subject, else return 0."""
    if not subject:
        return 0
    return 3 if kw_pat.search(subject) else 0


def _body_points(body: str, kw_pat: re.Pattern) -> tuple[int, int]:
    """
    Check if keyword is in the body.
    - Always gives 1 point if found.
    - Gives +1 extra if it shows up very early (first 200 chars).
    - Returns tuple of int (normal_points, early_bonus).
    """
    if not body:
        return 0, 0
    match = kw_pat.search(body)
    if not match:
        return 0, 0
    body_points = 1
    early_bonus = 2 if match.start() < _EARLY_WINDOW else 0
    return body_points, early_bonus


def keyword_score(subject: str, body: str) -> float:
    """
    Calculate overall keyword risk as a percentage (0-100%).
    - Goes through every suspicious word.
    - Adds points from subject + body + early bonus.
    - Normalizes against max possible points for fairness.
    """
    #Ensure subject and body are strings
    subject = subject or ""
    body = body or ""

    score = 0
    for kw in SUSPICIOUS_KEYWORDS:
        pattern = _regex_for_kw(kw)
        score += _subject_points(subject, pattern)
        body_pts, bonus = _body_points(body, pattern)
        score += body_pts + bonus

    max_possible = len(SUSPICIOUS_KEYWORDS) * _MAX_PER_KEYWORD
    return round((score / max_possible) * 100, 2) #score in percentage

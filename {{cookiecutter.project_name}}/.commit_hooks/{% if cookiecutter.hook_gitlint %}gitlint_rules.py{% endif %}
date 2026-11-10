"""
Custom gitlint rules, loaded through extra-path in .gitlint
"""

import re
from collections.abc import Sequence

from gitlint.git import GitCommit
from gitlint.rules import CommitMessageTitle, LineRule, RuleViolation
from pydocstyle.wordlists import IMPERATIVE_BLACKLIST, IMPERATIVE_VERBS, stem

STEMMER_EXCEPTIONS = frozenset({"embed"})
# The title's first word, after any Jira keys that a hook such as merge-issue-number-hook added
FIRST_WORD = re.compile(r"(?:[A-Z][A-Z0-9_]+-\d+: )*(\w+)")


def word_is_imperative(word: str) -> bool:
    """
    Check whether a word is an imperative verb, e.g. "Add" and not "Added"

    shortcut: words missing from pydocstyle's wordlist are judged by suffix; add misjudged
    verbs to STEMMER_EXCEPTIONS.

    :param word: The first word of the commit title
    :return: True if the word is an imperative verb
    """
    word = word.lower()
    if word in IMPERATIVE_BLACKLIST:
        return False
    if forms := IMPERATIVE_VERBS.get(stem(word)):
        return word in forms
    word_is_inflected = word.endswith(("ed", "ing", "s")) and stem(word) != word
    return word in STEMMER_EXCEPTIONS or not word_is_inflected


class TitleImperativeMood(LineRule):
    """
    UL1: Require the title's first word to be in the imperative mood
    """

    name = "title-imperative-mood"
    id = "UL1"
    target = CommitMessageTitle

    def validate(self, line: str, _: GitCommit) -> Sequence[RuleViolation] | None:
        """
        Check the first word of the title

        :param line: The commit title, e.g. "Add map writer"
        :return: A violation if the word isn't imperative, else None
        """
        match = FIRST_WORD.match(line)
        if match and not word_is_imperative(match[1]):
            message = f"Title must use the imperative mood (e.g. 'Add', not '{match[1]}')"
            return [RuleViolation(self.id, message, line)]
        return None


class TitleCapitalized(LineRule):
    """
    UL2: Require the title's first word to start with a capital letter
    """

    name = "title-capitalized"
    id = "UL2"
    target = CommitMessageTitle

    def validate(self, line: str, _: GitCommit) -> Sequence[RuleViolation] | None:
        """
        Check the first letter of the title

        :param line: The commit title, e.g. "Add map writer"
        :return: A violation if the first word starts with a lowercase letter, else None
        """
        match = FIRST_WORD.match(line)
        if match and match[1][0].islower():
            return [RuleViolation(self.id, "Title must start with a capital letter", line)]
        return None

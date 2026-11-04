import pytest
from password_policy import check_password, strength, suggest_fix

def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []


def test_valid_password_is_good():
    assert strength("Abcdef1!") == "good"


def test_password_at_maximum_length_is_valid():
    assert check_password("A" + "b" * 61 + "1!") == []


def test_password_longer_than_maximum_length_is_too_long():
    assert check_password("A" + "b" * 62 + "1!") == ["too long"]


def test_common_password_is_reported_case_insensitively():
    assert check_password("PASSWORD") == [
        "common",
        "no lowercase",
        "no digit",
        "no special",
    ]


@pytest.mark.parametrize(
    ("password", "expected_issue"),
    [
        ("abcdefgh1!", "no uppercase"),
        ("ABCDEFGH1!", "no lowercase"),
        ("Abcdefgh!", "no digit"),
        ("Abcdefg1", "no special"),
    ],
)
def test_password_reports_missing_character_categories(password, expected_issue):
    assert check_password(password) == [expected_issue]


def test_empty_password_reports_length_and_all_missing_categories():
    assert check_password("") == [
        "too short",
        "no uppercase",
        "no lowercase",
        "no digit",
        "no special",
    ]


def test_long_valid_password_is_strong():
    assert strength("Abcdefghij1!xy") == "strong"


def test_password_with_few_issues_is_weak():
    assert strength("Ab1!") == "weak"


def test_password_with_many_issues_is_very_weak():
    assert strength("abcdefgh") == "very weak"


def test_suggest_fix_for_valid_password():
    assert suggest_fix([]) == "none needed"


def test_suggest_fix_uses_first_issue_when_password_has_multiple_issues():
    issues = check_password("letmein")
    assert issues[0] == "too short"
    assert "common" in issues
    assert suggest_fix(issues) == "add more characters"


@pytest.mark.parametrize(
    ("issues", "expected_suggestion"),
    [
        (["too short"], "add more characters"),
        (["common"], "avoid common passwords"),
        (["no digit"], "add digit"),
        (["too long"], "shorten it"),
    ],
)
def test_suggest_fix_for_first_issue(issues, expected_suggestion):
    assert suggest_fix(issues) == expected_suggestion

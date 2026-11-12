from hypothesis import given, strategies as st

from password_policy import digit_ratio, first_character_type, split_credentials


@given(st.text() | st.none())
def test_first_character_type_no_crash(s):
    result = first_character_type(s)
    assert result in {"digit", "letter", "symbol"}


@given(st.text() | st.none())
def test_split_credentials_no_crash(s):
    result = split_credentials(s)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(part, str) for part in result)


@given(st.text() | st.none())
def test_digit_ratio_no_crash(s):
    result = digit_ratio(s)
    assert 0.0 <= result <= 1.0


def test_first_character_type_examples():
    assert first_character_type("7abc") == "digit"
    assert first_character_type("abc") == "letter"
    assert first_character_type("!abc") == "symbol"
    assert first_character_type("") == "symbol"
    assert first_character_type(None) == "symbol"


def test_split_credentials_examples():
    assert split_credentials("alice:Secret1") == ("alice", "Secret1")
    assert split_credentials(" alice : Secret1 ") == ("alice", "Secret1")
    assert split_credentials("alice") == ("alice", "")
    assert split_credentials(":") == ("", "")
    assert split_credentials(None) == ('', '')


def test_digit_ratio_examples():
    assert digit_ratio("abc") == 0.0
    assert digit_ratio("a1b2") == 2 / 4
    assert digit_ratio("") == 0.0
    assert digit_ratio(None) == 0.0

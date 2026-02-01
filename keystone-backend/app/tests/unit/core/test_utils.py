from app.core.utils import camel_case_to_snake_case


def test_camel_case_to_snake_case_empty_string():
    assert camel_case_to_snake_case("") == ""


def test_camel_case_to_snake_case_single_lowercase():
    assert camel_case_to_snake_case("a") == "a"


def test_camel_case_to_snake_case_single_uppercase():
    assert camel_case_to_snake_case("A") == "a"


def test_camel_case_to_snake_case_simple_camel():
    assert camel_case_to_snake_case("simpleTest") == "simple_test"


def test_camel_case_to_snake_case_complex_camel():
    assert camel_case_to_snake_case("CamelCaseTest") == "camel_case_test"


def test_camel_case_to_snake_case_with_numbers():
    assert camel_case_to_snake_case("test123Value456") == "test123_value456"


def test_camel_case_to_snake_case_mixed_case():
    assert camel_case_to_snake_case("iPhone") == "i_phone"
    assert camel_case_to_snake_case("B2BCompany") == "b2_b_company"

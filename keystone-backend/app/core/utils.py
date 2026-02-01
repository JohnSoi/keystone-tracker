"""Модуль с вспомогательными функциями."""


def camel_case_to_snake_case(value: str) -> str:
    """
    Преобразует строку из camelCase в snake_case.

    Args:
        value (str): Строка в camelCase.

    Returns:
        (str): Строка в snake_case.

    Examples:
        >>> camel_case_to_snake_case("camelCaseString")
        >>> #"camel_case_string"
    """
    if value:
        return "".join(["_" + i.lower() if i.isupper() else i for i in value]).lstrip("_")

    return value

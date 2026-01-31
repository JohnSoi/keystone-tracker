def camel_case_to_snake_case(value: str) -> str:
    if value:
        return "".join(["_" + i.lower() if i.isupper() else i for i in value]).lstrip("_")
    else:
        return value

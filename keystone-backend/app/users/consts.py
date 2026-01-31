"""Модуль констант для работы с пользователями."""

# Регулярное выражение для проверки email
EMAIL_VALIDATION_EXP: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Минимальный возраст пользователя
MIN_USER_AGE: int = 18

# Название куки для хранения access_token
ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
# Название куки для хранения refresh_token
REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"

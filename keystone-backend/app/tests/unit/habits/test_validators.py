import pytest
from app.habits.validators import validate_hex_color, validate_days_of_week
from app.habits.exceptions import InvalidColorTypeException, InvalidColorValueException, InvalidDayInWeekException, TooManyDaysOfWeekException, InvalidDayOfWeekException, DuplicatesInDayOfWeekException


def test_validate_hex_color_valid_with_hash():
    """Тест валидного HEX цвета с символом #."""
    assert validate_hex_color("#abc123") == "#ABC123"
    assert validate_hex_color("#ABC123") == "#ABC123"
    assert validate_hex_color("#123abc") == "#123ABC"


def test_validate_hex_color_valid_without_hash():
    """Тест валидного HEX цвета без символа #."""
    assert validate_hex_color("abc123") == "#ABC123"
    assert validate_hex_color("123abc") == "#123ABC"


def test_validate_hex_color_invalid_type():
    """Тест передачи невалидного типа данных."""
    with pytest.raises(InvalidColorTypeException):
        validate_hex_color(123)
    
    with pytest.raises(InvalidColorTypeException):
        validate_hex_color(None)
    
    with pytest.raises(InvalidColorTypeException):
        validate_hex_color([])


def test_validate_hex_color_invalid_length():
    """Тест HEX цветов с неправильной длиной."""
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#ab")
    
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#abcdefg")
    
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#abcde")


def test_validate_hex_color_invalid_characters():
    """Тест HEX цветов с недопустимыми символами."""
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#abg123")
    
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#abc123!")
    
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#abс123")  # кириллическая 'с'


def test_validate_hex_color_edge_cases():
    """Тест граничных случаев."""
    # Граничные значения
    assert validate_hex_color("#000000") == "#000000"  # черный
    assert validate_hex_color("#FFFFFF") == "#FFFFFF"  # белый
    
    # Минимальная и максимальная длина (уже проверено, но на всякий случай)
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("")
    
    with pytest.raises(InvalidColorValueException):
        validate_hex_color("#" * 8)

def test_validate_days_of_week_valid():
    """Тест валидных дней недели."""
    # Все дни недели в правильном порядке
    assert validate_days_of_week([1, 2, 3, 4, 5, 6, 7]) == [1, 2, 3, 4, 5, 6, 7]
    
    # Подмножество дней недели
    assert validate_days_of_week([1, 3, 5]) == [1, 3, 5]
    
    # Один день недели
    assert validate_days_of_week([1]) == [1]
    
    # Все дни недели в разном порядке
    assert validate_days_of_week([7, 6, 5, 4, 3, 2, 1]) == [7, 6, 5, 4, 3, 2, 1]


def test_validate_days_of_week_invalid_day():
    """Тест невалидных дней недели."""
    # Дни вне диапазона 1-7
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([0])
    
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([8])
    
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([-1])
    
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([100])
    
    # Несколько невалидных дней
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([1, 2, 8])
    
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([0, 7])


def test_validate_days_of_week_too_many_days():
    """Тест слишком большого количества дней недели."""
    # Больше 7 дней
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week([1, 2, 3, 4, 5, 6, 7, 9])
    
    # Много повторяющихся дней
    with pytest.raises(DuplicatesInDayOfWeekException):
        validate_days_of_week([1] * 8)
    
    # Очень длинный список
    with pytest.raises(InvalidDayInWeekException):
        validate_days_of_week(list(range(1, 10)))


def test_validate_days_of_week_edge_cases():
    """Тест граничных случаев."""
    # Пустой список - должен быть валидным (никакие дни не выбраны)
    assert validate_days_of_week([]) == []
    
    # Проверка граничных значений диапазона
    assert validate_days_of_week([1]) == [1]  # первый день
    assert validate_days_of_week([7]) == [7]  # последний день


def test_validate_days_of_week_duplicates():
    """Тест дубликатов в днях недели."""
    with pytest.raises(DuplicatesInDayOfWeekException):
        validate_days_of_week([1, 1])
    
    with pytest.raises(DuplicatesInDayOfWeekException):
        validate_days_of_week([1, 2, 1])
    
    with pytest.raises(DuplicatesInDayOfWeekException):
        validate_days_of_week([1, 2, 3, 4, 5, 6, 7, 1])


def test_validate_days_of_week_not_list():
    """Тест передачи не списка."""
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week("123")
    
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week("1,2,3")
    
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week(123)
    
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week(None)
    
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week({})
    
    with pytest.raises(InvalidDayOfWeekException):
        validate_days_of_week((1, 2, 3))
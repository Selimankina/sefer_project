def format_number(number: str) -> str:
    """
    Приведение номера к формату:
    - 4 цифры (с leading zeros)
    - опциональная буква в конце (в нижнем регистре)
    """
    if not number:
        return None

    digits = ''.join(filter(str.isdigit, number))
    letters = ''.join(filter(str.isalpha, number))

    digits = digits.zfill(4)

    if not digits or set(digits) == {"0"}:
        return None

    return f"{digits}{letters.lower()}"
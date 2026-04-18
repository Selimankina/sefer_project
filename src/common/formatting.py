def format_number(number: str) -> str:
    """
    Приведение номера к формату:
    - 4 цифры (leading zeros)
    - буквы в конце
    """

    digits = "".join(filter(str.isdigit, number))
    suffix = "".join(filter(str.isalpha, number))

    return digits.zfill(4) + suffix
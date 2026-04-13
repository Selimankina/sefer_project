def format_number(raw_number: str) -> str:
    if raw_number is None:
        return None

    digits_part = ""
    letter_part = ""

    for ch in raw_number:
        if ch.isdigit():
            digits_part += ch
        else:
            letter_part += ch

    digits_part = digits_part.zfill(4)

    return digits_part + letter_part
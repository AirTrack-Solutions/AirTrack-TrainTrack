# utils/country_flags.py
def get_country_flag(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return ""
    code = country_code.upper()
    return "".join(chr(0x1F1E6 + ord(c) - ord('A')) for c in code)

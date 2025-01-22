import datetime
import re


def format_date_string(date_line: "str") -> str:
    """Принимает строку с датой формата DD.MM.YYYY HH:MM:SS
    возвращает строку формата YYYY-MM-DD HH:MM:SS
    """
    if date_line:
        try:
            date_obj = datetime.datetime.strptime(date_line, "%d.%m.%Y %H:%M:%S")
            new_date_string = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            return new_date_string
        except Exception:
            return ""
    return ""

def get_date(date: str: str) -> str:
    """ Из строкu формата YYYY-MM-DD HH:MM:SS возвращает строку с датой
    формата YYYY-MM-DD"""
    pass


def get_greeting_by_time(time_string: str) -> str:
    """Функция принимает строку с датой формата YYYY-MM-DD HH:MM:SS
    и возвращает приветствие соответственно часам"""
    if time_string:
        try:
            date_obj = datetime.datetime.strptime(time_string,"%Y-%m-%d %H:%M:%S")
            hour = date_obj.hour
            if hour:
                if 5 <= hour < 12:
                    return "Доброе утро"
                elif 12 <= hour < 17:
                    return "Добрый день"
                elif 17 <= hour < 22:
                    return "Добрый вечер"
                elif 22 <= hour < 24 or 0 <= hour < 5:
                    return "Доброй ночи"
                else:
                    return ""
        except ValueError:
            return ""
    return ""


def get_card_number(card: str) -> str:
    """Из строки с номером карты убирает символ звездочки"""
    if card:
        card_number = re.sub(r"\*", "", str(card))
        return card_number
    return ""






if __name__ == "__main__":
    d = format_date_string('31.12.2021 16:44:00')
    print(d)
    h = get_greeting_by_time("2021-12-31 5:44:00")
    print(h)
    c = get_card_number("*6578")
    print(c)




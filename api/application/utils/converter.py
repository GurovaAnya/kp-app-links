import datetime


class Converter:

    @staticmethod
    def string_to_date(string: str):
        if string is None:
            return None
        print(string)
        date_values = string.split(" ")
        day = int(date_values[0])
        month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        month = month_list.index(date_values[1]) + 1
        year = int(date_values[2])
        return datetime.date(year, month, day)

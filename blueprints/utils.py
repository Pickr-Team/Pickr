from datetime import datetime


def get_graduation_year():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    if current_month >= 7:
        return current_year + 1
    else:
        return current_year
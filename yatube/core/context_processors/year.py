import datetime

year = datetime.datetime.today().year


def year(request):
    """Добавляет переменную с текущим годом."""
    return {
        'year': datetime.datetime.today().year,
    }

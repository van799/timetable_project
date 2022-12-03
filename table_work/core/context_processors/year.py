from django.utils import timezone


def year(request):
    """Добавляет переменную с текущим годом."""
    now = timezone.now()
    utc_time = now.year
    return {
        'year': utc_time,
    }

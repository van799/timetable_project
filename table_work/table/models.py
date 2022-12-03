from django.db import models


class Month(models.Model):
    """Класс месяцев."""
    class Meta:
        verbose_name = 'Месяц'
        verbose_name_plural = 'Месяцы'

    TYPE_CHOICES = [
        ("1", 'январь'),
        ("2", 'февраль'),
        ("3", 'март'),
        ("4", 'апрель'),
        ("5", 'май'),
        ("6", 'июнь'),
        ("7", 'июль'),
        ("8", 'август'),
        ("9", 'сентябрь'),
        ("10", 'октябрь'),
        ("11", 'ноябрь'),
        ("12", 'декабрь'),
    ]

    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=32, choices=TYPE_CHOICES)

    def __str__(self):
        return self.month


class Workers(models.Model):
    """Класс сотрудников."""
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    name_people = models.CharField(max_length=128, default='Дмитриев')

    def __str__(self):
        return f'{self.name_people}'


class SecurityType(models.Model):
    """Класс типа дежурств."""
    class Meta:
        verbose_name = 'Тип дежурств'
        verbose_name_plural = 'Тип дежурства'

    type_security = models.CharField(max_length=128, default='Дежурный по кабинетам')

    def __str__(self):
        return f'{self.type_security}'


class Event(models.Model):
    """Класс добавление дежурств."""
    class Meta:
        verbose_name = 'Дежурств'
        verbose_name_plural = 'Дежурства'

    event_id = models.AutoField(primary_key=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='event')
    title = models.ForeignKey(Workers, on_delete=models.CASCADE, related_name='workers')
    start_date = models.DateField()
    type_security = models.ForeignKey(SecurityType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """Класс добавления комментариев."""
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    author = models.CharField(
        max_length=15,
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Комментарий',
    )
    created = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True
    )

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text

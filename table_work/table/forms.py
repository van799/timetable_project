from django import forms

from .models import Comment, Event, Month


class CommentForm(forms.ModelForm):
    """Класс форма добавления комментариев."""
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Введите текст комментария',
                'class': 'form-control',
                'rows': 3,
            }),
            'author': forms.Textarea(attrs={
                'placeholder': 'Введите фамилию',
                'class': 'form-control',
                'rows': 1,
            }),
        }


class EventsForm(forms.ModelForm):
    """Форма добавления дежурства."""
    class Meta:
        model = Event
        fields = ('month', 'title', 'start_date', 'type_security',)
        widgets = {
            'month': forms.Select(attrs={
                'placeholder': 'Введите месяц',
                'class': 'form-control',
                'rows': 1,
            }),
            'title': forms.Select(attrs={
                'placeholder': 'Выберете фамилию',
                'class': 'form-control',
                'rows': 1,
            }),
            'type_security': forms.Select(attrs={
                'placeholder': 'Выберете фамилию',
                'class': 'form-control',
                'rows': 1,
            }),

        }


class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ('id', 'month',)

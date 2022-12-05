import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm, EventsForm, MonthForm
from .models import Month, Comment, Event, Workers
from .serializers import EventSerializer


def index(request):
    """Отображение дежурств"""
    # получаем из get запроса месяц, если месяц не указан выставляем текучий месяц
    if "month" in request.GET:
        selected_calendar = request.GET["month"]
        calendar = get_object_or_404(Month, id=selected_calendar)
    else:
        now = datetime.datetime.now()
        selected_calendar = int(now.month)
        calendar = get_object_or_404(Month, id=selected_calendar)

    fullcalendar = EventSerializer(
        calendar.event.all(), many=True
    ).data

    # В бесплатной версии календаря нет возможности сделать 2 строки,
    # календаре поэтому календаре в поле title обедняется с полем type_security
    for len_contex in range(len(fullcalendar)):
        fullcalendar[len_contex]['title'] = fullcalendar[len_contex]['title'] + '\\' + \
                                            fullcalendar[len_contex]['type_security']

    # выводим комментарии
    form = CommentForm(request.POST or None,
                       files=request.FILES or None)

    # фильтруем комментарии по месяцам и проводим сортировку
    comments_list = Comment.objects.filter(month=selected_calendar).order_by('-created')
    # добавляем пагинацию на 3 комментария
    paginator = Paginator(comments_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # выводим форму выбора месяца, с текущим месяцем
    month = get_object_or_404(Month, month=selected_calendar)
    all_calendar = MonthForm(
        request.POST or None,
        instance=month
    )

    context = {
        'events': fullcalendar,
        'form': form,
        'page_obj': page_obj,
        'all_calendar': all_calendar,
        'selected_calendar': int(selected_calendar)

    }
    return render(request, "table/index.html", context)


# функция добавления комментария
def add_comment(request, selected_calendar):
    month = get_object_or_404(Month, id=selected_calendar)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.month = month
        comment.save()
    return redirect('table:index')


# функция добавления дежурств, доступна только администратору
@login_required
def create_table(request):
    """Добавление дежурств"""
    if "month" in request.GET:
        selected_calendar = request.GET["month"]
    else:
        now = datetime.datetime.now()
        selected_calendar = int(now.month)
    # выводим форму выбора месяца, с текущим месяцем
    month = get_object_or_404(Month, month=selected_calendar)
    all_calendar = MonthForm(
        request.POST or None,
        instance=month
    )

    form = EventsForm(
        request.POST or None,
    )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    # сортировка дежурств по имени или по дате
    sort = request.GET.get('sort')
    if sort == 'date_up':
        tables = Event.objects.filter(month=selected_calendar).order_by('start_date')
    else:
        tables = Event.objects.filter(month=selected_calendar).order_by('-start_date')

    context = {
        'all_calendar': all_calendar,
        'form': form,
        'tables': tables,
    }
    return render(request, 'table/create_table.html', context)


@login_required
def edit_table(request, event_id):
    """Удаление добавленных дежурств."""
    event = Event.objects.get(event_id=event_id)
    event.delete()
    return redirect('table:create_table')


def analytics(request):
    """Аналитика дежурств"""
    if "month" in request.GET:
        selected_calendar = request.GET["month"]
    else:
        now = datetime.datetime.now()
        selected_calendar = int(now.month)

    # выводим форму выбора месяца, с текущим месяцем
    month = get_object_or_404(Month, month=selected_calendar)
    all_calendar = MonthForm(
        request.POST or None,
        instance=month
    )

    analytics_event = Event.objects.filter(month=selected_calendar)

    analytics_workers = {}
    charts_data = {}
    count_id = 0

    for workers in Workers.objects.all():
        count_works = Event.objects.filter(month=selected_calendar, title=workers).count()
        analytics_workers[workers] = count_works

        charts_data[count_id] = {
            'name': workers,
            'data': count_works,
        }
        count_id = count_id + 1
    print(month)
    context = {
        'all_calendar': all_calendar,
        'analytics_event': analytics_event,
        'analytics_workers': analytics_workers,
        'charts_data': charts_data,
    }
    return render(request, 'table/analytics.html', context)

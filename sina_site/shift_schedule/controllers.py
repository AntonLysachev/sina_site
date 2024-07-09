from datetime import timedelta, date
from django.forms import formset_factory
from .models import Shift
from .forms import ShiftForm, BaseShiftDayFormset
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
import calendar
import copy
import datetime


def week_as_str(shift: Shift) -> str:
    date = shift.date
    day = date.weekday()
    week_start = date - timedelta(days=day)
    week_end = week_start + timedelta(days=6)
    return f'{week_start.strftime("%d-%m-%Y")} - {week_end.strftime("%d-%m-%Y")}'


def group_weeks_from_shifts(shifts: QuerySet) -> dict:
    weeks = {}
    for shift in shifts:
        week = week_as_str(shift)
        weeks[week] = {}
    return weeks


def workers_as_dict() -> dict:
    workers = User.objects.all()
    workers_in_dict = {}
    for worker in workers:
        name = f'{worker.first_name} {worker.last_name}'
        id = worker.id
        workers_in_dict[name] = {'user_id': id}
        workers_in_dict[name]['days'] = {i: [] for i, day in enumerate(calendar.day_name)}
    return workers_in_dict


def group_weeks(shifts: QuerySet) -> dict:
    weekly_shifts = {}
    workers = workers_as_dict()
    weeks = group_weeks_from_shifts(shifts)
    for week in weeks:
        weekly_shifts[week] = copy.deepcopy(workers)
    return weekly_shifts


def group_shifts() -> dict:
    shifts = Shift.objects.all().order_by('-date')
    if shifts:
        weekly_shifts = group_weeks(shifts)
        for shift in shifts:
            worker = f'{shift.worker.first_name} {shift.worker.last_name}'
            type_shift = shift.shift
            date = shift.date
            day = date.weekday()
            week = week_as_str(shift)
            weekly_shifts[week][worker]['days'][day].append(type_shift)
    else:
        weekly_shifts = {}
    return weekly_shifts


def get_weeks_for_year(year):
    weeks = []
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    today = date.today()
    current_date = start_date
    while current_date <= end_date:
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        color = week_end > today
        if week_start <= today and week_end >= today:
            color = None
        weeks.append((f"{week_start.strftime('%d-%m-%Y')} - {week_end.strftime('%d-%m-%Y')}", color))
        current_date += timedelta(days=7)

    return weeks


def get_dates_of_week(week_start: date):
    dates = []
    days = tuple((i, day) for i, day in enumerate(calendar.day_name))
    for number, day in days:
        dates.append((day, week_start + timedelta(days=number)))
    return dates


def initialize_shift_formsets(start_date: datetime, request=None) -> dict:

    workers = User.objects.filter(is_active=True)
    dates = [start_date + timedelta(days=i) for i in range(7)]
    initial = []
    for worker in workers:
        for date in dates:
            shifts = Shift.objects.filter(date=date, worker=worker)
            shift_1 = shifts.filter(shift=1).exists()
            shift_2 = shifts.filter(shift=2).exists()
            initial.append({"worker": worker,
                            "date": date,
                            'shift_1': shift_1,
                            'shift_2': shift_2,
                            'state_1': shift_1,
                            'state_2': shift_2})

    ShiftDayFormset = formset_factory(ShiftForm, extra=0, formset=BaseShiftDayFormset)
    formset = ShiftDayFormset(request, initial=initial)
    formsets = [formset[i:i + 7] for i in range(0, len(formset), 7)]
    management_form = formset.management_form

    return {'formset': formset, 'formsets': formsets, 'management_form': management_form}

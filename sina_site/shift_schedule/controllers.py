from datetime import timedelta
from .models import Shift
from .forms import ShiftForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.query import QuerySet
import calendar
import copy


def week_as_str(shift: Shift) -> str:
    date = shift.date
    day = date.weekday()
    week_start = date - timedelta(days=day)
    week_end = week_start + timedelta(days=6)
    return f'{week_start} - {week_end}'


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


def group_shifts(shifts: QuerySet) -> dict:
    weekly_shifts  = group_weeks(shifts)
    for shift in shifts:
        worker = f'{shift.worker.first_name} {shift.worker.last_name}'
        type_shift = shift.shift
        date = shift.date
        day = date.weekday()
        week = week_as_str(shift)
        weekly_shifts[week][worker]['days'][day].append(type_shift)
    return weekly_shifts


def group_forms_for_week(users: User) -> dict:
    forms = {}
    for user in users:
        id = user.id
        name = f'{user.first_name} {user.last_name}'
        forms[name] = []
        for i in range(0, 7):
            form = ShiftForm(choices=[(f'{id}.{i}.1', f"{_('Shift')} 1"), (f'{id}.{i}.2', f"{_('Shift')} 2")])
            forms[name].append(form)
    return forms


def group_for_update(group: dict) -> dict:
    forms = {}
    for week, worker in group.items():
        for name, meta in worker.items():
            forms[name]= []
            id = meta['user_id']
            for day, shifts in meta['days'].items():
                selected = []
                for shift in shifts:
                    selected.append(f'{id}.{day}.{shift}')
                form = ShiftForm(choices=[(f'{id}.{day}.1', f"{_('Shift')} 1"), (f'{id}.{day}.2', f"{_('Shift')} 2")], selected=selected)
                forms[name].append(form)
    return forms


def add_shifts(shifts, date_from):
    day_of_week = date_from.weekday()
    start_of_week = date_from - timedelta(days=day_of_week)

    for shift in shifts:
        client_id, day, type = map(int, shift.split('.'))
        worker = User.objects.get(id=client_id)
        date = start_of_week + timedelta(days=day)
        try:
            Shift.objects.create(date=date, shift=type, worker=worker)
        except IntegrityError as e:
            raise e


def update_shifts(shifts, date_from):
    day_of_week = date_from.weekday()
    start_of_week = date_from - timedelta(days=day_of_week)
    end_of_week = start_of_week + timedelta(days=6)
    existing_shifts = Shift.objects.filter(date__range=[start_of_week, end_of_week])
    for_comparison = []

    for shift in shifts:
        client_id, day, type = map(int, shift.split('.'))
        worker = User.objects.get(id=client_id)
        date = start_of_week + timedelta(days=day)
        is_exists = Shift.objects.filter(date=date, shift=type, worker=worker)
        if is_exists.exists():
            shift_id = is_exists.first().id
            for_comparison.append(shift_id)
        else:
            try:
                shift = Shift.objects.create(date=date, shift=type, worker=worker)
                for_comparison.append(shift.id)
            except IntegrityError as e:
                if "(date, shift)" in str(e):
                    shift = Shift.objects.get(date=date, shift=type)
                    id = shift.id
                    shift.worker = worker
                    shift.save()
                    for_comparison.append(id)

    shifts_to_delete = existing_shifts.exclude(id__in=for_comparison)
    for shift in shifts_to_delete:
        shift.delete()


def validation_shifts(shifts):
    valid_shifts = []
    for shift in shifts:
        meta = shift[2:]
        if meta in valid_shifts:
            return False
        valid_shifts.append(meta)
    return True

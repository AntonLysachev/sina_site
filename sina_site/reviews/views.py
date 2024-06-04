from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from sina_site.mixins import LoginRequiredMixin
from sina_site.reviews.models import Review
from .forms import ReviewsFilterForm

class ReviewsIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = ReviewsFilterForm(request.GET)
        reviews = Review.objects.all()
        if form.is_valid():
            if form.cleaned_data['type_full']:
                reviews = reviews.filter(type="full")
            if form.cleaned_data['type_only_grade']:
                reviews = reviews.filter(type="only_grade")
        return render(request, 'reviews/index.html', context={'reviews': reviews, 'form': form})

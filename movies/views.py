from django.shortcuts import render
from django.conf import settings


def landing_page(request):
    category = request.GET.get("category", "popular")

    API_KEY = settings.TMDB_API_KEY
    return render(request, "movies/landing_page.html")

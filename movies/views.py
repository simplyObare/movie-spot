from django.shortcuts import render
from django.conf import settings
import requests


def landing_page(request):
    category = request.GET.get("category", "popular")

    API_KEY = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3/movie/"
    url = f"{base_url}{category}?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json().get("results", [])
    print(data)

    return render(
        request, "movies/landing_page.html", {"movies": data, "category": category}
    )

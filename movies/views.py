from django.shortcuts import render
from django.conf import settings
import requests


def landing_page(request):
    category = request.GET.get("category", "popular")
    search_query = request.GET.get("search", "")

    API_KEY = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3/movie/"
    error_message = ""

    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={search_query}&page=1&include_adult=false"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&language=en-US&page=1"
    try:
        response = requests.get(url)
        data = response.json().get("results", [])
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TMDB API: {e}")
        data = []
        error_message = "Error fetching data from TMDB API. Please try again later."

    if request.headers.get("HX-Request"):
        return render(
            request,
            "movies/partials/movie_list.html",
            {
                "movies": data,
                "category": category,
                "search_query": search_query,
                "error_message": error_message,
            },
        )

    return render(
        request,
        "movies/landing_page.html",
        {
            "movies": data,
            "category": category,
            "search_query": search_query,
            "error_message": error_message,
        },
    )

from django.shortcuts import render
from django.conf import settings
import requests

API_KEY = settings.TMDB_API_KEY


def landing_page(request):
    category = request.GET.get("category", "popular")
    search_query = request.GET.get("search", "")
    page = int(request.GET.get("page", 1))
    next_page = page + 1

    base_url = "https://api.themoviedb.org/3/movie/"
    error_message = ""

    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={search_query}&page={page}&include_adult=false"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&language=en-US&page={page}"
    try:
        response = requests.get(url)
        data = response.json().get("results", [])
        print(data)
        total_pages = response.json().get("total_pages", 1)
        has_next_page = page < total_pages
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TMDB API: {e}")
        data = []
        error_message = "Error fetching data from TMDB API. Please try again later."
        has_next_page = False

    if request.headers.get("HX-Request"):
        return render(
            request,
            "movies/partials/movie_list.html",
            {
                "movies": data,
                "category": category,
                "search_query": search_query,
                "error_message": error_message,
                "next_page": next_page,
                "has_next_page": has_next_page,
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
            "next_page": next_page,
            "has_next_page": has_next_page,
        },
    )


def movie_detail(request, movie_id):
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    movie_credit_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"
    error_message = ""

    try:
        movie_detail_response = requests.get(movie_detail_url)
        movie_data = movie_detail_response.json()
        print(movie_data)
    except requests.exceptions.RequestException as e:
        movie_data = []
        error_message = (
            "Error fetching movie details from TMDB API. Please try again later."
        )

    try:
        movie_credit_response = requests.get(movie_credit_url)
        movie_credits = movie_credit_response.json()
        print(movie_credits)
    except requests.exceptions.RequestException as e:
        movie_credits = []
        error_message = (
            "Error fetching movie credits from TMDB API. Please try again later."
        )

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie_data": movie_data,
            "error_message": error_message,
            "movie_credits": movie_credits,
        },
    )

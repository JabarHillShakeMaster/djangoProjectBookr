from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Review, Contributor
from .utils import average_rating
from django.db import models
from .forms import SearchForm

def index(request):
    # name = "world"
    # search = request.GET.get("search") or "</html>"
    # name = "world"
    # search = request.GET.get("search")
    # invalid_name =
    # name = HttpResponse
    # return HttpResponse("Hello, {}!".format(name))
    # , HttpResponse("{}".format(search))
    # return HttpResponse(name)
    return render(request, "base.html")

"""def searchResult(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.clearn_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)
            for contributors in fname_contributors:
                for book in contributors.book_set.all():
                    books.add(book)
            lname_contributors = Contributor.objects.filter(last_name__icontrains=search)
            for contributors in lname_contributors:
                for book in contributors.book_set.all():
                    books.add(book)

    return render(request, "search-result.html", {"form": form, "search_text": search_text, "books": books})

def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1> \
              <p>{Book.objects.count()} books and counting!</p></html>"
              
    return render(request, 'base.html')#HttpResponse(message)
"""

def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)
            for contributors in fname_contributors:
                for book in contributors.book_set.all():
                    books.add(book)
            lname_contributors = Contributor.objects.filter(last_name__icontrains=search)
            for contributors in lname_contributors:
                for book in contributors.book_set.all():
                    books.add(book)

    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "books": books})

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
            book_list.append({'book':book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})
    context = {
        'book_list': book_list
    }
    return render(request, 'reviews/books_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            'book': book,
            'book_rating': book_rating,
            'review': reviews
        }
    else:
        context = {
            'book': book,
            'book_rating': None,
            'review': None
        }
    return render(request, 'reviews/bookDetailView.html', context)

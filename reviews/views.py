from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Review
from .utils import average_rating
from django.db import models

def index(request):
    name = "world"
    # search = request.GET.get("search") or "</html>"
    # name = "world"
    # search = request.GET.get("search")
    # invalid_name =
    # name = HttpResponse
    # return HttpResponse("Hello, {}!".format(name))
    # , HttpResponse("{}".format(search))
    #return HttpResponse(name)
    return render(request, "base.html", {"name": name})

def searchResult(request):
    search = request.GET.get("search") or "</html>"

    return render(request, "searchResult.html", {"search": search})


"""def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1> \
              <p>{Book.objects.count()} books and counting!</p></html>"
              
    return render(request, 'base.html')#HttpResponse(message)
"""

def book_search():
    return render()
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

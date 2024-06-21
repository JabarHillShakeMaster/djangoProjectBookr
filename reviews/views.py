from django.http import HttpResponse
from .models import Book, Review, Contributor, Contributor, Publisher
from django.db import models
from .forms import PublisherForm, SearchForm, ReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .utils import average_rating

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
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request, "reviews/bookDetailView.html", context)

def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": publisher, "model_type": "Publisher"})

def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(book))

            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": book,
                   "related_model_type": "Book"
                   })
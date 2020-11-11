import requests

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin, DeleteView

from .forms import SearchBookForm, AddBookForm, SearchBookForImportForm
from .models.books import Book
from library.settings import API_KEY, GOOGLE_API


class BookListView(FormMixin, ListView):
    template_name = "book_list.html"
    form_class = SearchBookForm
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.queryset = Book.objects.all()
        form = SearchBookForm()
        if len(request.GET) != 0:
            form = SearchBookForm(request.GET)
            if form.is_valid():
                if request.GET["title"]:
                    self.queryset = Book.objects.filter(title=request.GET["title"])
                if request.GET["author"]:
                    self.queryset = self.queryset.filter(author=request.GET["author"])
                if request.GET["language"]:
                    self.queryset = self.queryset.filter(
                        language=request.GET["language"]
                    )
                if request.GET["lower_date"] != "-":
                    self.queryset = self.queryset.filter(
                        publication_date__gte=request.GET["lower_date"]
                    )
                if request.GET["higher_date"] != "-":
                    self.queryset = self.queryset.filter(
                        publication_date__lte=request.GET["higher_date"]
                    )
        return render(
            request, self.template_name, {"books": self.queryset, "form": form}
        )


class BookView(View):
    template_name = "add_book.html"
    form_class = AddBookForm
    success_url = reverse_lazy("books_list")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if kwargs:
                book = get_object_or_404(Book, pk=int(kwargs["pk"]))
                book.title = form.cleaned_data["title"]
                book.author = form.cleaned_data["author"]
                book.publication_date = form.cleaned_data["publication_date"]
                book.ISBN_number = form.cleaned_data["ISBN_number"]
                book.number_of_pages = form.cleaned_data["number_of_pages"]
                book.link_to_cover = form.cleaned_data["link_to_cover"]
                book.language = form.cleaned_data["language"]
                book.save()
            else:
                book = form.save(commit=True)
                book.save()
            books = Book.objects.all()
            form = SearchBookForm()
            return render(request, "book_list.html", {"books": books, "form": form})
        return render(request, "add_book.html", {"form": form})

    def get(self, request, *args, **kwargs):
        if kwargs:
            book = get_object_or_404(Book, pk=int(kwargs["pk"]))
            form = self.form_class(instance=book)
            return render(request, "add_book.html", {"form": form})
        return render(request, "add_book.html", {"form": self.form_class})


class DeleteBookView(DeleteView):
    model = Book

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=int(kwargs["pk"]))
        book.delete()
        books = Book.objects.all()
        form = SearchBookForm()
        return render(request, "book_list.html", {"books": books, "form": form})


class ImportGoogleBookView(View):
    form_class = SearchBookForImportForm
    template_name = "import_book_list.html"

    def get_params_for_request(self, **kwargs):
        found = False
        params = {}
        params["key"] = API_KEY
        params["q"] = ""
        for key, value in kwargs.items():
            if key != "csrfmiddlewaretoken":
                if value != "":
                    if not found:
                        params["q"] = value
                        found = True
                    if key in ["title", "author", "publisher"]:
                        params["q"] += "+in" + key + ":" + value
                    else:
                        params["q"] += "+" + key + ":" + value
        return params

    def get_data_from_api(self, **kwargs):
        google_books = requests.get(
            f"{GOOGLE_API}", params=self.get_params_for_request(**kwargs)
        )
        return google_books

    def get_isbn_number(self, data):
        identifiers_list = data.get("industryIdentifiers", None)
        isbn_number = ""
        if identifiers_list is not None:
            for identifier in identifiers_list:
                if identifier.get("type") in ["ISBN_13", "ISBN_10"]:
                    isbn_number += identifier.get("identifier") + " "
        return isbn_number

    def add_book_to_library(self, books):
        data = []
        for book in books:
            book = book["volumeInfo"]
            image_links = book.get("imageLinks", None)
            title = book.get("title", None)
            if image_links is not None:
                image_links = image_links.get("thumbnail", None)
            published_date = book.get("publishedDate", None)
            if published_date is not None:
                published_date = published_date[:4]
            author = book.get("authors", None)
            if author is not None:
                author = ",".join(author)
            book_dict = {}
            book_dict["title"] = title
            book_dict["author"] = author
            book_dict["image_link"] = image_links
            data.append(book_dict)
            Book.objects.get_or_create(
                title=title,
                author=author,
                publication_date=published_date,
                number_of_pages=book.get("pageCount", None),
                language=book.get("language", None),
                link_to_cover=image_links,
                ISBN_number=self.get_isbn_number(book),
            )
        return data

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            books = self.get_data_from_api(**form.cleaned_data)
            if books.status_code == 200:
                if books.json()["totalItems"] != 0:
                    imported_books = self.add_book_to_library(books.json()["items"])
                    return render(
                        request,
                        self.template_name,
                        {"books": imported_books, "form": form},
                    )
            return render(
                request, self.template_name, {"form": form, "imported": False}
            )

        return render(request, self.template_name, {"form": form, "imported": False})

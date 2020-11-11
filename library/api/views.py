from rest_framework import viewsets

from .serialize import BookSerializer
from books.models.books import Book


class BookApiView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_queryset(self):
        title = self.request.query_params.get("title", None)
        author = self.request.query_params.get("author", None)
        language = self.request.query_params.get("language", None)
        lower_date = self.request.query_params.get("lower_date", None)
        higher_date = self.request.query_params.get("higher_date", None)
        if title is not None:
            queryset = self.queryset.filter(title=title)
        if author is not None:
            queryset = self.queryset.filter(author=author)
        if language is not None:
            queryset = self.queryset.filter(language=language)
        if lower_date is not None:
            queryset = self.queryset.filter(publication_date__gte=lower_date)
        if higher_date is not None:
            queryset = self.queryset.filter(publication_date__lte=higher_date)

        return queryset

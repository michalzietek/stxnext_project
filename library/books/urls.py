from django.urls import path, re_path
from .views import ImportGoogleBookView, BookListView, BookView, DeleteBookView

urlpatterns = [
    path("", BookListView.as_view(), name="books_list"),
    re_path(r"^edit/(?P<pk>[^\.]+)/$", BookView.as_view(), name="edit_book"),
    re_path(r"^delete/(?P<pk>[^\.]+)/$", DeleteBookView.as_view(), name="delete_book"),
    re_path(r"^add/$", BookView.as_view(), name="add_book"),
    re_path(r"^import/$", ImportGoogleBookView.as_view(), name="import_book"),
]

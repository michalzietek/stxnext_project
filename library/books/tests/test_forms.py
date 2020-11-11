from django.test import TestCase

from ..forms import SearchBookForm, AddBookForm, SearchBookForImportForm


class TestForms(TestCase):
    def test_search_book_form_valid(self):
        form = SearchBookForm(
            data={"title": "title", "author": "author", "language": "language"}
        )

        self.assertTrue(form.is_valid())

    def test_add_book_form_valid(self):
        form = AddBookForm(
            data={
                "title": "title",
                "author": "author",
                "publication_date": 2020,
                "ISBN_number": "1111111111",
                "number_of_pages": 1,
                "link_to_cover": "link_to_cover",
                "language": "language",
            }
        )

        self.assertTrue(form.is_valid())

    def test_add_book_form_invalid(self):

        form = AddBookForm()

        self.assertFalse(form.is_valid())

    def test_google_search_book_form_valid(self):
        form = SearchBookForImportForm(
            data={
                "title": "title",
                "author": "author",
                "publisher": "publisher",
                "isbn": "1111111111",
                "subject": "subject",
                "lccn": "lccn",
                "oclc": "oclc",
            }
        )

        self.assertTrue(form.is_valid())

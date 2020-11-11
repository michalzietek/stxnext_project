from django.test import TestCase, Client
from django.urls import reverse

from ..models.books import Book


class TestsBookListView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.list_url = reverse("books_list")

    def test_book_list_GET(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")


class TestBookView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.add_book_url = reverse("add_book")
        self.books_list_url = reverse("books_list")
        self.book = Book.objects.create(
            title="title",
            author="author",
            publication_date=2020,
            ISBN_number="1111111111",
            number_of_pages=1,
            link_to_cover="link_to_cover",
            language="language",
        )

    def test_add_book_GET(self):

        response = self.client.get(self.add_book_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_book.html")

    def test_add_book_POST(self):

        response = self.client.post(
            self.add_book_url,
            {
                "title": "title",
                "author": "author",
                "publication_date": 2020,
                "ISBN_number": "1111111111",
                "number_of_pages": 1,
                "link_to_cover": "link_to_cover",
                "language": "language",
            },
        )

        self.assertTemplateUsed(response, "book_list.html")
        self.assertEqual(response.status_code, 200)

    def test_add_book_POST_no_data(self):

        response = self.client.post(self.add_book_url)

        self.assertEqual(response.status_code, 200)

    def test_book_EDIT(self):

        response = self.client.post(
            reverse("edit_book", args=[self.book.pk]),
            {
                "title": "title1",
                "author": "author",
                "publication_date": 2020,
                "ISBN_number": "1111111111",
                "number_of_pages": 1,
                "link_to_cover": "link_to_cover",
                "language": "language",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_book_DELETE(self):

        response = self.client.post(reverse("delete_book", args=[self.book.pk]))

        self.assertEqual(Book.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


class TestImportGoogleBookView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.import_url = reverse("import_book")

    def test_import_book_from_google_GET(self):

        response = self.client.get(self.import_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "import_book_list.html")

    def test_import_book_from_google_POST(self):

        response = self.client.post(
            self.import_url,
            {
                "title": "title",
                "author": "author",
                "publisher": "publisher",
                "isbn": "1111111111",
                "subject": "subject",
                "lccn": "lccn",
                "oclc": "oclc",
            },
        )

        self.assertTemplateUsed(response, "import_book_list.html")
        self.assertEqual(response.status_code, 200)

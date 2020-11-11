import datetime

from django import forms
from django.forms import ModelForm
from django.forms.widgets import Input

from .models.books import Book


def year_choices():
    return [("-", "-")] + [
        (year, year) for year in range(868, datetime.date.today().year + 1)
    ]


class SearchBookForm(forms.Form):
    title = forms.CharField(label="Title")
    author = forms.CharField(label="Author")
    language = forms.CharField(label="Language")
    lower_date = forms.ChoiceField(
        label="From date",
        choices=year_choices(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    higher_date = forms.ChoiceField(
        label="To date",
        choices=year_choices(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super(SearchBookForm, self).__init__(*args, **kwargs)

        self.fields["title"].required = False
        self.fields["author"].required = False
        self.fields["lower_date"].required = False
        self.fields["higher_date"].required = False
        self.fields["language"].required = False

    def clean(self):
        if (
            self.cleaned_data.get("higher_date") != "-"
            and self.cleaned_data.get("lower_date") != "-"
        ):
            if self.cleaned_data.get("higher_date") < self.cleaned_data.get(
                "lower_date"
            ):
                self.errors.update({"lower_date": "Selected dates are invalid"})


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "ISBN_number",
            "language",
            "link_to_cover",
            "publication_date",
            "number_of_pages",
        ]
        widgets = {
            "link_to_cover": Input(),
            "publication_date": forms.Select(
                choices=year_choices(), attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields["author"].required = False
        self.fields["ISBN_number"].required = False
        self.fields["link_to_cover"].required = False
        self.fields["language"].required = False
        self.fields["publication_date"].required = False
        self.fields["number_of_pages"].required = False

    def check_isbn_number(self, isbn_number):
        for character in isbn_number:
            if not character.isdigit() and character != "X":
                return False
        return True

    def clean(self):
        if self.cleaned_data.get("ISBN_number", None):
            isbn_number_list = self.cleaned_data.get("ISBN_number").split(" ")
            for number in isbn_number_list:
                if not number.isnumeric() and not self.check_isbn_number(number):
                    self.errors.update({"ISBN_number": "ISBN number must be a number"})
                elif len(number) != 10 and len(number) != 13:
                    self.errors.update(
                        {"ISBN_number": "ISBN number must be a 10 or 13 digit number"}
                    )


class SearchBookForImportForm(forms.Form):
    title = forms.CharField(label="Title")
    author = forms.CharField(label="Author")
    publisher = forms.CharField(label="Publisher")
    subject = forms.CharField(label="Subject")
    isbn = forms.CharField(label="ISBN Number")
    lccn = forms.CharField(label="Library of Congress Control Number")
    oclc = forms.CharField(label="Online Computer Library Center number")

    def __init__(self, *args, **kwargs):
        super(SearchBookForImportForm, self).__init__(*args, **kwargs)

        self.fields["title"].required = False
        self.fields["author"].required = False
        self.fields["publisher"].required = False
        self.fields["subject"].required = False
        self.fields["isbn"].required = False
        self.fields["lccn"].required = False
        self.fields["oclc"].required = False

from django.forms import ModelForm
from . models import Book


# Create the form class.
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

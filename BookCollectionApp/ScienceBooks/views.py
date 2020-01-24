from django.shortcuts import render, redirect, get_object_or_404
from .models import Book          #import the class of Book to be able to use object definition
from .forms import BookForm       #import the Book Form to be able to create and save
import requests
import json
import datetime                     #used for passing dates in easy to display format
from django.utils import timezone   #used for converting time from UTC to users time zone
from bs4 import BeautifulSoup as BS #necessary for datascraping




#View function that renders the home page
def home(request):
    return render(request, "ScienceBooks/books_home.html")


#View function that controls the main index page - list of books
def index(request):
    get_books = Book.Books.all()        #Gets all the current books from the database
    context = {'books': get_books}      #Creates a dictionary object of all the books for the template
    return render(request, 'ScienceBooks/books_index.html', context)


#View function to add a new book to the database
def add_book(request):
    form = BookForm(request.POST or None)     #Gets the posted form, if one exists
    if form.is_valid():                         #Checks the form for errors, to make sure it's filled in
        form.save()                             #Saves the valid form/book to the database
        return redirect('listBooks')            #Redirects to the index page
    else:
        print(form.errors)                      #Prints any errors for the posted form to the terminal
        form = BookForm()                       #Creates a new blank form
    return render(request, 'ScienceBooks/books_create.html', {'form':form})


#View function to look up the details of a book
def details_book(request, pk):
    pk = int(pk)                               #Casts value of pk to an int so it's in the proper form
    book = get_object_or_404(Book, pk=pk)      #Gets single instance of the book from the database
    context={'book':book}                      #Creates dictionary object to pass the book object
    return render(request, 'ScienceBooks/books_details.html', context)


#View function to edit the details of a book
def edit_book(request, pk):
    pk = int(pk)                               #Casts value of pk to an int so it's in the proper form
    book = get_object_or_404(Book, pk=pk)      #Gets single instance of the book from the database
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('bookDetails', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'ScienceBooks/books_edit.html', {'form': form})


#View function to delete a book
def delete_book(request, pk):
    pk = int(pk)                               #Casts value of pk to an int so it's in the proper form
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('listBooks')
    context = {'book':book}
    return render(request, 'ScienceBooks/books_delete.html', context)



#def api_response(request):

 #   response = requests.get('https://www.googleapis.com/books/v1/volumes?q=&key=AIzaSyB2L-26ep0cgV1qHbVARIzHWKBekHnHE6g')
  #  bookdata = response.json()
   # context = {'bookdata': bookdata}
    #return render(request, 'ScienceBooks/books_api.html', context)



#View function to connect to the API and extract JSON response
def api_response(request):
    book = {}
    if 'search_terms' in request.GET:
        search_terms = request.GET['search_terms']
        url = 'https://www.googleapis.com/books/v1/volumes?q=%s&key=AIzaSyB2L-26ep0cgV1qHbVARIzHWKBekHnHE6g' % search_terms
        response = requests.get(url)
        book = response.json()
        request.session['book_data'] = book
    return render(request, 'ScienceBooks/books_api.html', {'book': book})



#View function for data scraping the Google website for current news stories
def google_news(request):
    page=requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen")
    soup = BS(page.content, 'html.parser')  # Initial processing of the html by beautiful soup, soup is now a navigatable object
    nodes = soup.find_all('h3', class_='ipQwMb ekueJc RD0gLb')  # Search for h3 elements
    articles = []  # Create blank list to add articles to
    for node in nodes:  # Iterates through all the h3 elements with class 'ipQwMb ekueJc RD0gLb'
        title = node.find('a').get_text()  # Sets title equal to the text of the a tag
        link = node.find('a').get('href')  # Sets link equal to the href of the a tag
        url = "https://news.google.com" + link  # Modifies the link to a full url, since the links were relative
        timedivs = node.find_next_siblings('div', class_='QmrVtf RD0gLb')
        for timediv in timedivs:
            timestamp = timediv.find('time').get_text() # Gets the time of each article
            article = {'title': title, 'url': url, 'date': timestamp}  # Creates an article object dictionary with needed elements
            articles.append(article)  # Adds article dictionary item to the list before iterating through next node
    context = {'articles': articles}  # Creates a dictionary element for the articles to pass to the template
    return render(request, 'ScienceBooks/google_news.html', context)


def add_api_book(request):
    if request.method == 'POST' and 'btn2' in request.POST:
        print(request.POST)
        id = request.POST.get('btn2')
        print(id)
        data = request.session['book_data']
        dict={}
        for i in data['items']:
            book_id = (i['id'])
            if id == book_id:
                title = (i['volumeInfo']['title'])
                author = (i['volumeInfo']['authors'])
                published = (i['volumeInfo']['publishedDate'])
                try:
                    reviews = (i['volumeInfo']['averageRating'])
                except KeyError:
                    reviews = None
                dict = {'title': title, 'authors': author, 'publication_date': published, 'google_reviews':reviews}
                print(dict)
        form = BookForm(request.POST or None)
        form = BookForm(dict)
        if form.is_valid:
            form.save()
            return redirect('listBooks')
        else:
            print(form.errors)
            form = BookForm(dict)
        return render(request, 'ScienceBooks/books_create.html', {'form': form} )



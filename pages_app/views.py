from django.shortcuts import render
import pandas as pd
from pages_app.models import BookClass, OneBook

# group function used in >>>>
from pages_app.pandas_postgres import get_books_data_frame


def group(books, bt):
    index = 0;
    book_list = []
    for book_type in bt:
        if book_type != "NONE":
            gk = books.groupby('genres')
            df4 = gk.get_group(book_type)
            df5 = df4.groupby('rating')
            max_rating = max(df5.rating)
            df6 = df5.get_group(max_rating[0])

            book_obj = OneBook()
            book_obj.title = df6.title.values[index]
            book_obj.writer = df6.writer.values[index]
            book_obj.genres = df6.genres.values[index]
            book_obj.page_num = df6.page_num.values[index]
            book_obj.pub_year = df6.pub_year.values[index]
            book_obj.rating = df6.rating.values[index]
            book_obj.image_url = df6.image_url.values[index].lower()
            book_obj.isbn = df6.isbn.values[index]
            book_list.append(book_obj)
            index += 1

    return book_list


def group2(books, bt):
    gk = books.groupby('genres')
    df4 = gk.get_group(bt)
    df5 = df4.groupby('rating')
    max_rating = max(df5.rating)
    df6 = df5.get_group(max_rating[0])
    book_list = []
    for x in range(4):
        book_obj = OneBook()
        book_obj.title = df6.title.values[x]
        book_obj.writer = df6.writer.values[x]
        book_obj.genres = df6.genres.values[x]
        book_obj.page_num = df6.page_num.values[x]
        book_obj.pub_year = df6.pub_year.values[x]
        book_obj.rating = df6.rating.values[x]
        book_obj.image_url = df6.image_url.values[x].lower()
        book_obj.isbn = df6.isbn.values[x]
        book_list.append(book_obj)
    return book_list


# home page function renders index.html and returns response
def login(request):
    return render(request, 'pages/login.html')


# home page function renders index.html and returns response
def home(request):
    books = BookClass.objects.all().order_by('-id')[:6]

    book = []
    for i in range(6):
        book_obj = OneBook()
        book_obj.title = books[i].title
        book_obj.writer = books[i].writer
        book_obj.genres = books[i].genres
        book_obj.page_num = books[i].page_num
        book_obj.pub_year = books[i].pub_year
        book_obj.rating = books[i].rating
        book_obj.image_url = books[i].image_url
        book_obj.isbn = books[i].isbn
        book.append(book_obj)
    return render(request, 'pages/index.html', {'book': book})


# find out user choise and redirect to relevant page.
def user_choise(request):
    books = BookClass.objects.all().order_by('-id')[:6]
    if 'yes_enter' in request.POST:
        return render(request, 'pages/inter_book.html', {'books': books})
    elif 'no_enter' in request.POST:
        return render(request, 'pages/not_inter_book.html', {'books': books})


# our user_chose page view
def result1(request):
    books = pd.read_csv("bookworm_data.csv")

    # books = get_books_data_frame()

    if 'book1_type' in request.POST:
        bt = request.POST['book1_type'].upper()
    else:
        bt = ""
    if 'book1_type' in request.POST:
        bt2 = request.POST['book2_type'].upper()
    else:
        bt2 = ""
    if 'book3_type' in request.POST:
        bt3 = request.POST['book3_type'].upper()
    else:
        bt3 = ""
    if 'book4_type' in request.POST:
        bt4 = request.POST['book4_type'].upper()
    else:
        bt4 = ""
    if 'book5_type' in request.POST:
        bt5 = request.POST['book5_type'].upper()
    else:
        bt5 = ""

    books = books.loc[:, ["title", "writer", "genres", "page_num", "pub_year", "rating", "isbn", "image_url"]]
    books = books.applymap(lambda s: s.upper() if type(s) == str else s)
    book_types = []

    if bt == "NONE" and bt2 == "NONE" and bt3 == "NONE" and bt4 == "NONE" and bt5 == "NONE":
        return render(request, 'pages/NameError.html')

    book_types.append(bt)
    book_types.append(bt2)
    book_types.append(bt3)
    book_types.append(bt4)
    book_types.append(bt5)
    book = group(books, book_types)

    return render(request, 'pages/result.html', {'books': book})

def result2(request):
    books = pd.read_csv("bookworm_data.csv")
    # books = get_books_data_frame()

    books = books.loc[:, ["title", "writer", "isbn",
                          "page_num", "pub_year", "rating", "image_url", "genres"]]

    books = books.applymap(lambda s: s.upper() if type(s) == str else s)

    if request.method == 'POST':
        selected_types = request.POST.getlist('ckb')

    if len(selected_types) < 3:
        return render(request, 'pages/selected_book_error.html')
    else:
        bt = selected_types[0].upper()
        bt2 = selected_types[1].upper()
        bt3 = selected_types[2].upper()

    book_list = []
    temp = group2(books, bt)
    book_list.append(temp[0])
    book_list.append(temp[1])
    book_list.append(temp[2])
    book_list.append(temp[3])

    temp = group2(books, bt2)
    book_list.append(temp[0])
    book_list.append(temp[1])
    book_list.append(temp[2])
    book_list.append(temp[3])

    temp = group2(books, bt3)
    book_list.append(temp[0])
    book_list.append(temp[1])
    book_list.append(temp[2])
    book_list.append(temp[3])

    return render(request, 'pages/result.html', {'books': book_list})

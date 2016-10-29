from django.shortcuts import render, redirect, reverse
from .models import User, Book, Review
from django.contrib import messages


# ################    LOGIN / REGISTER      ###################

def login_reg(request):
    request.session.flush()
    return render(request, 'books/login_reg.html')

def register(request):
    if request.method == "POST":
        result = User.objects.createUser(
            name=request.POST['name'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            pw_hash=request.POST['password'], password_c=request.POST['password_c']
            )

        if result[0]:
            request.session['user'] = result[1]
            request.session['id'] = result[2]
            return redirect('books')

        else:
            messages.add_message(request, messages.INFO, result[1][0])
            return redirect('/')

def login(request):
    if request.method == "POST":
        result = User.objects.loginUser(
            email=request.POST['email'],
            pw_hash=request.POST['password']
            )

        if result[0]:
            request.session['user'] = result[1]
            request.session['id'] = result[2]
            return redirect('books')

        else:
            messages.add_message(request, messages.INFO, result[1][0])
            return redirect('/')

def logout(request):

    if  'user' in request.session:
        request.session.pop('user')
        messages.add_message(request, messages.INFO, "You are logged out")
        return redirect('/')

    else:
        messages.add_message(request, messages.INFO, "Already logged out")
        return redirect('/')

# ################    INDEX PAGE      ###################

def index(request):
    print('hit index')
    result = Review.objects.indexShow()

    context = {
        'index_item' : result
    }
    return render(request, 'books/index.html', context)

# ################    ADD / DELETE NEW      ###################

def add(request):

    context = {
        'books' : Book.objects.getAllBooks(),
    }
    return render(request, 'books/add.html', context)

def create(request):

    if request.method == 'POST':
        result = Review.objects.addBook_and_Review(
            user=request.session['id'],
            title=request.POST['title'],
            new_title=request.POST['new_title'],
            author=request.POST['author'],
            new_author=request.POST['new_author'],
            review=request.POST['review'],
            rating=request.POST['rating']
        )

        if not result[0]:
            messages.add_message(request, messages.INFO, result[1][0])
            return redirect('add')
        else:
            return redirect(reverse('show', kwargs={'id':result[1].book.id}))

def add_new_review(request):

    if request.method == 'POST':
        result = Review.objects.addNewReview(
            user=request.POST['user_id'],
            book=request.POST['book_id'],
            review=request.POST['review'],
            rating=request.POST['rating']
        )

        return redirect(reverse('show', kwargs={'id':result[1].book.id}))

def delete_review(request, id):

    if request.method == 'POST':
        result = Review.objects.deleteReview(
            user=request.POST['user_id'],
            review_id=request.POST['review_id'],
            book_id=request.POST['book_id']
        )

        if result[0]:
            messages.add_message(request, messages.INFO, result[1][0])
            return redirect(reverse('show', kwargs={'id':request.POST['book_id']}))
        else:
            return redirect(reverse('show', kwargs={'id':request.POST['book_id']}))

# ################    SHOW BOOK / USER     ###################

def show(request, id):

    context = {

        'id': id,
        'show_books': Book.objects.getShowBooks(id)[0],
        'show_reviews': Review.objects.getShowReviews(id)
        }

    return render(request, 'books/show.html', context)

def show_user(request, id):
    if request.method == "POST":
        context = {
            'user' : User.objects.get(id=request.POST['user_id']),
            'books' : Book.objects.getBooks(request.POST['user_id'])[:5],
            'count' : len(Book.objects.getBooks(request.POST['user_id']))
        }
        return render(request, 'books/show_user.html', context)

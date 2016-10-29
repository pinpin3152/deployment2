from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

#https://docs.djangoproject.com/en/1.10/ref/models/fields/#mode-field-types

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):

   def createUser(self, **kwargs):
      errors = False
      error_list = []
      kwargs['name'] = kwargs['name'].replace(" ", "")

      if not kwargs['name'].isalpha():
         error_list.append("Name should be present and at least 1 letter")
         errors = True

      if not kwargs['alias'].isalpha():
         error_list.append("Alias should be present and at least 1 letter")
         errors = True

      if not kwargs['email']:
         error_list.append("Email is required")
         errors = True

      if not EMAIL_REGEX.match(kwargs['email']):
         error_list.append("Not a valid email")
         errors = True

      if User.objects.filter(email=kwargs['email']):
         error_list.append("Email already in use")
         errors = True

      if not len(kwargs['pw_hash']) >= 8:
         error_list.append("Password need to be at least 8 characters ")
         errors = True

      if not kwargs['pw_hash'] == kwargs['password_c']:
         error_list.append("Password & Confirmation dont match")
         errors = True

      if len(error_list) == 0:
         kwargs['pw_hash'] = kwargs['pw_hash'].encode('utf-8')
         pw_hash = bcrypt.hashpw(
         kwargs['pw_hash'], bcrypt.gensalt())
         user = User.objects.create(
            name=kwargs['name'],
            alias=kwargs['alias'],
            email=kwargs['email'],
            pw_hash=pw_hash
            )
         return (True, user.alias, user.id)
      else:
         return (False, error_list)

   def loginUser(self, **kwargs):
      error = False
      error_list = []

      if not kwargs['email']:
         error_list.append("Email is required")
         error = True

      if not EMAIL_REGEX.match(kwargs['email']):
         error_list.append("Not a valid email")
         error = True

      try:
         user = User.objects.get(email=kwargs['email'])
         input_pw = kwargs['pw_hash'].encode('utf-8')
         hashed_pw = user.pw_hash.encode('utf-8')

         if bcrypt.hashpw(input_pw, hashed_pw) == hashed_pw and error == False:
            print("Password and email valid")
            return (True, user.alias, user.id)
         else:
            print ("hit try else error")
            error_list.append("That didn't work, try again!")
            return (False, error_list)

      except:
         print ("hit except error")
         error_list.append("That didn't work, try again!")
         return (False, error_list)

class ReviewManager(models.Manager):

   def addBook_and_Review(self, **kwargs):

      error_list =[]
      errors = False

      ### If Empty Validations ###

      if kwargs['author'] == "" and kwargs['new_author'] == "":
         error_list.append("Author cant be left blank")
         errors = True
         return (False, error_list)

      if kwargs['title'] == "" and kwargs['new_title'] == "":
         error_list.append("Title cant be left blank")
         errors = True
         return (False, error_list)

      if kwargs['review'] == "":
         error_list.append("Review cant be left blank")
         errors = True
         return (False, error_list)

      #### If existing Author / Title validations ###

      if kwargs['new_author']:
         kwargs['author'] = kwargs['new_author']

      if kwargs['new_title']:
         kwargs['title'] = kwargs['new_title']

      try:
         book = Book.objects.get(title=kwargs['title'])
         user = User.objects.get(id=kwargs['user'])

         result = Review.objects.create(
            review=kwargs['review'],
            rating=kwargs['rating'],
            user=user,
            book=book
            )
         print "try succeed"
         return (True, result)

      except:
         book = Book.objects.create(title=kwargs['title'], author=kwargs['author'])

         user = User.objects.get(id=kwargs['user'])

         result = Review.objects.create(
            review=kwargs['review'],
            rating=kwargs['rating'],
            user=user,
            book=book
            )
         print "else succeed with new Title"
         return (True, result)

   def getShowReviews(self, id):
      book = Book.objects.get(id=id)
      title = book.title

      result = Review.objects.all().filter(book_id=book).order_by('-id')

      return result

   def addNewReview(self, **kwargs):
      print kwargs

      book = Book.objects.get(id=kwargs['book'])
      user = User.objects.get(id=kwargs['user'])

      result = Review.objects.create(
         review=kwargs['review'],
         rating=kwargs['rating'],
         user=user,
         book=book
         )
      print "Success add new title"

      return (True, result)

   def deleteReview(self, **kwargs):
      errors = False
      error_list = []

      review = Review.objects.get(id=kwargs['review_id'])

      print kwargs['user']
      print review.user_id

      if int(kwargs['user']) == int(review.user_id):
         review.delete()
         result = True
         return (False, result)

      else:
         print 'hit else in model'
         error_list.append("You can only delete your own reviews")
         return (True, error_list)

   def indexShow(self):
      book = Book.objects.all()
      result = Review.objects.all().order_by('-id')
      return result

class BookManager(models.Manager):

   def getShowBooks(self, id):
      result = Book.objects.filter(id=id)
      return result

   def getBooks(self, id):
      user = User.objects.get(id=id)

      result = Book.objects.filter(review__user_id=id)
      return result

   def getAllBooks(self):
      return Book.objects.all()

class User(models.Model):
   name = models.CharField(max_length=200)
   alias = models.CharField(max_length=200)
   email = models.EmailField()
   pw_hash = models.CharField(max_length=200)
   created_at = models.DateField(auto_now_add=True)
   updated_at = models.DateField(auto_now=True)
   objects = UserManager()

class Book(models.Model):
   title = models.CharField(max_length=200)
   author = models.CharField(max_length=200)
   created_at = models.DateField(auto_now_add=True)
   updated_at = models.DateField(auto_now=True)
   objects = BookManager()

class Review(models.Model):
   review = models.CharField(max_length=2000)
   rating = models.CharField(max_length=200)
   created_at = models.DateField(auto_now_add=True)
   updated_at = models.DateField(auto_now=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   book = models.ForeignKey(Book, on_delete=models.CASCADE)
   objects = ReviewManager()

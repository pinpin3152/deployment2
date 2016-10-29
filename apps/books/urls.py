from django.conf.urls import url
from . import views
urlpatterns = [
      url (r'^$', views.login_reg, name = 'login_reg'),
      url (r'^books$', views.index, name = 'books'),
      url (r'^register$', views.register, name = 'register'),
      url (r'^login$', views.login, name = 'login'),
      url (r'^logout$', views.logout, name = 'logout'),
      url (r'^books/add$', views.add, name = 'add'),
      url (r'^books/create$', views.create, name = 'create'),
       url (r'^books/delete/(?P<id>[0-9]+)?$', views.delete_review, name = 'delete'),
      url (r'^books/add/review', views.add_new_review, name = 'add_new_review'),
      url (r'^books/(?P<id>[0-9]+)?$', views.show, name = 'show'),
      url (r'^books/user/(?P<id>[0-9]+)?$', views.show_user, name = 'show_user'),
    #   url (r'^products/(?P<id>[0-9]+)?$', views.update, name = 'update'),
]

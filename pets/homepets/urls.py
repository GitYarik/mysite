from django.urls import path, re_path
from homepets.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('',HomepetsHome.as_view(), name="home"),
    path('about/', about, name="about"),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name="contact"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name="register"),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', HomepetsCategory.as_view(), name="category"),
    #path("cats/<slug:cat>", category, name="category"),
    #re_path(r'archive/(?P<year>[0-9]{4})/', archive),

]

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .utils import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin



menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]
# class делает тоже что и функция index
class HomepetsHome(DataMixin, ListView):
    #paginate_by = 3  # количечтво элементов на странице
    model = Homepets
    template_name = "homepets/index.html"
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items())) # обьеденили словари
        #context['menu'] = menu    миксины  c_def
        #context['title'] = 'Все категории'   миксины  c_def
        #context['cat_selected'] = 0#выбранные нельзя нажать   миксины  c_def
        return context

    def get_queryset(self):#метод отображениея публикаций если стоит галдочка ин публишь
        return Homepets.objects.filter(is_published=True).select_related('cat')

#def index(request):
#    posts = Homepets.objects.all()
#
#    context = {
#        "posts": posts,
#        "menu": menu,
#        'title': "Главная страница",
#        "cat_selected": 0,
#    }
#    return render(request, "homepets/index.html", context=context)


def about(request):
    contact_list = Homepets.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepets/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView): # добавление статьи
    form_class = AddPostForm
    template_name = 'homepets/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')# перенаправление если не авторизован пользователь
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление страницы')
        context = dict(list(context.items()) + list(c_def.items())) # обьеденили словари
        return context

#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST)
#        if form.is_valid():
#            #print(form.cleaned_data)
#            try:
#                Homepets.objects.create(**form.cleaned_data)
#                return redirect('home')
#            except:
#                form.add_error(None, 'Ошибка добавления поста')
#    else:
#        form = AddPostForm()
#
#    context = {
#        'form': form,
#        "menu": menu,
#        'title': "Добавить статью",
#
#    }
#
#    return render(request, "homepets/addpage.html", context=context)


#def contact(request):
#    return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'homepets/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None,**kwargs): #отображение верхнего меню
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(context.items()) + list(c_def.items()))  # обьеденили словари
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


#def login(request):
#    return HttpResponse("Авторизация")

# class делает тоже что и функция show_post
class ShowPost(DataMixin, DetailView):
    model = Homepets
    template_name = "homepets/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None,**kwargs): #отображение верхнего меню
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))  # обьеденили словари
        return context

#def show_post(request, post_slug):
#    post = get_object_or_404(Homepets, slug=post_slug)
#
#    context = {
#        "post": post,
#        "menu": menu,
#        'title': post.title,
#        "cat_selected": post.cat_id,
#    }
#
#    return render(request, "homepets/post.html", context=context)

# class делает тоже что и функция show_category
class HomepetsCategory(DataMixin, ListView):
    #paginate_by = 3  # количечтво элементов на странице
    model = Homepets
    template_name = "homepets/index.html"
    context_object_name = 'posts'
    allow_empty = False# 404 если не правильный слаг

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Категория - '+str(context['posts'][0].cat)
        #context['menu'] = menu
        #context['cat_selected'] = context['posts'][0].cat_id#выбранные нельзя нажать
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                    cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))  # обьеденили словари
        return context

    def get_queryset(self):#метод отображениея публикаций если стоит галдочка ин публишь
        return Homepets.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

#def show_category(request, cat_id):
#    posts = Homepets.objects.filter(cat_id=cat_id)
#
#    if len(posts) == 0:
#        raise Http404()
#
#    context = {
#        "posts": posts,
#        "menu": menu,
#        'title': "Отображение по рубрикам",
#        "cat_selected": cat_id,
#    }
#    return render(request, "homepets/index.html", context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

# def category(request, cat):
#   if(request.GET):
#      print(request.GET)
#  return HttpResponse(f"<h1> Category</h1>  <p>{cat}</p>")


# def archive(request, year):
#   if int(year)>2022:
#       return redirect("home", permanent=True)
#   return HttpResponse(f"<h1> Архив по годам</h1>  <p>{year}</p>")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "homepets/register.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'homepets/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')



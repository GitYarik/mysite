from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'},
        ]


class DataMixin:
    paginate_by = 3  # количечтво элементов на странице

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('homepets'))
            cache.set('cats', cats, 60)

        #cats = Category.objects.all().annotate(Count('homepets'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:# проверка на авторизацию
            user_menu.pop(1)# если не авторизован удалем из меню "Добавить статью"

        context['menu'] = user_menu

        context['cats'] = cats
        if "cat_selected" not in context:
            context['cat_selected'] = 0
        return context




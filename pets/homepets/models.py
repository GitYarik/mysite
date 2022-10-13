from django.db import models
from django.urls import reverse



class Homepets(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="фото")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):#метод для базы данных({{ p.get_absolute_url }})
        return reverse("post", kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name ="домашних животных"
        verbose_name_plural = "Домашние животные"
        ordering =["title"] #сортировка по имени

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name ="категорию"
        verbose_name_plural = "Категория"
        ordering =["id"] #сортировка по имени

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # метод для базы данных({{ p.get_absolute_url }})
        return reverse("category", kwargs={'cat_slug': self.slug})





#ForeingnKey(<ccылка на первичную модель>, on delete=<ограничение при удалении>) -связь многик к одному
#ManyToManyField - многие ко многим
#OneToONEFeild - Один к одному
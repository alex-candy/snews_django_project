

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True, unique=True)
    full_text = models.TextField(blank=True, null=True)
    from_place = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    date_redact = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    auth_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL,  blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL,  blank=True, null=True)
    blog_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        # managed = False
        db_table = 'articles'

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'art_id': self.id})

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'category'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('redact')

class Coment(models.Model):
    id = models.AutoField(primary_key=True)
    text_coment = models.TextField( blank=True, null=True)
    articles = models.ForeignKey('Articles', on_delete=models.SET_NULL, blank=True, null=True)
    auth_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    video = models.ForeignKey('Video', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'coment'

    def __str__(self):
        return self.text_coment


class Condition(models.Model):
    id = models.AutoField(primary_key=True)
    condition = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'condition'

    def __str__(self):
        return self.condition




class Placing(models.Model):
    id = models.AutoField(primary_key=True)
    placing_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'placing'

    def __str__(self):
        return self.placing_name



class Source(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'source'

    def __str__(self):
        return self.source


class TypeVideo(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'type_video'

    def __str__(self):
        return self.type_name


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True, unique=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    full_text = models.TextField( blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    preview =models.ImageField(upload_to='photos/', blank=True, null=True)
    auth_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    placing = models.ForeignKey('Placing', on_delete=models.SET_NULL, blank=True, null=True)
    type_video = models.ForeignKey('TypeVideo', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, blank=True, null=True)
    date_redact = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    video_views = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'video'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos')

# class Articles(models.Model):
#     title = models.CharField('Название', max_length=50,blank=True, null=True)
#     autor = models.CharField('Автор', max_length=250,blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True,db_index=True, null=True)
#     full_text = models.TextField('Статья',db_index=True, blank=True, null=True)
#     date_create = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True, blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Cтатья'
#         verbose_name_plural = 'Статьи'
#
#     def get_absolute_url(self):
#         return reverse('detail_article', kwargs={'slug': self.slug})
#
# class Koment(models.Model):
#     user = models.CharField( max_length=50,blank=True, null=True)
#     full_text = models.TextField('Статья',db_index=True, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'
#
# class Sotrud(models.Model):
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#     firstname = models.CharField(max_length=50)
#     secondname = models.CharField(max_length=100)
#     kontakts = models.CharField(max_length=100)
#     role = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.firstname
#
#     class Meta:
#         db_table = 'sotrud'
#         verbose_name = 'Сотрудник'
#         verbose_name_plural = 'Сотрудники'
#
#     def get_absolute_url(self):
#         return reverse('sotrud_update', kwargs={'pk': self.pk})
#
# class KriminalNow(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         # managed = False
#         db_table = 'kriminal_now'
#         verbose_name = 'Криминал'
#         verbose_name_plural = 'Криминал'
#
#
#     def get_absolute_url(self):
#         return reverse('detail_news_kriminal', kwargs={'slug': self.slug})
#
#
# class KulturNow(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         # managed = False
#         db_table = 'kultur_now'
#         verbose_name = 'Культура'
#         verbose_name_plural = 'Культура'
#
#     def get_absolute_url(self):
#         return reverse('detail_news_kultur', kwargs={'slug': self.slug})
#
#
# class NaukNow(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     date = models.DateField(auto_now_add=True, blank=True, null=True)
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         # managed = False
#         db_table = 'nauk_now'
#         verbose_name = 'Наука'
#         verbose_name_plural = 'Наука'
#
#     def get_absolute_url(self):
#         return reverse('detail_news_nauk', kwargs={'slug': self.slug})
#
#
# class Navig(models.Model):
#     id = models.AutoField(primary_key=True)
#     idregistation = models.ForeignKey('Registration', models.CASCADE, db_column='idregistation', blank=True, null=True)
#     idobsujd = models.ForeignKey('Articles', models.CASCADE, db_column='idobsujd', blank=True, null=True)
#     idnowost = models.ForeignKey('Nowost', models.CASCADE, db_column='idnowost', blank=True, null=True)
#     navigat = models.CharField(max_length=45, blank=True, null=True)
#
#     def __str__(self):
#         return self.navigat
#
#     class Meta:
#         # managed = False
#         db_table = 'navig'
#         verbose_name = 'Навигация'
#         verbose_name_plural = 'Навигация'
#
#
# class Nowost(models.Model):
#     id = models.AutoField(primary_key=True)
#     sport_now_idsport_now = models.ForeignKey('SportNow', models.CASCADE, db_column='idsport_now', blank=True, null=True)
#     kriminal_now_idkriminal_now = models.ForeignKey('KriminalNow', models.CASCADE, db_column='idkriminal_now', blank=True, null=True)
#     politik_now_idpolitik_now = models.ForeignKey('PolitikNow', models.CASCADE, db_column='idpolitik_now', blank=True, null=True)
#     nauk_now_idnauk_now = models.ForeignKey('NaukNow', models.CASCADE, db_column='idnauk_now', blank=True, null=True)
#     kultur_now_idkultur_now = models.ForeignKey('KulturNow', models.CASCADE, db_column='idkultur_now', blank=True, null=True)
#     nowost_name = models.CharField(max_length=100, blank=True, null=True)
#     name_categor = models.CharField(max_length=45, blank=True, null=True)
#     url_categor = models.CharField(max_length=45, blank=True, null=True)
#     url_ctreate_categor = models.CharField(max_length=45, blank=True, null=True)
#
#     def __str__(self):
#         return self.name_categor
#
#     class Meta:
#         # managed = False
#         db_table = 'nowost'
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#
#
#
# class PolitikNow(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         # managed = False
#         db_table = 'politik_now'
#         verbose_name = 'Политика'
#         verbose_name_plural = 'Политика'
#
#     def get_absolute_url(self):
#         return reverse('detail_news_politik', kwargs={'slug': self.slug})
#
#
# class Registration(models.Model):
#     idregistation = models.AutoField(primary_key=True)
#     parol = models.CharField(max_length=50)
#     nickname = models.CharField(max_length=50)
#     role = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.nickname
#
#     class Meta:
#         # managed = False
#         db_table = 'registation'
#
#
# class SportNow(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     foto = models.ImageField(upload_to='photos/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         # managed = False
#         db_table = 'sport_now'
#         verbose_name = 'Спорт'
#         verbose_name_plural = 'Спорт'
#
#     def get_absolute_url(self):
#         return reverse('detail_news_sport', kwargs={'slug': self.slug})





# Create your models here.

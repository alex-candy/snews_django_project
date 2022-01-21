#импортируем модели для работы с сайтами html
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
#импортируем сразу все модели из файла с моделями
from .models import *
#импортируем формы для записи
from .forms import *
#импортируем класс для работы с представлениями
from django.views.generic import DetailView, UpdateView
#импорт библиотеки для работы с mysql
import mysql.connector
#импорт класс для работы с ошибкой
from mysql.connector import Error
#import eel
#Формы для регистрации
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import F

#====================================================================================
"""РЕГИСТРАЦИЯ"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'kurs/register.html', {'form':form})

"""АВТОРИЗАЦИЯ"""
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()
    return render(request, 'kurs/login.html', {'form':form})

"""ВЫХОД ИЗ АККАУНТА"""
def user_logout(request):
    logout(request)
    return redirect('home')

#================================================================================

"""ГЛАВНАЯ СТРАНИЦА"""
def index(request):
    # rows = Articles.objects.raw("select * from main_articles")
    # data = {
    #     'title': 'Главная страница',
    #     'values': ['some', 'cddcdc', 'cdcd'],
    #     'obj': {'1': 'ddefe', '2': 'dewec', '3': 'wdqew'},
    #     'rows': rows,
    # }
    with connection.cursor() as cursor:  # эквивалентно записи
        cursor.execute("select * from test_trigger")
        trigger = cursor.fetchall()
        data={"trigger": trigger}
    return render(request, "kurs/index.html", data)
##============================================================================
# """СТРАНИЦА Сотрудников"""
# def sotrud(request):
#     sotrud=Sotrud.objects.all()
#     return render (request, "kurs/about.html",{'sotrud':sotrud})
#
# def create_sotrud(request):
#     error = ''
#     if request.method == 'POST':
#         form = SotrudForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'kurs/about_create.html', {"form": form})
#         else:
#             error = "Данные введены не верно"
#
#     form = SotrudForm()
#     data = {"form": form, "error": error}
#     return render(request, 'kurs/about_create.html', data)
#
# """ИЗМЕНЕНИЕ СОТРУДНИКА"""
# class SotrudUpdate(UpdateView):
#     model = Sotrud
#     template_name = "kurs/about_update.html"
#     form_class = SotrudForm
#
# def sotrud_delete(request, pk):
#     with connection.cursor() as cursor:
#         cursor.execute("select * from sotrud where id =%s", [pk])
#         dnews = cursor.fetchall()
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("delete from sotrud where id = %s", [pk])
#             return redirect("about")
#     data = {
#         'dnews': dnews,
#     }
#     return render(request, "kurs/about_delete.html", data)
#
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

"""РЕДАКТИРОВАНИЕ КАТЕГОРИЙ"""
def redact(request):
    categor=Category.objects.raw("select * from category")
    return render(request, "kurs/redact.html", {'categor': categor})

'''УДАЛЕНИЕ ВИДЕО'''
def redact_delete(request, cat_id):
        with connection.cursor() as cursor:
            cursor.execute("delete from category where id = %s", [cat_id])
        return redirect("redact")


"""ИЗМЕНЕНИЕ ВИДЕО"""
class RedactUpdate(UpdateView):
    model = Category
    template_name = "kurs/redact_update.html"
    form_class = CategoryForm

"""СОЗДАНИЕ ВИДЕО"""
def redact_create(request):
    error=''
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            otvet = 'Создание прошло успешно'
            return render(request, 'kurs/redact_create.html', {"form":form, 'otvet':otvet}) #'test':test})
        else:
            error="Данные введены не верно"
    form=CategoryForm()
    data={"form":form, "error":error}
    return render(request, 'kurs/redact_create.html', data)


#=================================================================================================================================================

"""ВЫБОР СТРАНІЦЫ СО СТАТЬЯМИ"""
def articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    # news = Articles.objects.raw("select * from main_articles")
    categor = Category.objects.raw("select * from category")
    with connection.cursor() as cursor:
        cursor.execute("select * from view_articles where not condition_id=4 order by id desc")
        news = cursor.fetchall()
        cursor.execute("SELECT * FROM view_articles_2 where blog_views = (select max(blog_views) FROM view_articles_2)")
        popular = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor': categor, "popular":popular})

"""ПОКАЗАТЬ ОПРЕДЕЛЁННУЮ КАТЕГОРИЮ"""
def show_category(request, cat_id):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    # news = Articles.objects.raw("select * from main_articles")
    categor = Category.objects.raw("select * from category")
    with connection.cursor() as cursor:
        cursor.execute("select * from view_articles where category_id=%s order by id desc ",[cat_id])
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor': categor})



'''УДАЛЕНИЕ НОВОСТИ'''
def article_delete(request, art_id):
    with connection.cursor() as cursor:
        cursor.execute("select * from view_articles where id=%s", [art_id])
        dnews = cursor.fetchall()
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("delete from articles where id = %s", [art_id])
        return redirect("articles")
    data = {
        'dnews': dnews,
    }
    return render(request, "kurs/articles_delete.html", data)

"""ИЗМЕНЕНИЕ СТАТЬИ"""
class ArticleUpdate(UpdateView):
    model = Articles
    template_name = "kurs/articles_update.html"
    form_class = ArticlesForm

"""СОЗДАНИЕ СТАТЬИ"""
def articles_create(request):
    error=''
    user_id = request.user.id
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            # from_place = form.cleaned_data.get('from_place')
            # photo = form.cleaned_data.get('photo')
            # full_text = form.cleaned_data.get('full_text')
            # category = form.cleaned_data.get('category')
            # category=category.id
            # condition = form.cleaned_data.get('condition')
            # condition=condition.id
            # source = form.cleaned_data.get('source')
            # source = source.id
            # with connection.cursor() as cursor:
            #     cursor.execute("INSERT INTO articles (title, full_text, photo, date_redact, auth_user_id, category_id, condition_id, source_id, from_place) VALUES (%s, %s, %s, now(), %s, %s, %s, %s, %s)",
            #                    [title, full_text, photo, user_id, category, condition, source, from_place])
            form.save()
            otvet='Создание прошло успешно'
            with connection.cursor() as cursor:
                cursor.execute("update articles set auth_user_id=%s where title=%s",
                               [user_id, title])

            return render(request, 'kurs/articles_create.html', {"form":form,'otvet':otvet}) #'test':test})
        else:
            error="Данные введены не верно"
    form=ArticlesForm()
    data={"form":form, "error":error}
    return render(request, 'kurs/articles_create.html', data)


"""ПОКАЗАТЬ СТАТЬЮ ДЕТАЛЬНО"""
def show_article(request, art_id):
    form=Koment()
    user=request.user
    user1=str(user)
    blog_object=Articles.objects.get(id=art_id)
    blog_object.blog_views=blog_object.blog_views+1
    blog_object.save()
    with connection.cursor() as cursor:
        cursor.execute("select * from view_articles where id=%s", [art_id])
        dnews = cursor.fetchall()
        cursor.execute("select * from view_articles_2 where id=%s", [art_id])
        views = cursor.fetchall()
        cursor.execute("select * from view_coment where articles_id=%s", [art_id])
        koments = cursor.fetchall()
    return render(request, "kurs/details_view_articles.html", {'dnews':dnews,'views':views,'form':form, 'koments': koments, 'user1': user1})


"""ПОИСК СТАТЬИ"""
def articles_poisk(request):
    categor = Category.objects.raw("select * from category")
    if request.method == 'POST':
        form = Poisk(request.POST)
        if form.is_valid():
            poisk = form.cleaned_data.get('poisk')
            with connection.cursor() as cursor:
                cursor.callproc("poisk_article", [poisk])
                news = cursor.fetchall()
                paginator = Paginator(news, 9)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            return render(request, "kurs/articles.html", {'page_obj': page_obj, 'form': form, 'news': news, 'categor':categor})
    else:
        form = Poisk()
        # news = Articles.objects.order_by('-date')
        # news = Articles.objects.raw("select * from main_articles")
        with connection.cursor() as cursor:
            cursor.execute("select * from articles order by id desc")
            news = cursor.fetchall()
            paginator = Paginator(news, 9)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, "kurs/articles.html", {'page_obj': page_obj, 'form': form, 'news': news, 'categor':categor})

"""КОММЕНТАРИИ"""
def article_koment(request, art_id):
    with connection.cursor() as cursor:
        cursor.execute("select * from view_articles where id=%s", [art_id])
        dnews = cursor.fetchall()
        cursor.execute("select * from view_coment where articles_id=%s order by id desc", [art_id])
        koments = cursor.fetchall()
    if request.method == 'POST':
        form = Koment(request.POST)
        user_id = request.user.id
        if form.is_valid():
            koment = form.cleaned_data.get('koment')
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO coment (auth_user_id, text_coment, articles_id) VALUES (%s, %s, %s)",[user_id, koment, art_id])
            # return render(request, "kurs/details_view_articles.html", {'form': form, 'dnews': dnews, 'koments': koments})
            return HttpResponseRedirect(reverse('detail_article', kwargs={'art_id': art_id}))
    else:
        form=Koment()
        return render(request, "kurs/details_view_articles.html", {'form': form, 'dnews': dnews, 'koments': koments})

"""СОРТИРОВКА СТАРЫЕ"""
def sort_star_articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = Category.objects.raw("select * from category")
    #news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("starye_a")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_now_articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = Category.objects.raw("select * from category")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("nowye_a")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_prower_articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = Category.objects.raw("select * from category")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("prower_a")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА СКРЫТЫЕ"""
def sort_skryt_articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = Category.objects.raw("select * from category")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc( "skryt_a")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_dorab_articles(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = Category.objects.raw("select * from category")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("dorab_a")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/articles.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

'''Удаление коментов'''
def delete_coment_article(request, art_id, com_id):
    with connection.cursor() as cursor:
        cursor.execute("delete from coment where id = %s", [com_id])
    return HttpResponseRedirect(reverse('detail_article', kwargs={'art_id': art_id}))
#==================================================================================================================================================
#=================================================================================================================================================

"""ВЫБОР СТРАНИЦЫ С ВИДЕО"""
def videos(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    # news = Articles.objects.raw("select * from main_articles")
    categor = TypeVideo.objects.raw("select * from type_video")
    with connection.cursor() as cursor:
        cursor.execute("select * from view_video where not condition_id=4 order by id desc")
        news = cursor.fetchall()
        cursor.execute("SELECT * FROM view_video_2 where video_views = (select max(video_views) FROM view_video_2)")
        popular = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj,'popular':popular, 'form': form, 'news': news, 'categor': categor})

"""ПОКАЗАТЬ ВИДЕО"""
def show_type(request, vid_id):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    # news = Articles.objects.raw("select * from main_articles")
    categor = TypeVideo.objects.raw("select * from type_video")
    with connection.cursor() as cursor:
        cursor.execute("select * from view_video where type_video_id=%s order by id desc ",[vid_id])
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor': categor})

"""ПОКАЗАТЬ ВИДЕО"""
def show_video(request, art_id):
    form=Koment()
    user = request.user
    user1 = str(user)
    blog_object = Video.objects.get(id=art_id)
    blog_object.video_views = blog_object.video_views + 1
    blog_object.save()
    with connection.cursor() as cursor:
        cursor.execute("select * from view_video where id=%s", [art_id])
        dnews = cursor.fetchall()
        cursor.execute("select * from view_video_2 where id=%s", [art_id])
        views = cursor.fetchall()
        cursor.execute("select * from view_coment where video_id=%s", [art_id])
        koments = cursor.fetchall()
    return render(request, "kurs/view_video.html", {'dnews':dnews, 'form':form, 'koments': koments,'views':views, 'user1':user1})

'''УДАЛЕНИЕ ВИДЕО'''
def video_delete(request, art_id):
    with connection.cursor() as cursor:
        cursor.execute("select * from view_video where id=%s", [art_id])
        dnews = cursor.fetchall()
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("delete from video where id = %s", [art_id])
        return redirect("videos")
    data = {
        'dnews': dnews,
    }
    return render(request, "kurs/video_delete.html", data)

"""ИЗМЕНЕНИЕ ВИДЕО"""
class VideoUpdate(UpdateView):
    model = Video
    template_name = "kurs/video_update.html"
    form_class = VideoForm

"""СОЗДАНИЕ ВИДЕО"""
def video_create(request):
    error=''
    user_id = request.user.id
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            form.save()
            otvet = 'Создание прошло успешно'
            with connection.cursor() as cursor:
                cursor.execute("update video set auth_user_id=%s where title=%s",
                               [user_id, title])
            return render(request, 'kurs/video_create.html', {"form":form, 'otvet':otvet}) #'test':test})
        else:
            error="Данные введены не верно"
    form=VideoForm()
    data={"form":form, "error":error}
    return render(request, 'kurs/video_create.html', data)



"""ПОИСК ВИДЕО"""
def video_poisk(request):
    categor = TypeVideo.objects.raw("select * from type_video")
    if request.method == 'POST':
        form = Poisk(request.POST)
        if form.is_valid():
            poisk = form.cleaned_data.get('poisk')
            with connection.cursor() as cursor:
                cursor.callproc("poisk_video", [poisk])
                news = cursor.fetchall()
                paginator = Paginator(news, 9)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            return render(request, "kurs/videos.html", {'page_obj': page_obj, 'form': form, 'news': news, 'categor':categor})
    else:
        form = Poisk()
        # news = Articles.objects.order_by('-date')
        # news = Articles.objects.raw("select * from main_articles")
        with connection.cursor() as cursor:
            cursor.execute("select * from view_video order by id desc")
            news = cursor.fetchall()
            paginator = Paginator(news, 9)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, "kurs/videos.html", {'page_obj': page_obj, 'form': form, 'news': news, 'categor':categor})

def video_koment(request, art_id):
    with connection.cursor() as cursor:  # эквивалентно записи
        cursor.execute("select * from view_video where id=%s", [art_id])
        dnews = cursor.fetchall()
        cursor.execute("select * from view_coment where video_id=%s order by id desc", [art_id])
        koments = cursor.fetchall()
    if request.method == 'POST':
        form = Koment(request.POST)
        user_id = request.user.id
        if form.is_valid():
            koment = form.cleaned_data.get('koment')
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO coment (auth_user_id, text_coment, video_id) VALUES (%s, %s, %s)",[user_id, koment, art_id])
            # return render(request, "kurs/details_view_articles.html", {'form': form, 'dnews': dnews, 'koments': koments})
            return HttpResponseRedirect(reverse('detail_video', kwargs={'art_id': art_id}))
    else:
        form=Koment()
        return render(request, "kurs/view_video.html", {'form': form, 'dnews': dnews, 'koments': koments})

"""СОРТИРОВКА СТАРЫЕ"""
def sort_star_video(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = TypeVideo.objects.raw("select * from type_video")
    #news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("starye_v")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_now_video(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = TypeVideo.objects.raw("select * from type_video")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("nowye_v")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_prower_video(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = TypeVideo.objects.raw("select * from type_video")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("prower_v")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА СКРЫТЫЕ"""
def sort_skryt_video(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = TypeVideo.objects.raw("select * from type_video")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc( "skryt_v")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

"""СОРТИРОВКА НОВЫЕ"""
def sort_dorab_video(request):
    form=Poisk()
    #news = Articles.objects.order_by('-date')
    categor = TypeVideo.objects.raw("select * from type_video")
    # news = Articles.objects.raw("select * from main_articles")
    with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
        cursor.callproc("dorab_v")
        news = cursor.fetchall()
        paginator = Paginator(news, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "kurs/videos.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})

'''Удаление коментов'''
def delete_coment_video(request, art_id, com_id):
    with connection.cursor() as cursor:
        cursor.execute("delete from coment where id = %s", [com_id])
    return HttpResponseRedirect(reverse('detail_video', kwargs={'art_id': art_id}))

# #=============================================================================
# """ВЫБОР ОСНОВНОЙ СТРАНІЦЫ НОВОСТЕЙ"""
# def news_home(request):
#     form=Poisk()
#     #news = Articles.objects.order_by('-date')
#     categor = Nowost.objects.raw("select * from nowost")
#     # news = Articles.objects.raw("select * from main_articles")
#     with connection.cursor() as cursor:
#         cursor.execute("select * from main_news order by id desc")
#         news = cursor.fetchall()
#         paginator = Paginator(news, 9)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/news_home.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})
#
# """ТЕСТОВАЯ ФУНКЦИЯ, КОТОРАЯ ПОКАЗЫВАЕТ НОВОСТИ НА ГЛАВНОЙ СТРАНИЦЕ (ОНА РАБОТАЕТ)"""
# def show_news_main(request, slug):
#     form=Koment()
#     with connection.cursor() as cursor:  # эквивалентно записи
#         cursor.execute("select * from main_news where slug=%s", [slug])
#         dnews = cursor.fetchall()
#         cursor.execute("select * from koments where url_name=%s", [slug])
#         koments = cursor.fetchall()
#     return render(request, "kurs/details_view_main.html", {'form': form, 'dnews': dnews, 'koments': koments})
#
# def news_koment(request, slug):
#     with connection.cursor() as cursor:  # эквивалентно записи
#         cursor.execute("select * from main_news where slug=%s", [slug])
#         dnews = cursor.fetchall()
#         cursor.execute("select * from koments where url_name=%s", [slug])
#         koments = cursor.fetchall()
#     if request.method == 'POST':
#         form = Koment(request.POST)
#         user = request.user
#         if form.is_valid():
#             koment = form.cleaned_data.get('koment')
#             with connection.cursor() as cursor:
#                 cursor.execute("INSERT INTO koments (obs_name, text_obs, url_name) VALUES (%s, %s, %s)",[user, koment, slug])
#             # return render(request, "kurs/details_view_articles.html", {'form': form, 'dnews': dnews, 'koments': koments})
#             return HttpResponseRedirect(reverse('detail_news_main', kwargs={'slug': slug}))
#     else:
#         form=Koment()
#         return render(request, "kurs/details_view_main.html", {'form': form, 'dnews': dnews, 'koments': koments})
#
# """СОЗДАНИЕ НОВОЙ НОВОСТИ"""
# def create(request):
#     error=''
#     if request.method == 'POST':
#         form = AddNewsForm(request.POST)
#         if form.is_valid():
#             cat = form.cleaned_data.get('categor')
#             title = form.cleaned_data.get('title')
#             slug = form.cleaned_data.get('slug')
#             foto = form.cleaned_data.get('foto')
#             content = form.cleaned_data.get('content')
#             cat=cat.lower()
#             if cat == "спорт":
#                 with connection.cursor() as cursor:
#                     cursor.execute("INSERT INTO sport_now (title, sport_now.text, sport_now.date, foto, slug) VALUES (%s, %s, now(), %s, %s)",
#                                    [title, content, foto, slug])
#                 return render(request, "kurs/create.html", {'form':form})
#             elif cat == "криминал":
#                 with connection.cursor() as cursor:
#                     cursor.execute(
#                         "INSERT INTO kriminal_now (title, kriminal_now.text, kriminal_now.date, foto, slug) VALUES (%s, %s, now(), %s, %s)",
#                         [title, content, foto, slug])
#                 return render(request, "kurs/create.html", {'form': form})
#             elif cat == "культура":
#                 with connection.cursor() as cursor:
#                     cursor.execute(
#                         "INSERT INTO kultur_now (title, kultur_now.text, kultur_now.date, foto, slug) VALUES (%s, %s, now(), %s, %s)",
#                         [title, content, foto, slug])
#                 return render(request, "kurs/create.html", {'form': form})
#             elif cat == "наука":
#                 with connection.cursor() as cursor:
#                     cursor.execute(
#                         "INSERT INTO nauk_now (title, nauk_now.text, nauk_now.date, foto, slug) VALUES (%s, %s, now(), %s, %s)",
#                         [title, content, foto, slug])
#                 return render(request, "kurs/create.html", {'form': form})
#             elif cat == "политика":
#                 with connection.cursor() as cursor:
#                     cursor.execute(
#                         "INSERT INTO politik_now (title, politik_now.text, politik_now.date, foto, slug) VALUES (%s, %s, now(), %s, %s)",
#                         [title, content, foto, slug])
#                 return render(request, "kurs/create.html", {'form': form})
#             else:
#                 error = "Вы ввели несуществующую категорию"
#         else:
#             error = 'Форма была неверной'
#     form = AddNewsForm()
#     data = {
#         'form': form,
#         'error': error,
#     }
#     return render(request, "kurs/create.html", data)
#
# """РЕДАКТИРОВАНИЕ СТАРОЙ НОВОСТИ"""
# def news_update(request, slug):
#     error=''
#     form2=Koment()
#     with connection.cursor() as cursor:
#         cursor.execute("select * from main_news where slug=%s", [slug])
#         dnews = cursor.fetchall()
#     if request.method == 'POST':
#         form = UpdateNewsForm(request.POST)
#         if form.is_valid():
#             pole = form.cleaned_data.get('pole')
#             redact = form.cleaned_data.get('redact')
#             pole=pole.lower()
#             if pole=="заголовок":
#                 with connection.cursor() as cursor:
#                     cursor.execute("UPDATE nauk_now SET title = %s, nauk_now.date=now() WHERE slug = %s",[redact, slug])
#                     cursor.execute("UPDATE kultur_now SET title = %s, kultur_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE kriminal_now SET title = %s, kriminal_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE politik_now SET title = %s, politik_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE sport_now SET title = %s, sport_now.date=now() WHERE slug = %s", [redact, slug])
#                 return HttpResponseRedirect(reverse('detail_news_main', kwargs={'slug': slug}))
#             elif pole == "текст":
#                 with connection.cursor() as cursor:
#                     cursor.execute("UPDATE nauk_now SET nauk_now.text = %s, nauk_now.date=now() WHERE slug = %s",[redact, slug])
#                     cursor.execute("UPDATE kultur_now SET kultur_now.text = %s, kultur_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE kriminal_now SET kriminal_now.text = %s, kriminal_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE politik_now SET politik_now.text = %s, politik_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE sport_now SET sport_now.text = %s, sport_now.date=now() WHERE slug = %s", [redact, slug])
#                 # return render(request, "kurs/details_view_main.html", {'form': form, 'dnews': dnews})
#                 return HttpResponseRedirect(reverse('detail_news_main', kwargs={'slug': slug}))
#             elif pole == "фото":
#                 with connection.cursor() as cursor:
#                     cursor.execute("UPDATE nauk_now SET foto = %s, nauk_now.date=now() WHERE slug = %s",[redact, slug])
#                     cursor.execute("UPDATE kultur_now SET foto = %s, kultur_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE kriminal_now SET foto = %s, kriminal_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE politik_now SET foto = %s, politik_now.date=now() WHERE slug = %s", [redact, slug])
#                     cursor.execute("UPDATE sport_now SET foto = %s, sport_now.date=now() WHERE slug = %s", [redact, slug])
#                 return HttpResponseRedirect(reverse('detail_news_main', kwargs={'slug': slug}))
#             else:
#                 error="Такого поля не существует"
#
#     form = UpdateNewsForm()
#     with connection.cursor() as cursor:
#         cursor.execute("select * from main_news where slug=%s", [slug])
#         dnews = cursor.fetchall()
#     data={'form': form,'form2':form2, 'dnews': dnews,'error':error }
#     return render(request, "kurs/news_update.html", data)
#
# '''УДАЛЕНИЕ НОВОСТИ'''
# def news_delete(request, slug):
#     with connection.cursor() as cursor:
#         cursor.execute("select * from main_news where slug=%s", [slug])
#         dnews = cursor.fetchall()
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("delete from nauk_now where slug = %s",
#                            [slug])
#             cursor.execute("delete from kultur_now where slug = %s",
#                            [slug])
#             cursor.execute("delete from politik_now where slug = %s",
#                            [slug])
#             cursor.execute("delete from sport_now where slug = %s",
#                            [slug])
#             cursor.execute("delete from kriminal_now where  slug = %s",
#                            [slug])
#         return redirect("news_home")
#     data = {
#         'dnews': dnews,
#     }
#     return render(request, "kurs/news_delete.html", data)
#
# """ФОРМИРОВАНИЕ СТРАНИЦЫ НА ОСНОВЕ ПОИСКОВОГО ЗАПРОСА"""
# def news_home_poisk(request):
#     if request.method == 'POST':
#         form = Poisk(request.POST)
#         if form.is_valid():
#             poisk = form.cleaned_data.get('poisk')
#             categor = Nowost.objects.raw("select * from nowost")
#             with connection.cursor() as cursor:
#                 cursor.callproc("poisk",[poisk])
#                 news = cursor.fetchall()
#                 paginator = Paginator(news, 9)
#                 page_number = request.GET.get('page')
#                 page_obj = paginator.get_page(page_number)
#             return render(request, "kurs/news_home.html",{'page_obj': page_obj, 'form': form, 'news': news, 'categor': categor})
#     else:
#         form = Poisk()
#         # news = Articles.objects.order_by('-date')
#         categor = Nowost.objects.raw("select * from nowost")
#         # news = Articles.objects.raw("select * from main_articles")
#         with connection.cursor() as cursor:
#             cursor.execute("select * from main_news order by id desc")
#             news = cursor.fetchall()
#             paginator = Paginator(news, 9)
#             page_number = request.GET.get('page')
#             page_obj = paginator.get_page(page_number)
#         return render(request, "kurs/news_home.html", {'page_obj': page_obj, 'form': form, 'news': news, 'categor': categor})
#
# """СОРТИРОВКА СТАРЫЕ"""
# def news_sort_star(request):
#     form=Poisk()
#     #news = Articles.objects.order_by('-date')
#     categor = Nowost.objects.raw("select * from nowost")
#     #news = Articles.objects.raw("select * from main_articles")
#     with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
#         cursor.callproc("starye")
#         news = cursor.fetchall()
#         paginator = Paginator(news, 9)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/news_home.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})
#
# """СОРТИРОВКА НОВЫЕ"""
# def news_sort_now(request):
#     form=Poisk()
#     #news = Articles.objects.order_by('-date')
#     categor = Nowost.objects.raw("select * from nowost")
#     # news = Articles.objects.raw("select * from main_articles")
#     with connection.cursor() as cursor: #эквивалентно записи cursor=connection.cursor только ещё бы пришлось писать cursor.close()
#         cursor.callproc("nowye")
#         news = cursor.fetchall()
#         paginator = Paginator(news, 9)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/news_home.html", {'page_obj':page_obj, 'form': form, 'news': news, 'categor':categor})
#
#
# # """ВЫБОР КОНКРЕТНОЙ НОВОСТИ"""
# # class News(DetailView):
# #     model = Articles
# #     template_name = 'kurs/details_view.html'
# #     context_object_name = 'article'
#
# #======================================================================================================================
#
# """КАТЕГОРИЯ КРИМИНАЛ"""
# def criminal_news(request):
#     form = Poisk()
#     news = KriminalNow.objects.raw("select * from kriminal_now")
#     categor = Nowost.objects.raw("select * from nowost")
#     paginator = Paginator(news, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/criminal_news.html", {'page_obj':page_obj, 'news': news, 'categor':categor, 'form':form})
#
# """КАТЕГОРИЯ КУЛЬТУРА"""
# def cultur_news(request):
#     form = Poisk()
#     news = KulturNow.objects.raw("select * from kultur_now")
#     categor = Nowost.objects.raw("select * from nowost")
#     paginator = Paginator(news, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/cultur_news.html", {'page_obj':page_obj, 'news': news,'categor':categor, 'form':form})
#
# """КАТЕГОРИЯ ПОЛИТИКА"""
# def politik_news(request):
#     form = Poisk()
#     news = PolitikNow.objects.raw("select * from politik_now")
#     categor = Nowost.objects.raw("select * from nowost")
#     paginator = Paginator(news, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/politik_news.html", {'page_obj':page_obj, 'news': news,'categor':categor, 'form':form})
#
# """КАТЕГОРИЯ НАУКА"""
# def sience_news(request):
#     form = Poisk()
#     news = NaukNow.objects.raw("select * from nauk_now")
#     categor = Nowost.objects.raw("select * from nowost")
#     paginator = Paginator(news, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/sience_news.html", {'page_obj':page_obj, 'news': news,'categor':categor, 'form':form})
#
# """КАТЕГОРИЯ СПОРТ"""
# def sport_news(request):
#     form = Poisk()
#     news = SportNow.objects.raw("select * from sport_now")
#     categor = Nowost.objects.raw("select * from nowost")
#     paginator = Paginator(news, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "kurs/sport_news.html", {'page_obj':page_obj, 'news': news,'categor':categor, 'form':form })





# Create your views here.

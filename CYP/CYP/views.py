from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.generic import View
from .forms import UserForm
from django.db import connection

# from django.core.context_processors import csrf


# Create your views here.
def index(request):
    if (request.GET.get('id')):
        id_num = request.GET.get('id')
        with connection.cursor() as cursor:
            cursor.execute(("SELECT url, source, post_date, title, author, text, top_image FROM cyp.News_articles WHERE cyp.News_articles.id = '%s'") % (int(id_num)))
            scrolls = cursor.fetchall()[0]
            ats = ""
            for stuff in scrolls[4]:
                ats += stuff.encode("utf-8").strip("[u']")
            ats = ats.strip("[u']")
        return render_to_response('News/Article.html', {'url': scrolls[0], 'source': scrolls[1], 'post_date': scrolls[2], 'title': scrolls[3], 'author': ats, 'texts': scrolls[5], 'top_image': scrolls[6]})
    else:
        return render(request, 'News/splash_page.html')

def aboutUs(request):
    return render(request, 'News/about.html')

def splash_page(request):
    return render(request, 'News/splash_page.html')

def service(request):
    return render(request, "News/service.html")

def house(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, first_name, last_name, party, person_id, district  FROM cyp.News_people WHERE cyp.News_people.role = 'senator'")
        peoples = cursor.fetchall()
        people = []
        for x in range(0,len(peoples)):
            people.append({'id': ("http://127.0.0.1:8000/house/?id=" + str(peoples[x][0])), 'first_name': peoples[x][1].title(), 'last_name': peoples[x][2].title(), 'party': peoples[x][3].title(), 'person_id': ("images/senate_pictures/"+peoples[x][4]+".jpg"), 'district': peoples[x][5]})

        if (request.GET.get('id')):
            id_num = request.GET.get('id')
            cursor.execute(("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id JOIN cyp.News_people on cyp.news_people.id = cyp.News_article_person.people_id_id WHERE cyp.News_people.id = '%s' ORDER BY cyp.News_articles.post_date DESC") % (int(id_num)))
        else:
            cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id JOIN cyp.News_people on cyp.news_people.id = cyp.News_article_person.people_id_id WHERE cyp.News_people.role = 'house' ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[]
        if len(scrolls)!= 0:
            if len(scrolls) < 9:
                article_pool_size = len(scrolls)
            else:
                article_pool_size = 9
            for x in range(0,article_pool_size):
                scroll.append({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
        else:
            scroll.append({'id': "", 'url': "", 'source': "No articles found", 'post_date': "Check Back At a Later Time", 'title': "Currently There Are No Articles Yet for This Person", 'top_image': ""})
    return render_to_response('News/house_news.html', {'peoples': people, 'scrolls': scroll})

def republican_scroll(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id JOIN cyp.News_people on cyp.news_people.id = cyp.News_article_person.people_id_id WHERE cyp.News_people.party = 'republican' ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/republican_scroll.html', {'scrolls': scroll})

def senate(request):
    # if (request.GET.get('id')):
    #     id_num = request.GET.get('id')
    #     with connection.cursor() as cursor:
    #         cursor.execute(("SELECT url, source, post_date, title, author, text, top_image FROM cyp.News_articles WHERE cyp.News_articles.id = '%s'") % (int(id_num)))
    #         scrolls = cursor.fetchall()[0]
    #         ats = ""
    #         for stuff in scrolls[4]:
    #             ats += stuff.encode("utf-8")
    #         ats = ats.strip("[]")
    #     return render_to_response('News/Article.html', {'url': scrolls[0], 'source': scrolls[1], 'post_date': scrolls[2], 'title': scrolls[3], 'author': ats, 'texts': scrolls[5], 'top_image': scrolls[6]})
    # else:
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id JOIN cyp.News_people on cyp.news_people.id = cyp.News_article_person.people_id_id WHERE cyp.News_people.role = 'senator' ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/senate_news.html', {'scrolls': scroll})

def democrat_scroll(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM cyp.News_people WHERE cyp.News_people.role = 'senator'")
        image_url = cursor.fetchall()

        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id JOIN cyp.News_people on cyp.news_people.id = cyp.News_article_person.people_id_id WHERE cyp.News_people.party = 'democrat' ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/democrat_scroll.html', {'scrolls': scroll}, {'image': image_url})

def recent_news(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/recent_news.html', {'scrolls': scroll})
    #
    # if (request.GET.get('id')):
    #     id_num = request.GET.get('id')
    #     with connection.cursor() as cursor:
    #         cursor.execute(("SELECT url, source, post_date, title, author, text, top_image FROM cyp.News_articles WHERE cyp.News_articles.id = '%s'") % (int(id_num)))
    #         scrolls = cursor.fetchall()[0]
    #         ats = ""
    #         for stuff in scrolls[4]:
    #             ats += stuff.encode("utf-8")
    #         ats = ats.strip("[]")
    #     return render_to_response('News/Article.html', {'url': scrolls[0], 'source': scrolls[1], 'post_date': scrolls[2], 'title': scrolls[3], 'author': ats, 'texts': scrolls[5], 'top_image': scrolls[6]})
    # else:
    #     return render(request, 'News/recent_news.html')

def news_scroll(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles ORDER BY cyp.News_articles.post_date DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("http://127.0.0.1:8000/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/news_scroll.html', {'scrolls': scroll})

def news_scroll_one(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id WHERE cyp.News_article_person.people_id_id = 110 ORDER BY cyp.News_article_person.weight DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/news_scroll_one.html', {'scrolls': scroll})

def news_scroll_two(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id WHERE cyp.News_article_person.people_id_id = 105 ORDER BY cyp.News_article_person.weight DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/news_scroll_two.html', {'scrolls': scroll})

def news_scroll_three(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT News_articles.id, url, source, post_date, title, top_image FROM cyp.News_articles JOIN cyp.News_article_person on cyp.News_articles.id = cyp.News_article_person.articles_id_id WHERE cyp.News_article_person.people_id_id = 106 ORDER BY cyp.News_article_person.weight DESC")
        scrolls = cursor.fetchall()
        scroll=[{},{},{},{},{},{},{},{},{}]
        if len(scrolls) < 9:
            article_pool_size = len(scrolls)
        else:
            article_pool_size = 9
        for x in range(0,article_pool_size):
            scroll[x].update({'id': ("/?id=" + str(scrolls[x][0])), 'url': scrolls[x][1], 'source': scrolls[x][2], 'post_date': scrolls[x][3], 'title': scrolls[x][4], 'top_image': scrolls[x][5]})
    return render_to_response('News/news_scroll_three.html', {'scrolls': scroll})

#def login(request):
    # c = {}
    # c.update(csrf(request))
    #return render_to_response('CYP/Login.html')

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('accounts/loggedin')
        # This is were we will swith to the other app
    else:
        return HttpResponseRedirect('accounts/invalid')
def loggedin(request):
    return render_to_response('news/home.html', {'fullname' : request.user.username})

def logout(request):
    auth.logout(request)
    return render_to_response('CYP/home.html')

def invalid(request):
    return render_to_response('CYP/invalid_login.html')

class UserFormView(View):
    for_class = UserForm
    template_name = 'CYP/Registartion.html'
    # c = {}
    # c.update(csrf(request))
    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            #normalizing data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = auth.authenticate(username = username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('News/home.html')

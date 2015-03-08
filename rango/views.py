from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

from datetime import datetime

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
        
    return render(request, 'rango/about.html', {'visits': count})


def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category = category).order_by('-views')

        context_dict['pages'] = pages

        context_dict['category'] = category

        context_dict['category_name_slug'] = category
        
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name
        
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors

    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

@login_required
def register_profile(request):
    if request.method == 'POST':
        instance = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(request.POST or None, instance=instance)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('profile', request.user.username)
        else:
            print form.errors

    else:
        form = UserProfileForm()

    context_dict = {'form': form}

    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

def search(request):

    result_list = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
            
    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass
            
    return redirect(url)

def profile(request, user_name):
    user = User.objects.get(username=user_name)
    context_dict = {}
    context_dict['username'] = user_name
    try:
        context_dict['profile'] = user.profile
    except:
        pass
    return render(request, 'rango/profile.html', context_dict)

def userspage(request):
    users = User.objects.order_by('username')
    
    return render(request, 'rango/users.html', {'users': users})

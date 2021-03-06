from multiprocessing import context

import neighborhood
from .forms import Neighbohoodform,ProfileForm, PostForm,CommentForm,AlertsForm,ShopForm
from .models import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import User
from django.contrib.auth import  logout as auth_logout
from django.contrib import messages

# Create your views here.
@login_required(login_url='/accounts/login/')
def index( request):
    
    title = 'Neighborhood'
    context ={
        'title': title,        
    }
    return render(request, 'index.html', context)

@login_required(login_url='/accounts/login/')
def home(request):
    current_user =request.user
    neighborhood_id = Profile.objects.get(user=current_user.id)
    N_hoods=Neighborhood.get_neighborhoods
    business=Shop.get_business_by_neighborhood(neighborhood_id.neighborhood)
    post=Post.objects.all()
    context={"posts":post,"user":current_user,"hoods":N_hoods,"business":business}
    return render(request, 'home.html',context)


@login_required(login_url='/accounts/login/')
def view_post(request,post_id):
    current_user = request.user
    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments =[]
    post = Post.objects.get(id=post_id)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = current_user
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    context= {"post":post,"form":form,"comments":comments}

    return render(request,'view_post.html',context)


def new_post(request):
    current_user = request.user
    profile =Profile.objects.filter(user=current_user.id) 
    
    if request.method=="POST":
        post_form =PostForm(request.POST,request.FILES)
        print()
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.username = current_user
            # post.neighborhood = profile.neighborhood
            # post.profile_image = profile.profile_image
            post.save()

        return redirect('home')

    else:
        post_form = PostForm()
    title = " New Post"
    return render(request,'post_item.html',{"form":post_form, 'title': title})


@login_required(login_url='login')
def profile(request,userID=None):
    if userID== None:
        userID=request.user.id
    # current_user= User.objects.get(id=userID)
    current_user= request.user
    user = current_user
    own_posts= Post.objects.filter(username=current_user)
    profile = Profile.objects.all()
    own_alerts = Alerts.objects.filter(author=current_user)
    context ={'posts':own_posts, 'alerts':own_alerts, 'profile':profile,'current_user': current_user}
    return render(request, 'profile.html', context)



@login_required(login_url='login')
def edit_profile(request, username):
    # user = User.objects.get(username=username)
    current_user = request.user  
    get_profile= Profile.objects.filter(user_id=request.user.id)
    if get_profile.exists():        
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)
            if  profile_form.is_valid():
                profile_form.save()
                return redirect('/profile/', current_user)
        else:        
            profile_form = ProfileForm(instance=request.user.profile)       
    else:
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)
            if  profile_form.is_valid():
                profile_form.save()
                return redirect('/profile/', current_user)
        else:        
            profile_form = ProfileForm() 
           
    context = {
        'prof_form': profile_form, 
        'current_user': current_user
    }
    return render(request, 'profile_edit.html', context)

@login_required(login_url='/accounts/login/')
def shops(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    shops= Shop.objects.filter(neighborhood=profile.neighborhood)
    
    return render( request, 'shops.html',{'shops': shops})

@login_required(login_url='/accounts/login/')
def new_shop(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method=="POST":
        form =ShopForm(request.POST,request.FILES)
        if form.is_valid():
            shop = form.save(commit = False)
            shop.owner = current_user
            shop.neighborhood = profile.neighborhood
            shop.save()

        return HttpResponseRedirect('/shops')

    else:
        form = ShopForm()

    return render(request,'shop_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def alerts(request):
    current_user=request.user
    profile=Profile.objects.get(user=current_user)
    alerts= Alerts.objects.filter(neighborhood=profile.neighborhood)
    context={'alerts': alerts}
    return render( request, 'alerts.html', context)

@login_required(login_url='/accounts/login/')
def new_alert(request):
    current_user=request.user
    profile=Profile.objects.get(user=current_user)
    if request.method=="POST":
        form =AlertsForm(request.POST)
        if form.is_valid():
            alerts = form.save(commit = False)
            alerts.author = current_user
            alerts.neighborhood = profile.neighborhood
            alerts.save()
        return HttpResponseRedirect('/alerts')
    else:
        form = AlertsForm()
    return render(request,'new_alert.html',{"form":form})

def search_business(request):
    current_user = request.user
    profile =Profile.objects.get(user=current_user)
    if 'business_name' in request.GET and request.GET["business_name"]:
        search_term = request.GET.get("business_name")
        searched_businesses = Shop.search_shop(search_term)
        message=f"{search_term}"
        context = {"message":message,"businesses":searched_businesses,"profile":profile}
        return render(request,'search.html',context)
    else:
        message="You haven't searched for any term"
        context = {"message":message}
        return render(request,'search.html',context)


def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return HttpResponseRedirect('/')

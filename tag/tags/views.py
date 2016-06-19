from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
# Create your views here.
from .models import *
from django.utils import timezone
import datetime

def tagpage(request, tagid):
    tag = Tag.objects.get(id = tagid)
    tagheadline = tag.name
    tagstreak = tag.streak
    tagowner = tag.owner
    if request.method == "POST":
        form = PassForm(request.POST)
        if form.is_valid():
            person = request.POST['username']
            PersonObject = User.objects.get(username = person)
            tag.owner = PersonObject
            tag.streak += 1
            tag.save()
            return HttpResponse("Success")
    else:
        form = PassForm()
        return render(request, 'tags/tag.html', { 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form})



def homepage(request):
    oldtags = Tag.objects.filter(created__lte = timezone.now() + datetime.timedelta(days = -1))
    oldtags.delete()
    return render(request, "tags/homepage.html")

def user_homepage(request):

        Tags = Tag.objects.filter(owner__username = request.user.username)

        tagslist = list(Tags.order_by())
        taglink = []
        for x in tagslist:
            taglink.append(x.id)
        alltogether = []
        for x in range(0,len(tagslist)):
            alltogether.append([])
            alltogether[x].append(tagslist[x])
            alltogether[x].append(taglink[x])


        lists = ", ".join(str(v) for v in tagslist)


        user = User.objects.get(username = request.user.username)
        response = "This is {} homepage. He/She's email is {} and his tags are: ".format(user.username,user.email,)
        if request.method == "POST":
            form = TagForm(request.POST)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.owner = request.user
                tag.save()
                return redirect('profile')
        else:
            form = TagForm()
            return render(request, 'tags/profile.html', {'response': response, 'username': request.user.username, 'form':form, 'lists': lists, 'taglink': taglink, 'alltogether':alltogether})
        return render(request, "tags/profile.html", {'response': response, 'username': request.user.username, 'form':form, 'lists': lists, 'taglink': taglink, 'alltogether':alltogether})


def sign_up(request):

        error = ""
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return redirect('login')
            else:
                
                return render(request, 'tags/sign_up.html', {'form':form, 'error':error})
        else:
            form = UserCreationForm()
            return render(request, 'tags/sign_up.html', {'form':form, 'error':error})


def loginuser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            auth = authenticate(username = request.POST['username'], password = request.POST['password'])
            if auth:
                login(request, auth)
                return redirect('homepage', username = request.POST['username'])
            else:
                return render(request, 'tags/loginfail.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'tags/login.html', {'form': form})

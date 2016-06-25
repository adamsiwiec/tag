from django.shortcuts import render,redirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
# Create your views here.
from .models import *
from django.utils import timezone
import datetime
from django.conf import settings

def pass_tag(request, username, tagid):
    try:
        taginmotion = Tag.objects.get(id = tagid)
    except:
        return redirect('profile')

    if request.user == taginmotion.owner:
        try:
            taginmotion.owner = User.objects.get(username = username)
            taginmotion.streak += 1
            owner = Credits.objects.get(user = taginmotion.original)
            owner.credits += 10
            taginmotion.created = timezone.now()
            owner.save()
            taginmotion.save()
            return redirect('taghomepage', tagid)
        except:
            return redirect('taghomepage', tagid)

    else:
        return redirect('profile')
def editprofile(request):
    if request.method == "POST":
        form = ExtraForm(request.POST, request.FILES)
        if form.is_valid():

            try:
                userupdate = Extra.objects.get(user = request.user)
                extra = form.save(commit = False)
                userupdate.profileimage = extra.profileimage
                userupdate.bio = extra.bio
                userupdate.save()
                return redirect('profile')
            except:
                extra = form.save(commit = False)
                extra.user = request.user
                extra.save()
                return redirect('profile')
        else:
            form = ExtraForm()
            return render(request, 'tags/editprofile.html', {'form':form})
    else:
        form = ExtraForm()
        return render(request, 'tags/editprofile.html', {'form':form})

def removefriend(request, removevar):
    try:
        removefriendship = Friendship.objects.get(friend__username = removevar , creator__username = request.user.username)
        removefriendship.delete()
        return redirect('profile')
    except:
        return redirect('profile')


def view_homepage(request, username):
    if username == request.user.username:
        return redirect('profile')
    try:
        extra = Extra.objects.get(user__username = username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    creditsowned = Credits.objects.get(user__username = username)
    creditsowned = creditsowned.credits
    Tags = Tag.objects.filter(owner__username = username)
    Friends = Friendship.objects.filter(creator__username = username)
    friendslist = list(Friends.order_by())
    tagslist = list(Tags.order_by())
    taglink = []
    newfriends = Friendship.objects.filter(creator__username = username, created__gte = timezone.now() - datetime.timedelta(days = 2))
    newfriendslist = list(newfriends.order_by())
    if len(newfriendslist) > 8:
        newfriendslist = ["You have over 8 new friends"]
    for x in tagslist:
        taglink.append(x.id)
    alltogether = []
    for x in range(0,len(tagslist)):
        alltogether.append([])
        alltogether[x].append(tagslist[x])
        alltogether[x].append(taglink[x])


    lists = ", ".join(str(v) for v in tagslist)


    user1 = User.objects.get(username = username)
    name = user1.first_name + " " + user1.last_name

    return render(request, 'tags/viewprofile.html', {'creditsowned':creditsowned, 'bio': bio, 'BASE_DIR':settings.BASE_DIR, 'extrapic': extrapic, 'newfriendslist':newfriendslist, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'username1':username,  'lists': lists, 'taglink': taglink, 'alltogether':alltogether})



def addfriends(request):
    if request.method == "POST":
        form = FriendshipForm(request.POST)
        if form.is_valid():
            try:
                if request.post['username'] == request.user.username:
                    redirect('profile')

                newfriendship = Friendship()
                newfriendship.creator = request.user
                newfriend = User.objects.get(username = request.POST['username'])
                newfriendship.friend = newfriend
                credits = Credits.objects.get(user= request.user)
                credits.credits += 10
                credits.save()
                newfriendship.save()
                return redirect('profile')
            except:
                return redirect('profile')

        else:
            form = FriendshipForm()
            return render(request, 'tags/friend.html', {'form':form})
    else:
        form = FriendshipForm()
        return render(request, 'tags/friend.html', {'form':form})

def tagpage(request, tagid):
    tag = Tag.objects.get(id = tagid)
    tagheadline = tag.name
    tagstreak = tag.streak
    tagowner = tag.owner
    if tag.owner == request.user:
        if request.method == "POST":
            form = PassForm(request.POST)
            if form.is_valid():
                person = request.POST['username']
                if person == request.user.username:
                    return redirect('profile')
                try:
                    PersonObject = User.objects.get(username = person)
                except:
                    return redirect('profile')
                tag.owner = PersonObject
                tag.streak += 1
                owner = Credits.objects.get(user = tag.original)
                owner.credits += 10
                tag.created = timezone.now()
                owner.save()
                tag.save()
                return redirect('taghomepage', tagid = tagid)

            else:
                form = PassForm()
                formbutton = '<button type = "submit">Create Tag</button>'
                return render(request, 'tags/tag.html', { 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form, 'formbutton': formbutton})
        else:
            form = PassForm()
            formbutton = '<button type = "submit">Create Tag</button>'
            suggestions = '<h1>Recommendations:</h1>'
            friends = list(Friendship.objects.filter(creator = request.user).order_by())
            recommendfriends = friends[:3]
            friendName = []
            for x in recommendfriends:
                friendName.append("{} {}".format(x.friend.first_name, x.friend.last_name))
            zipped = zip(recommendfriends, friendName)

            return render(request, 'tags/tag.html', {'tagid':tagid, 'zipped':zipped, 'suggestions':suggestions, 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form, 'formbutton': formbutton})
    else:
        form = ""
        formbutton = ""
        return render(request, 'tags/tag.html', { 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form, 'formbutton': formbutton})


def homepage(request):
    oldtags = Tag.objects.filter(created__lte = timezone.now() + datetime.timedelta(days = -1))
    oldtags.delete()
    return render(request, "tags/homepage.html")


def user_homepage(request):
        try:
            extra = Extra.objects.get(user = request.user)
            extrapic = extra.profileimage.url
            bio = extra.bio
        except:
            extrapic = False
            bio = ""

        if request.user.id == None:
            return redirect('login')
        Tags = Tag.objects.filter(owner__username = request.user.username)
        Friends = Friendship.objects.filter(creator__username = request.user.username)
        friendslist = list(Friends.order_by())
        tagslist = list(Tags.order_by())
        taglink = []
        creditsowned = Credits.objects.get(user = request.user)
        creditsowned = creditsowned.credits
        newfriends = Friendship.objects.filter(creator__username = request.user.username, created__gte = timezone.now() - datetime.timedelta(days = 2))
        newfriendslist = list(newfriends.order_by())
        if len(newfriendslist) > 8:
            newfriendslist = ["You have over 8 new friends"]
        for x in tagslist:
            taglink.append(x.id)
        alltogether = []
        for x in range(0,len(tagslist)):
            alltogether.append([])
            alltogether[x].append(tagslist[x])
            alltogether[x].append(taglink[x])


        lists = ", ".join(str(v) for v in tagslist)


        user = User.objects.get(username = request.user.username)
        name = user.first_name + " " + user.last_name
        if request.method == "POST":
            form = TagForm(request.POST)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.owner = request.user
                tag.original = request.user
                subtractcred = Credits.objects.get(user = request.user)
                if subtractcred.credits >= 25:
                    subtractcred.credits -= 25
                    subtractcred.save()
                    tag.save()

                return redirect('profile')
            else:

                form = TagForm()
                return render(request, 'tags/profile.html', { 'creditsowned':creditsowned, 'bio':bio,'extrapic':extrapic, 'newfriendslist':newfriendslist, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'form':form, 'lists': lists, 'taglink': taglink, 'alltogether':alltogether})

        else:

            form = TagForm()
            return render(request,  'tags/profile.html', {'creditsowned':creditsowned, 'bio':bio,'extrapic':extrapic, 'newfriendslist':newfriendslist, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'form':form, 'lists': lists, 'taglink': taglink, 'alltogether':alltogether})



def sign_up(request):

        if request.method == "POST":
            form = UserCreate(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                credit = Credits()
                user.save()
                credit.user = user
                credit.credits = 200
                credit.save()

                return redirect('login')
            else:
                form = UserCreate()
                return render(request, 'tags/sign_up.html', {'form':form})
        else:
            form = UserCreate()
            return render(request, 'tags/sign_up.html', {'form':form})

import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings
from rest_framework import generics

from . import forms
from . import models
from . import serializers


def getextra(request):
    try:
        extra = models.Extra.objects.get(user__username=request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""

    return extrapic, bio


class ListTags(generics.ListCreateAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class UpdateTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


# DISPLAYS HOW IT WORKS PAGE
def works(request):
    extrapic, bio = getextra(request)
    return render(request, 'tags/works.html', {'extrapic': extrapic})


# LOG IN USER
def login_user(request):
    extrapic, bio = getextra(request)

    username = password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profile')
    form = forms.LoginForm()
    return render(request, 'tags/login.html', {'form': form,
                                               'extrapic': extrapic})


# PASS ON A TAG TO ANOTHER USER. NOT MEANT FOR USERS VIEWING, ONLY FOR REDIRECTS
def pass_tag(request, username, tagid):

    try:
        taginmotion = models.Tag.objects.get(id=tagid)
    except:
        return redirect('profile')

    if request.user == taginmotion.owner:
        try:
            taginmotion.owner = models.User.objects.get(username=username)
            taginmotion.streak += 1
            owner = models.Credits.objects.get(user=taginmotion.original)
            owner.credits += 10
            taginmotion.created = timezone.now()
            owner.save()
            taginmotion.save()
            return redirect('taghomepage', tagid)
        except:
            return redirect('taghomepage', tagid)

    else:
        return redirect('profile')


# EDIT YOUR PROFILE OR CHANGE A PASSWORD
def editprofile(request):
    # CREDITS
    creditsownedmodel = models.Credits.objects.get(user__username=request.user.username)
    creditsowned = creditsownedmodel.credits
# MAKES NAME
    user = models.User.objects.get(username=request.user.username)
    name = user.first_name + " " + user.last_name
# EXTRA PROFILE INFO
    extrapic, bio = getextra(request)

    if request.method == "POST":
        form = forms.ExtraForm(request.POST, request.FILES)
        if form.is_valid():

            try:
                userupdate = models.Extra.objects.get(user=request.user)
                extra = form.save(commit=False)
                userupdate.profileimage = extra.profileimage
                userupdate.bio = extra.bio
                userupdate.save()
                return redirect('profile')
            except:
                extra = form.save(commit=False)
                extra.user = request.user
                extra.save()
                return redirect('profile')
        else:
            form = forms.ExtraForm()
            return render(
                request,
                'tags/editprofile.html',
                {'form': form,
                    'extrapic': extrapic,
                    'bio': bio,
                    'name': name,
                    'creditsowned': creditsowned})
    else:
        form = forms.ExtraForm()
        return render(
            request,
            'tags/editprofile.html',
            {'form': form,
                'extrapic': extrapic,
                'bio': bio,
                'name': name,
                'creditsowned': creditsowned})


# REMOVE A FRIEND (SO SAD)
def removefriend(request, removevar):
    try:
        removefriendship = models.Friendship.objects.get(
            friend__username=removevar,
            creator__username=request.user.username)

        removefriendship.delete()
        return redirect('profile')
    except:
        return redirect('profile')


# FOR OUTSIDE USERS TO VIEW ANOTHER USERS PROFILE
def view_homepage(request, username):
    # LOGICAL REDIRECT
    if username == request.user.username:
        return redirect('profile')
    # EXTRA PROFILE INFO
    extrapic, bio = getextra(request)

    try:
        extra = models.Extra.objects.get(user__username=username)
        extrapic1 = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic1 = False
        bio = ""


# CREDITS
    creditsowned = models.Credits.objects.get(user__username=username)
    creditsowned = creditsowned.credits

# TAGS
    Tags = models.Tag.objects.filter(owner__username=username)
    tagslist = list(Tags.order_by())
    taglink = []

# FRIENDS
    Friends = models.Friendship.objects.filter(creator__username=username)
    my_friends = models.Friendship.objects.filter(
        creator__username=request.user.username)
    my_friendslist = list(my_friends.order_by())
    friendslist = list(Friends.order_by())
    newfriends = models.Friendship.objects.filter(
        creator__username=username,
        created__gte=timezone.now() - datetime.timedelta(days=2))
    newfriendslist = list(newfriends.order_by())
# PERMISSION TO REMOVE FRIEND
    try:
        if models.Friendship.objects.get(friend__username=username) in my_friendslist:
            permission = True
    except:
        permission = False

# CREATE A TEMPLATE COMPATIBLE LIST OF FRIENDS
    if len(newfriendslist) > 8:
        newfriendslist = ["You have {} new friends".format(len(newfriendslist))]
    for x in tagslist:
        taglink.append(x.id)
    alltogether = []
    for x in range(0, len(tagslist)):
        alltogether.append([])
        alltogether[x].append(tagslist[x])
        alltogether[x].append(taglink[x])


# MAKES NAME
    user = models.User.objects.get(username=username)
    name = user.first_name + " " + user.last_name

    return render(
        request,
        'tags/viewprofile.html',
        {'permission': permission,
            'creditsowned': creditsowned,
            'bio': bio,
            'BASE_DIR': settings.BASE_DIR,
            'extrapic': extrapic,
            'extrapic1': extrapic1,
            'friendslist': friendslist,
            'name': name,
            'username': request.user.username,
            'username1': username,
            'alltogether': alltogether})


# PAGE FOR ADDING FRIENDS BASED ON USERNAME AND SUGGESTIONS
def addfriends(request):
    extrapic, bio = getextra(request)

    if request.method == "POST":
        form = forms.FriendshipForm(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['username'] == request.user.username:
                    return redirect('profile')
                newfriendship = models.Friendship()
                newfriendship.creator = request.user
                newfriend = models.User.objects.get(username=request.POST['username'])
                newfriendship.friend = newfriend
                credits = models.Credits.objects.get(user=request.user)
                credits.credits += 10
                credits.save()
                newfriendship.save()
                return redirect('profile')
            except:
                formerror = "There is no user with that username"
                form = forms.FriendshipForm()
                return render(
                    request,
                    'tags/friend.html',
                    {'formerror': formerror,
                        'form': form,
                        'extrapic': extrapic})
        else:
            form = forms.FriendshipForm()
            return render(
                request,
                'tags/friend.html',
                {'formerror': formerror,
                    'form': form,
                    'extrapic': extrapic})
    else:
        form = forms.FriendshipForm()
        return render(
            request,
            'tags/friend.html',
            {'form': form, 'extrapic': extrapic})


# DISPLAYS INFORMATION ABOUT A SPECIFIC TAG
def tagpage(request, tagid):

    extrapic, bio = getextra(request)
    tag = models.Tag.objects.get(id=tagid)
    if tag.owner == request.user:
        permission = True
    else:
        permission = False
    tagheadline = tag.name
    tagstreak = tag.streak
    tagowner = tag.owner
    if tag.owner == request.user:
        if request.method == "POST":
            form = forms.PassForm(request.POST)
            if form.is_valid():
                person = request.POST['username']
                if person == request.user.username:
                    return redirect('profile')
                try:
                    PersonObject = models.User.objects.get(username=person)
                except:
                    return redirect('profile')
                tag.owner = PersonObject
                tag.streak += 1
                owner = models.Credits.objects.get(user=tag.original)
                owner.credits += 10
                tag.created = timezone.now()
                owner.save()
                tag.save()
                return redirect('taghomepage', tagid=tagid)

            else:
                form = forms.PassForm()
                formbutton = '<button type = "submit">Create Tag</button>'
                return render(
                    request,
                    'tags/tag.html',
                    {'tagheadline': tagheadline,
                        'tagstreak': tagstreak,
                        'tagowner': tagowner,
                        'form': form,
                        'formbutton': formbutton})
        else:
            form = forms.PassForm()
            formbutton = '<button type = "submit">Create Tag</button>'
            suggestions = '<h1>Recommendations:</h1>'
            friends = list(models.Friendship.objects.filter(
                creator=request.user).order_by())

            recommendfriends = friends[:3]
            friendName = []
            for x in recommendfriends:
                friendName.append("{} {}".format(x.friend.first_name,
                                                 x.friend.last_name))
            zipped = zip(recommendfriends, friendName)

            return render(
                request,
                'tags/tag.html',
                {'tagid': tagid,
                    'zipped': zipped,
                    'suggestions': suggestions,
                    'tagheadline': tagheadline,
                    'tagstreak': tagstreak,
                    'tagowner': tagowner,
                    'form': form,
                    'formbutton': formbutton,
                    'extrapic': extrapic,
                    'permission': permission})
    else:
        form = ""
        formbutton = ""
        return render(
            request,
            'tags/tag.html',
            {'tagheadline': tagheadline,
             'tagstreak': tagstreak,
             'tagowner': tagowner,
             'form': form,
             'formbutton': formbutton,
             'extrapic': extrapic,
             'permission': permission})


# DISPLAY'S LANDING PAGE
def homepage(request):
    extrapic, bio = getextra(request)
    return render(request, "tags/homepage.html", {'extrapic': extrapic})


# USER HOMEPAGE IF THEY ARE LOGGED IN
def user_homepage(request):
    # GET EXTRA PROFILE INFO
        extrapic, bio = getextra(request)

# REDIRECT IF NOT LOGGED IN
        if request.user.id is None:
            return redirect('login')
# TAGS
        Tags = models.Tag.objects.filter(owner__username=request.user.username)
        tagslist = list(Tags.order_by())
        taglink = []

# FRIENDS
        Friends = models.Friendship.objects.filter(
            creator__username=request.user.username)
        friendslist = list(Friends.order_by())
        newfriends = models.Friendship.objects.filter(
            creator__username=request.user.username,
            created__gte=timezone.now() - datetime.timedelta(days=2))
        newfriendslist = list(newfriends.order_by())

# CREDITS
        creditsowned = models.Credits.objects.get(user=request.user)
        creditsowned = creditsowned.credits

# MAKE A TEMPLATE COMPATIBLE FORMAT
        if len(newfriendslist) > 8:
            newfriendslist = ["You have over 8 new friends"]
        for x in tagslist:
            taglink.append(x.id)
        alltogether = []
        for x in range(0, len(tagslist)):
            alltogether.append([])
            alltogether[x].append(tagslist[x])
            alltogether[x].append(taglink[x])


# GETS USER AND NAME
        user = models.User.objects.get(username=request.user.username)
        name = user.first_name + " " + user.last_name

# TAG CREATION FORM
        if request.method == "POST":
            form = forms.TagForm(request.POST)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.owner = request.user
                tag.original = request.user
                subtractcred = models.Credits.objects.get(user=request.user)
                if subtractcred.credits >= 25:
                    subtractcred.credits -= 25
                    subtractcred.save()
                    tag.save()

                return redirect('profile')
            else:
                formerrors = form.errors
                print(form.errors)
                form = forms.TagForm()
                return render(
                    request,
                    'tags/profile.html',
                    {'formerrors': formerrors,
                     'creditsowned': creditsowned,
                     'bio': bio,
                     'extrapic': extrapic,
                     'newfriendslist': newfriendslist,
                     'friendslist': friendslist,
                     'name': name,
                     'username': request.user.username,
                     'form': form,
                     'alltogether': alltogether})

        else:

            form = forms.TagForm()
            return render(
                request,
                'tags/profile.html',
                {'creditsowned': creditsowned,
                 'bio': bio,
                 'extrapic': extrapic,
                 'newfriendslist': newfriendslist,
                 'friendslist': friendslist,
                 'name': name,
                 'username': request.user.username,
                 'form': form,
                 'alltogether': alltogether})


# SIGN UP PAGE USING DEFAULT FORM PAGE
def sign_up(request):
    extrapic, bio = getextra(request)

    if request.method == "POST":
        form = forms.UserCreate(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            credit = models.Credits()
            user.save()
            credit.user = user
            credit.credits = 200
            credit.save()

            return redirect('login')
        else:
            form_errors = form.errors
            form = forms.UserCreate()
            return render(
                request,
                'tags/sign_up.html',
                {'form': form,
                 'form_errors': form_errors,
                 'extrapic': extrapic})
    else:
        form = forms.UserCreate()
        return render(
            request,
            'tags/sign_up.html',
            {'form': form, 'extrapic': extrapic})

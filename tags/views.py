from django.shortcuts import render,redirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.utils import timezone
import datetime
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

# DISPLAYS HOW IT WORKS PAGE
def works(request):
    try:
        extra = Extra.objects.get(user__username = request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    return render(request,'tags/works.html',{'extrapic':extrapic,})
# LOG IN USER
def login_user(request):
    try:
        extra = Extra.objects.get(user__username = request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""

    #logout(request)
    username = password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profile')
    form = LoginForm()
    return render(request, 'tags/login.html', {'form':form, 'extrapic':extrapic,})


# PASS ON A TAG TO ANOTHER USER (NOT MEANT FOR USERS VIEWING, ONLY FOR REDIRECTS)
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



# EDIT YOUR PROFILE OR CHANGE A PASSWORD
def editprofile(request):
# CREDITS
    creditsowned = Credits.objects.get(user__username = request.user.username)
    creditsowned = creditsowned.credits
# MAKES NAME
    user = User.objects.get(username = request.user.username)
    name = user.first_name + " " + user.last_name
# EXTRA PROFILE INFO
    try:
        extra = Extra.objects.get(user__username = request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""


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
            return render(request, 'tags/editprofile.html', {'form':form, 'extrapic':extrapic, 'bio': bio, 'name':name,'creditsowned':creditsowned,})
    else:
        form = ExtraForm()
        return render(request, 'tags/editprofile.html', {'form':form, 'extrapic':extrapic, 'bio': bio, 'name':name,'creditsowned':creditsowned,})



# REMOVE A FRIEND (SO SAD)
def removefriend(request, removevar):
    try:
        removefriendship = Friendship.objects.get(friend__username = removevar , creator__username = request.user.username)
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
    try:
        extra = Extra.objects.get(user__username = request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    try:
        extra = Extra.objects.get(user__username = username)
        extrapic1 = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic1 = False
        bio = ""


# CREDITS
    creditsowned = Credits.objects.get(user__username = username)
    creditsowned = creditsowned.credits

# TAGS
    Tags = Tag.objects.filter(owner__username = username)
    tagslist = list(Tags.order_by())
    taglink = []

# FRIENDS
    Friends = Friendship.objects.filter(creator__username = username)
    my_friends = Friendship.objects.filter(creator__username = request.user.username)
    my_friendslist = list(my_friends.order_by())
    print(my_friendslist)
    friendslist = list(Friends.order_by())
    newfriends = Friendship.objects.filter(creator__username = username, created__gte = timezone.now() - datetime.timedelta(days = 2))
    newfriendslist = list(newfriends.order_by())
# PERMISSION TO REMOVE FRIEND
    try:
        if Friendship.objects.get(friend__username = username) in my_friendslist:
            permission = True
        else:
            permission = False
    except:
        return redirect("profile")
# CREATE A TEMPLATE COMPATIBLE LIST OF FRIENDS
    if len(newfriendslist) > 8:
        newfriendslist = ["You have {} new friends".format(len(newfriendslist))]
    for x in tagslist:
        taglink.append(x.id)
    alltogether = []
    for x in range(0,len(tagslist)):
        alltogether.append([])
        alltogether[x].append(tagslist[x])
        alltogether[x].append(taglink[x])


# MAKES NAME
    user = User.objects.get(username = username)
    name = user.first_name + " " + user.last_name

    return render(request, 'tags/viewprofile.html', {'permission':permission, 'creditsowned':creditsowned, 'bio': bio, 'BASE_DIR':settings.BASE_DIR, 'extrapic': extrapic, 'extrapic1': extrapic1, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'username1':username, 'alltogether':alltogether})



# PAGE FOR ADDING FRIENDS BASED ON USERNAME AND SUGGESTIONS
def addfriends(request):
    try:
        extra = Extra.objects.get(user = request.user)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    if request.method == "POST":
        form = FriendshipForm(request.POST)
        if form.is_valid():
            try:
                if request.POST['username'] == request.user.username:
                    return redirect('profile')
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
            return render(request, 'tags/friend.html', {'form':form, 'extrapic':extrapic,})
    else:
        form = FriendshipForm()
        return render(request, 'tags/friend.html', {'form':form, 'extrapic':extrapic,})



# DISPLAYS INFORMATION ABOUT A SPECIFIC TAG
def tagpage(request, tagid):

    try:
        extra = Extra.objects.get(user = request.user)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    tag = Tag.objects.get(id = tagid)
    if tag.owner == request.user:
        permission = True;
    else:
        permission = False;
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

            return render(request, 'tags/tag.html', {'tagid':tagid, 'zipped':zipped, 'suggestions':suggestions, 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form, 'formbutton': formbutton, 'extrapic':extrapic, 'permission':permission})
    else:
        form = ""
        formbutton = ""
        return render(request, 'tags/tag.html', { 'tagheadline':tagheadline, 'tagstreak':tagstreak, 'tagowner': tagowner, 'form':form, 'formbutton': formbutton, 'extrapic':extrapic, 'permission':permission})



# DELETES OLD USERS AND DISPLAY'S LANDING PAGE, MIGHT DELETE IF THIS IS INEFFICIENT
def homepage(request):
    oldtags = Tag.objects.filter(created__lte = timezone.now() + datetime.timedelta(days = -1))
    oldtags.delete()
    try:
        extra = Extra.objects.get(user = request.user)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    return render(request, "tags/homepage.html", {'extrapic':extrapic})



# USER HOMEPAGE IF THEY ARE LOGGED IN
def user_homepage(request):
# GET EXTRA PROFILE INFO
        try:
            extra = Extra.objects.get(user = request.user)
            extrapic = extra.profileimage.url
            bio = extra.bio
        except:
            extrapic = False
            bio = ""

# REDIRECT IF NOT LOGGED IN
        if request.user.id == None:
            return redirect('login')
# TAGS
        Tags = Tag.objects.filter(owner__username = request.user.username)
        tagslist = list(Tags.order_by())
        taglink = []

# FRIENDS
        Friends = Friendship.objects.filter(creator__username = request.user.username)
        friendslist = list(Friends.order_by())
        newfriends = Friendship.objects.filter(creator__username = request.user.username, created__gte = timezone.now() - datetime.timedelta(days = 2))
        newfriendslist = list(newfriends.order_by())

# CREDITS
        creditsowned = Credits.objects.get(user = request.user)
        creditsowned = creditsowned.credits

# MAKE A TEMPLATE COMPATIBLE FORMAT
        if len(newfriendslist) > 8:
            newfriendslist = ["You have over 8 new friends"]
        for x in tagslist:
            taglink.append(x.id)
        alltogether = []
        for x in range(0,len(tagslist)):
            alltogether.append([])
            alltogether[x].append(tagslist[x])
            alltogether[x].append(taglink[x])


# GETS USER AND NAME
        user = User.objects.get(username = request.user.username)
        name = user.first_name + " " + user.last_name

# TAG CREATION FORM
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
                return render(request, 'tags/profile.html', { 'creditsowned':creditsowned, 'bio':bio,'extrapic':extrapic, 'newfriendslist':newfriendslist, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'form':form, 'alltogether':alltogether})

        else:

            form = TagForm()
            return render(request,  'tags/profile.html', {'creditsowned':creditsowned, 'bio':bio,'extrapic':extrapic, 'newfriendslist':newfriendslist, 'friendslist': friendslist, 'name': name, 'username': request.user.username, 'form':form, 'alltogether':alltogether})



# SIGN UP PAGE USING DEFAULT FORM PAGE
def sign_up(request):
    try:
        extra = Extra.objects.get(user__username = request.user.username)
        extrapic = extra.profileimage.url
        bio = extra.bio
    except:
        extrapic = False
        bio = ""
    if request.method == "POST":
        form = UserCreate(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            credit = Credits()
            extra = Extra()
            user.save()
            extra.user = user
            extra.save()
            credit.user = user
            credit.credits = 200
            credit.save()

            return redirect('login')
        else:
            form = UserCreate()
            return render(request, 'tags/sign_up.html', {'form':form, 'extrapic':extrapic,})
    else:
        form = UserCreate()
        return render(request, 'tags/sign_up.html', {'form':form, 'extrapic':extrapic,})

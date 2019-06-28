from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages #for messages
from .models import * #For adding in models, * captures all
import bcrypt
import re

def index(request):
    return render(request, 'wish_app/index.html')


def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        last = User.objects.last()
        request.session['userid'] = last.id
        request.session['name'] = last.first_name
        return redirect('/dashboard')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else :
        passcheck = User.objects.return_user(request.POST)
        if bcrypt.checkpw(request.POST['password'].encode(), passcheck.password.encode()):
            request.session['userid'] = passcheck.id
            request.session['name'] = passcheck.first_name
            return redirect('/dashboard')
        else:
            messages.error(request, "Incorrect Password", extra_tags='login')
            return redirect('/')


def dashboard(request):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        user = User.objects.return_user_on_uid(request.session['userid'])
        wishes = Wish.objects.get_wishes(request.session['userid'])
        granted = Wish.objects.get_granted()
        content = {
            'name': request.session['name'],
            'wishes': wishes,
            'granted': granted,
            'user': user,
        }
        return render(request, 'wish_app/main.html', content)


def new_wish(request):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        content = {
            'name': request.session['name'],
        }
        return render(request, 'wish_app/makewish.html', content)


def create_wish(request):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create')
            return redirect('/wishes/new')
        else:
            user = User.objects.get(id=request.session['userid'])
            Wish.objects.create(wish=request.POST['wish'], desc=request.POST['desc'], created_by=user)
            return redirect('/dashboard')


def show_wish(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        this_wish = Wish.objects.get(id=wid)
        content = {
            'name': request.session['name'],
            'wish': this_wish,
        }
        return render(request, 'wish_app/showwish.html', content)


def edit_wish(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        this_wish = Wish.objects.get(id=wid)
        content = {
            'name': request.session['name'],
            'wish': this_wish,
        }
        return render(request, 'wish_app/editwish.html', content)


def update_wish(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='update')
            return redirect('/wishes/'+str(wid)+'/edit')
        else:
            revise_wish = Wish.objects.get(id=wid)
            revise_wish.wish=request.POST['wish']
            revise_wish.desc=request.POST['desc']
            revise_wish.save()
            return redirect('/dashboard')


def delete_wish(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        delete_wish = Wish.objects.get(id=wid)
        delete_wish.delete()
        return redirect('/dashboard')


def like_wish(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        uid = request.session['userid']
        Wish.objects.like_wish(uid, wid)
        return redirect('/dashboard')


def granted(request, wid):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        Wish.objects.wish_granted(wid)
        return redirect('/dashboard')


def stats_page(request):
    if not 'userid' in request.session:
        messages.error(request, "Please Log In", extra_tags='login')
        return redirect('/')
    else:
        uid = request.session['userid']
        user = User.objects.return_user_on_uid(uid)
        total_granted = len(Wish.objects.filter(granted = True))
        user_granted = len(Wish.objects.filter(created_by = user, granted = True))
        user_pending = len(Wish.objects.filter(created_by = user, granted = False))
        content = {
            'name': request.session['name'],
            'total_granted': total_granted,
            'user_granted': user_granted,
            'user_pending': user_pending,
        }
        return render(request, 'wish_app/wishstats.html', content)



def logout(request):
    request.session.clear()
    return redirect('/')

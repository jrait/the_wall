from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime,timedelta

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }

    return render(request,'index.html',context)

def register(request):
    errors = User.objects.validator(request.POST)
    if len (errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        logged_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['userid'] = logged_user.id
        request.session['userfirst'] = logged_user.first_name
        request.session['access'] = 'registered'
        return redirect('/success')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')

    messages.error(request,"User or password is incorrect")
    return redirect('/')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        message_cutoff = datetime.now()-timedelta(minutes = 30)+timedelta(hours = 6)
        context={
            'user': User.objects.get(id = request.session['userid']),
            'all_messages':Message.objects.all(),
            'all_comments':Comments.objects.all(),
            'message_cutoff':message_cutoff,
        }
        test = Message.objects.get(id=4)
        print(message_cutoff)
        print(test.created_at)
        return render(request,'home.html',context)
        

def logout(request):
    request.session.clear()
    return redirect('/')

def post(request):
    if request.method == 'POST':
        post_user = User.objects.get(id=int(request.session['userid']))
        Message.objects.create(message = request.POST['message'],user = post_user)
    return redirect('/success')

def comment(request):
    if request.method == 'POST':
        post_user = User.objects.get(id=int(request.session['userid']))
        post_message = Message.objects.get(id=int(request.POST['message_id']))
        Comments.objects.create(comment = request.POST['message'],user = post_user,message = post_message)
    return redirect('/success')

def delete(request,message_id,user_id):
    if request.session['userid'] == user_id:
        delete_message = Message.objects.get(id = message_id)
        delete_message.delete()
        return redirect('/success')
    else:
        return redirect('/success')
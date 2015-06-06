from django.shortcuts import render, HttpResponseRedirect
from .forms           import SignUpForm
from django.contrib   import messages
from django.conf      import settings
from django.core.mail import send_mail

from django.core.context_processors import csrf
from django.contrib import auth

# Create your views here.
def home(request):
    
    form = SignUpForm(request.POST or None)
    
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        subject     = 'Hello ' + form_data.first_name + ' ' + form_data.last_name + '!'
        message     = 'This is a test message from lucasberge.com'
        from_email  = settings.EMAIL_HOST_USER
        to_list     = [form_data.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.success(request, 'Email successfully sent!')
        return HttpResponseRedirect('/')
        
    return render(request, "signup.html", locals())
    
def contact(request):
    
    return render(request, "contact.html", locals())

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html', locals())

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        messages.success(request, 'Successful Login!')
        return HttpResponseRedirect('/')
    else:
        messages.info(request, 'Invalid Username or Password!')
        return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    messages.warning(request, 'You have successfully logged out!')
    return HttpResponseRedirect('/')
    #return render(request, 'logout.html', {'full_name' : request.user.username})

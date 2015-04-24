from django.shortcuts import render, HttpResponseRedirect
from .forms           import SignUpForm
from django.contrib   import messages
from django.conf      import settings
from django.core.mail import send_mail
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
        messages.success(request, 'Django messaging system!')
        return HttpResponseRedirect('/thank-you/')
        
    return render(request, "signup.html", locals())
    
    
def thankyou(request):
    
    return render(request, "thankyou.html", locals())
    
def contact(request):
    
    return render(request, "contact.html", locals())
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            subject = f"Contact Form Submission from {name}"
            body = f"Name: {name}\nEmail: {email}\nMessage:\n\n{message}"
            send_mail(subject, body, email, ['pritomrabidas102@gmail.com'])
            return HttpResponse("Message sent successfully!")
        else:
            return HttpResponse("Please fill in all fields.")

    return render(request, 'contact/contact.html')

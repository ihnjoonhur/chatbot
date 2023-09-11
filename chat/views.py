from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User

import openai
import os  # Add this to use environment variables

# Secure your API key by using environment variables or Django's secrets
openai.api_key = os.environ["OPENAI_API_KEY"]



def ask_openai(message):
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = message,
            max_tokens=150,
            n=1,
            stop=None, 
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        return answer


# Create your views here.

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Use the ask_openai function to get the response
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Passwords do not match"
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    return render(request)
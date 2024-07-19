from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils import get_yt_link, get_transcription, generate_blog_from_transcription
from .models import BlogPost


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
       
        ytLink = data['link']

        title = get_yt_link(ytLink)
            
        transcription = get_transcription(ytLink)
        if not transcription:
            return JsonResponse({'error:' 'Error fetching transcription'}, status=500)
        
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error:' 'Error generating blog content'}, status=500)
        
        new_blog_article = BlogPost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_link= ytLink,
            generated_content= blog_content
        )
        
        new_blog_article.save()
        
        return JsonResponse({'content': blog_content})
       
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "blogs.html", {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, "blog-details.html", {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Username or password is wrong!'
            return render(request, 'login.html', {'error_message': error_message})
            
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Username or email is taken!'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match!'
            return render(request, 'register.html', {'error_message': error_message})
        
    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('/')
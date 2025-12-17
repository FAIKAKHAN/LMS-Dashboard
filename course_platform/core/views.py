from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Category, Profile, Lesson, Comment, Contact
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    courses = Course.objects.all()[:6]
    categories = Category.objects.all()
     
    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)

def playlist(request, id):
    course = get_object_or_404(Course, id=id)
    lessons = course.lessons.all()
    context = {'course': course, 'lessons': lessons}
    return render(request, 'playlist.html', context)

def watch_video(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    course = lesson.course
    comments = lesson.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'add_comment' in request.POST and request.user.is_authenticated:
            content = request.POST.get('comment_box')
            Comment.objects.create(user=request.user, lesson=lesson, content=content)
            return redirect('watch_video', id=id)
            
    context = {   
        'lesson': lesson,
        'course': course,
        'comments': comments
    }
    return render(request, 'watch-video.html', context)

def teachers(request):
    tutors = Profile.objects.filter(role='Teacher')
    context = {'tutors': tutors}
    return render(request, 'teachers.html', context)

def teacher_profile(request, username):
    tutor = get_object_or_404(Profile, user__username=username, role='Teacher')
    courses = tutor.course_set.all()
    context = {'tutor': tutor, 'courses': courses}
    return render(request, 'teacher_profile.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'profile.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        message = request.POST.get('msg')
        
        Contact.objects.create(name=name, email=email, phone=phone, message=message)
        messages.success(request, 'Message sent successfully!')
        return redirect('contact')
        
    return render(request, 'contact.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        
        # Authenticate using email (Django defaults to username, but we can try to find user by email)
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            
    return render(request, 'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        c_pass = request.POST.get('c_pass')
        
        if password != c_pass:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')
            
        user = User.objects.create_user(username=email.split('@')[0], email=email, password=password)
        user.first_name = name
        user.save()
        
        # Create Profile
        Profile.objects.create(user=user, role='Student', profession='Student')
        
        login(request, user)
        messages.success(request, 'Registered successfully!')
        return redirect('home')
        
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

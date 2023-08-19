from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.decorators import login_required
from core import settings
from .models import User_Profile, Course
from django.contrib.auth import authenticate, login, logout
from .models import Course, Module, Lesson, Assessment, Resource, Student, UserCode
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import UserCreationForm
from django.http import JsonResponse
import json

def save_user_codes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        html_code = data.get("html_code")
        css_code = data.get("css_code")
        js_code = data.get("js_code")

        user_code, created = UserCode.objects.get_or_create(user=user)
        user_code.html_code = html_code
        user_code.css_code = css_code
        user_code.js_code = js_code
        user_code.save()

        return JsonResponse({"message": "User codes saved successfully."})

    return JsonResponse({"message": "Invalid request."}, status=400)

def get_user_codes(request):
    user = request.user
    try:
        user_code = UserCode.objects.get(user=user)
        return JsonResponse(
            {
                "html_code": user_code.html_code,
                "css_code": user_code.css_code,
                "js_code": user_code.js_code,
            }
        )
    except UserCode.DoesNotExist:
        return JsonResponse({"message": "User codes not found."}, status=404)




@login_required
def home(request):

    user = User.objects.get(username=request.user)

    return render(request, 'index.html', {'user':user})


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'



@login_required
def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    user = request.user  # Use the request.user object directly

    try:
        student = Student.objects.get(user=user)
        is_enrolled = course in student.enrolled_courses.all()
    except Student.DoesNotExist:
        is_enrolled = False

    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': is_enrolled, 'user': user})


@login_required
def enroll_course(request, slug):  # Use slug parameter
    if request.user.is_authenticated:
        course = get_object_or_404(Course, slug=slug)
        student, created = Student.objects.get_or_create(user=request.user)

        if course not in student.enrolled_courses.all():
            student.enrolled_courses.add(course)
            return redirect('academy:course_detail', slug=slug)
        else:
            messages.info(request, 'You are already enrolled in this course.')
            return redirect('academy:course_detail', slug=slug)
    else:
        # Handle non-authenticated users (redirect to login or show a message)
        messages.error(request, 'Sign Up to Enroll')
        return redirect('academy:signin')  # Redirect to your login view


def user_dashboard(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            enrolled_courses = student.enrolled_courses.all()
            return render(request, 'user/user_dashboard.html', {'enrolled_courses': enrolled_courses})
        except Student.DoesNotExist:
            return render(request, 'user/user_dashboard.html', {'message': 'You are not enrolled in any courses yet.'})
    else:
        return render(request, 'user/user_dashboard.html', {'message': 'Please log in to access your dashboard.'})


def html_css(request):
    return render(request, 'courses/html_css.html')


def nodejs(request):
    return render(request, 'courses/nodejs.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_authenticated:
                login(request, user)
            
            # Send welcome email
            subject = "Welcome to Nuel-Green ICT!!"
            message = (
                f"Hello {user.username}!!\n"
                "Welcome to Nuel-Green ICT!!\n"
                "Thank you for visiting our website.\n"
                "We have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\n"
                "Thanking You\nAnubhav Madhav"
            )
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            if not user.is_active:
                logout(request)
                messages.info(
                    request,
                    "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.",
                )
            else:
                messages.success(request, "Your Account has been created successfully!!")

            return redirect("academy:home")
    else:
        form = UserCreationForm()

    return render(request, 'user/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully signed in!")
            return redirect('academy:home')  # Redirect to your desired URL after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'user/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('academy:home')  # Redirect to the 'academy:home' URL name


def create_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        f_name = request.POST.get('first_name')
        m_name = request.POST.get('middle_name')
        l_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        edu_qual = request.POST.get('educational_qualification')
        email = request.POST.get('email_address')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        emp_status = request.POST.get('employment_status')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        comfirm_password = request.POST.get('confirm_password')
        how_did_you_hear = request.POST.get('how_did_you_hear')
        career_path = request.POST.get('career_path')

        if User_Profile.objects.filter(username=username).exists():
                messages.error(request, 'User with the same username already exists')
        elif User_Profile.objects.filter(email=email).exists():
            messages.error(request, 'User with the same email already exists')
        
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters')

        if password != comfirm_password:
            messages.error(request, 'Password does not match')

       
        user = User_Profile.objects.create(
            username=username,
            f_name=f_name,
            m_name=m_name,
            l_name=l_name,
            gender=gender,
            edu_qual=edu_qual,
            email=email,
            country=country,
            street_address=street_address,
            emp_status=emp_status,
            phone_number=phone_number,
            password=password,
            how_did_you_hear=how_did_you_hear,
            career_path=career_path
        )

        context = {
            'f_name':f_name,
            'l_name':l_name
        }

        user.save()

        return redirect('signin')

    return render(request, 'user/signup.html', context)
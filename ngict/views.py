from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.decorators import login_required
from core import settings
from django.contrib.auth import authenticate, login, logout
from .models import Project, ProjectSubmission, User_Profile, Course, Module, Lesson, Assessment, Resource, Student, UserCode, Assessment, Question, Answer, AssessmentScore, UserProgress
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import UserCreationForm
from django.http import JsonResponse
import json





def view_course_assessments(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    assessments = Assessment.objects.filter(course=course)
    return render(request, 'courses/assessments/course_assessments.html', {'assessments': assessments, 'course': course})


@login_required
def view_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment)
    
    user = request.user
    assessment_score = AssessmentScore.objects.filter(user=user, assessment=assessment).first()
    
    return render(request, 'courses/assessments/view_assessment.html', {'assessment': assessment, 'questions': questions, 'score': assessment_score})


@login_required
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment)

    score = None
    user = request.user
    assessment_score = AssessmentScore.objects.filter(user=user, assessment=assessment).last()
    if assessment_score:
        score = assessment_score.score

    if request.method == 'POST':
        total_questions = questions.count()
        correct_answers = 0
        error_answers = 0
        
        for question in questions:
            user_answer_id = request.POST.get(f'question_{question.id}', None)
            if user_answer_id:
                user_answer = get_object_or_404(Answer, id=user_answer_id)
                if user_answer.is_correct:
                    correct_answers += 1
                else:
                    error_answers += 1
        
        score = (correct_answers / total_questions) * 100
        if score < 100:
            messages.error(request, 'Some of your answers are incorrect. Please review your answers.')
        else:
            messages.success(request, 'You passes the test')
        user = request.user
        
        # Save user's assessment score
        assessment_score = AssessmentScore.objects.create(user=user, assessment=assessment, score=score)
        assessment_score.save()
        
        if error_answers > 0:
            error_message = "Some of your answers are incorrect. Please review your answers."
            return render(request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'error_message': error_message})
        
        return redirect('academy:view_assessment', assessment_id=assessment.id)

    return render(request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'score':assessment_score})


@login_required
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


@login_required
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


from django.http import JsonResponse

@login_required
def projects(request):
    projects = Project.objects.all()
    submitted_project_ids = ProjectSubmission.objects.filter(user=request.user).values_list('submitted_project_id', flat=True)
    project_submissions = ProjectSubmission.objects.filter(user=request.user)

    if request.method == 'POST':
        submitted_project_id = request.POST.get('project_id')
        project_link = request.POST.get('project_link')
        submitted_project = Project.objects.get(id=submitted_project_id)

        project_submission = ProjectSubmission(user=request.user, submitted_project=submitted_project, project_link=project_link)
        project_submission.save()

        return JsonResponse({'project_title': submitted_project.project_title, 'project_link': project_link})

    return render(request, 'courses/projects/projects.html', {
        'projects': projects,
        'submitted_project_ids': submitted_project_ids,
        'project_submissions': project_submissions
    })



@login_required
def user_dashboard(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            enrolled_courses = student.enrolled_courses.all()

            progress_data = []
            for course in enrolled_courses:
                user_progress = UserProgress.objects.filter(user=request.user, course=course)
                total_weeks = course.duration_in_weeks  # Assuming the course has a duration_in_weeks field

                progress_data.append({
                    'course': course,
                    'total_weeks': total_weeks,
                    'user_progress': user_progress,
                })

            return render(request, 'user/user_dashboard.html', {'enrolled_courses': enrolled_courses, 'progress_data': progress_data})
        except Student.DoesNotExist:
            return render(request, 'user/user_dashboard.html', {'message': 'You are not enrolled in any courses yet.'})
    else:
        return render(request, 'user/user_dashboard.html', {'message': 'Please log in to access your dashboard.'})



@login_required
def html_css(request):
    course = Course.objects.get(slug='html_css')  # Get the html_css course
    assessments = Assessment.objects.filter(course=course)
    return render(request, 'courses/html_css.html', {'assessments': assessments, 'course':course})


@login_required
def python(request):
    course = Course.objects.get(slug='python')  # Get the python course
    assessments = Assessment.objects.filter(course=course)
    return render(request, 'courses/python.html', {'assessments': assessments, 'course':course})

@login_required
def javascript(request):
    course = Course.objects.get(slug='javascript')  # Get the javascript course
    assessments = Assessment.objects.filter(course=course)
    return render(request, 'courses/javascript.html', {'assessments': assessments, 'course':course})

# Similarly, define similar functions for other courses...



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
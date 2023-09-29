from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.decorators import login_required
from core import settings
from django.contrib.auth import authenticate, login, logout

from instructors.models import Answer, Assessment, Lesson, Module, Question
# from instructors.models import *
from .models import Note, Project, ProjectSubmission, User_Profile, Course, Student, UserCode, AssessmentScore, UserProgress
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import NoteForm, UserCreationForm
from django.http import JsonResponse
import json





@login_required
def html_css(request):
    course = Course.objects.get(slug='html_css')  # Get the html_css course
    assessments = Assessment.objects.filter(course=course)
    modules = Module.objects.filter(course=course)
    return render(request, 'courses/html_css.html', {'assessments': assessments, 'course':course,  'modules': modules})



@login_required
def notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('academy:notes')
    else:
        form = NoteForm()
    
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'user/notes.html', {'form': form, 'notes': notes})


def view_course_assessments(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    assessments = Assessment.objects.filter(course=course)
    return render(request, 'courses/assessments/course_assessments.html', {'assessments': assessments, 'course': course})


@login_required
def view_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = Question.objects.filter(assessment=assessment)
    
    user = request.user
    assessment_score = AssessmentScore.objects.filter(user=user, assessment=assessment).last()
    
    return render(request, 'courses/assessments/view_assessment.html', {'assessment': assessment, 'questions': questions, 'score': assessment_score})



class TakeAssessmentView:

    def __init__(self, request, assessment_id):
        self.request = request
        self.assessment_id = assessment_id


    def get_assessment(self):
        return get_object_or_404(Assessment, id=self.assessment_id)


    def get_user(self):
        return self.request.user


    def get_questions(self, assessment):
        return Question.objects.filter(assessment=assessment)


    def get_assessment_score(self, assessment):
        return AssessmentScore.objects.filter(user=self.get_user(), assessment=assessment).last()


    def calculate_score(self, questions, user_answers):
        total_questions = questions.count()
        correct_answers = 0
        for question, user_answer_id in user_answers.items():
            user_answer = get_object_or_404(Answer, id=user_answer_id)
            if user_answer.is_correct:
                correct_answers += 1
        return (correct_answers / total_questions) * 100


    def handle_post_request(self, assessment, questions):

        user_answers = {}
        for question in questions:
            user_answer_id = self.request.POST.get(f'question_{question.id}', None)
            if user_answer_id:
                user_answers[question.id] = user_answer_id


        score = self.calculate_score(questions, user_answers)
        assessment_score = AssessmentScore.objects.create(user=self.get_user(), assessment=assessment, score=score)


        if score < 100:
            messages.error(self.request, 'Some of your answers are incorrect. Please review your answers.')
            error_message = "Some of your answers are incorrect. Please review your answers."
            return render(self.request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'error_message': error_message})


        messages.success(self.request, 'You passed the test')
        assessment_score.save()
        return redirect('academy:view_assessment', assessment_id=assessment.id)


    def render_page(self, assessment, questions, assessment_score=None):
        return render(self.request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'score': assessment_score})



@login_required
def take_assessment(request, assessment_id):
    take_assessment_view = TakeAssessmentView(request, assessment_id)
    assessment = take_assessment_view.get_assessment()
    questions = take_assessment_view.get_questions(assessment)
    assessment_score = take_assessment_view.get_assessment_score(assessment)

    if request.method == 'POST':
        return take_assessment_view.handle_post_request(assessment, questions)
    
    return take_assessment_view.render_page(assessment, questions, assessment_score)



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



@login_required
def course_detail(request, slug):

    course = Course.objects.get(slug=slug)
    user = request.user

    try:
        student = Student.objects.get(user=user)
        is_enrolled = course in student.enrolled_courses.all()
    except Student.DoesNotExist:
        is_enrolled = False

    # Retrieve modules, lessons, and assessments related to the course
    modules = Module.objects.filter(course=course)
    lessons = Lesson.objects.filter(module__in=modules)
    assessments = Assessment.objects.filter(lesson__in=lessons)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'user': user,
        'modules': modules,
        'lessons': lessons,
        'assessments': assessments,
    })


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'



class EnrollCourseView:
    def __init__(self, request, slug):
        self.request = request
        self.slug = slug

    @property
    def user(self):
        return self.request.user

    def enroll_student(self):
        
        course = get_object_or_404(Course, slug=self.slug)
        student, created = Student.objects.get_or_create(user=self.user)

        if course not in student.enrolled_courses.all():
            student.enrolled_courses.add(course)
            return True
        else:
            return False

    def render_enroll_redirect(self, success):
        if success:
            return redirect('academy:course_detail', slug=self.slug)
        else:
            messages.info(self.request, 'You are already enrolled in this course.')
            return redirect('academy:course_detail', slug=self.slug)

    def render_unauthenticated_redirect(self):
        messages.error(self.request, 'Sign Up to Enroll')
        return redirect('academy:signin')


#enroll
@login_required
def enroll_course(request, slug):
    enroll_course_view = EnrollCourseView(request, slug)

    if request.user.is_authenticated:
        success = enroll_course_view.enroll_student()
        return enroll_course_view.render_enroll_redirect(success)
    else:
        return enroll_course_view.render_unauthenticated_redirect()
    


@login_required
def unenroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    student, created = Student.objects.get_or_create(user=request.user)

    if course in student.enrolled_courses.all():
        student.enrolled_courses.remove(course)
        messages.success(request, 'You have been unenrolled from the course.')
    else:
        messages.warning(request, 'You were not enrolled in this course.')

    return redirect('academy:user_dashboard')  # Redirect to the enrolled courses page



class ProjectView:
    def __init__(self, request):
        self.request = request

    @property
    def user(self):
        return self.request.user

    def get_submitted_project_ids(self):
        return ProjectSubmission.objects.filter(user=self.user).values_list('submitted_project_id', flat=True)

    def get_project_submissions(self):
        return ProjectSubmission.objects.filter(user=self.user)

    def handle_post_request(self):
        submitted_project_id = self.request.POST.get('project_id')
        project_link = self.request.POST.get('project_link')
        submitted_project = Project.objects.get(id=submitted_project_id)

        project_submission = ProjectSubmission(user=self.user, submitted_project=submitted_project, project_link=project_link)
        project_submission.save()

        return {'project_title': submitted_project.project_title, 'project_link': project_link}

    def render_page(self):
        projects = Project.objects.all()
        submitted_project_ids = self.get_submitted_project_ids()
        project_submissions = self.get_project_submissions()

        if self.request.method == 'POST':
            response_data = self.handle_post_request()
            return JsonResponse(response_data)

        return render(self.request, 'courses/projects/projects.html', {
            'projects': projects,
            'submitted_project_ids': submitted_project_ids,
            'project_submissions': project_submissions
        })

@login_required
def projects(request):
    project_view = ProjectView(request)
    return project_view.render_page()


class UserDashboardView:
    def __init__(self, request):
        self.request = request


    @property
    def user(self):
        return self.request.user


    def get_enrolled_courses(self):
        try:
            student = Student.objects.get(user=self.user)
            return student.enrolled_courses.all()
        except Student.DoesNotExist:
            return None



    def get_progress_data(self, enrolled_courses):
        progress_data = []
        for course in enrolled_courses:
            user_progress = UserProgress.objects.filter(user=self.user, course=course)
            total_weeks = course.duration_in_weeks  # Assuming the course has a duration_in_weeks field

            assessment_scores = AssessmentScore.objects.filter(user=self.user, assessment__course=course)

            progress_data.append({
                'course': course,
                'total_weeks': total_weeks,
                'user_progress': user_progress,
                'assessment_scores': assessment_scores,
            })
        return progress_data



    def render_dashboard(self, enrolled_courses, progress_data=None, message=None):
        context = {'enrolled_courses': enrolled_courses}
        if progress_data is not None:
            context['progress_data'] = progress_data
        if message is not None:
            context['message'] = message
        return render(self.request, 'user/user_dashboard.html', context)

    def render_authenticated_dashboard(self):
        enrolled_courses = self.get_enrolled_courses()
        if enrolled_courses is not None:
            progress_data = self.get_progress_data(enrolled_courses)
            return self.render_dashboard(enrolled_courses, progress_data)
        else:
            return self.render_dashboard(enrolled_courses, message='You are not enrolled in any courses yet.')

    def render_unauthenticated_dashboard(self):
        return self.render_dashboard(enrolled_courses=None, message='Please log in to access your dashboard.')


@login_required
def user_dashboard(request):
    user_dashboard_view = UserDashboardView(request)
    
    if request.user.is_authenticated:
        return user_dashboard_view.render_authenticated_dashboard()
    else:
        return user_dashboard_view.render_unauthenticated_dashboard()


class SignupView:
    def __init__(self, request):
        self.request = request

    def render_signup_page(self, form):
        return render(self.request, 'user/signup.html', {'form': form})

    def handle_post_request(self, form):
        if form.is_valid():
            user = form.save()
            if user.is_authenticated:
                login(self.request, user)

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
                logout(self.request)
                messages.info(
                    self.request,
                    "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.",
                )
            else:
                messages.success(self.request, "Your Account has been created successfully!!")

            return redirect("academy:home")

        return self.render_signup_page(form)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        signup_view = SignupView(request)
        return signup_view.handle_post_request(form)
    else:
        form = UserCreationForm()
        signup_view = SignupView(request)
        return signup_view.render_signup_page(form)


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

class UpdateProfileView:
    def __init__(self, request):
        self.request = request

    def handle_post_request(self):
        user = self.request.user  # Get the authenticated user
        
        # Extract form data from POST request
        f_name = self.request.POST.get('first_name')
        m_name = self.request.POST.get('middle_name')
        l_name = self.request.POST.get('last_name')
        gender = self.request.POST.get('gender')
        edu_qual = self.request.POST.get('educational_qualification')
        country = self.request.POST.get('country')
        street_address = self.request.POST.get('street_address')
        emp_status = self.request.POST.get('employment_status')
        phone_number = self.request.POST.get('phone_number')
        how_did_you_hear = self.request.POST.get('how_did_you_hear')
        career_path = self.request.POST.get('career_path')

        # Update user profile
        user_profile, created = User_Profile.objects.get_or_create(
            user=user,
            defaults={
                'f_name': f_name,
                'm_name': m_name,
                'l_name': l_name,
                'gender': gender,
                'edu_qual': edu_qual,
                'country': country,
                'street_address': street_address,
                'emp_status': emp_status,
                'phone_number': phone_number,
                'how_did_you_hear': how_did_you_hear,
                'career_path': career_path
            }
        )
        
        if not created:
            # If the profile already exists, update the fields
            user_profile.f_name = f_name
            user_profile.m_name = m_name
            user_profile.l_name = l_name
            user_profile.gender = gender
            user_profile.edu_qual = edu_qual
            user_profile.country = country
            user_profile.street_address = street_address
            user_profile.emp_status = emp_status
            user_profile.phone_number = phone_number
            user_profile.how_did_you_hear = how_did_you_hear
            user_profile.career_path = career_path
            user_profile.save()

            messages.success(self.request, 'User profile updated successfully')
            return redirect('academy:user_dashboard')  # Replace with the appropriate URL

        messages.success(self.request, 'User profile created successfully')
        return redirect('academy:user_dashboard')  # Replace with the appropriate URL

    def render_update_profile_page(self):
        return render(self.request, 'user/user_profile.html', context={})
        

def update_profile(request):
    update_profile_view = UpdateProfileView(request)
    
    if request.method == 'POST':
        return update_profile_view.handle_post_request()
    
    return update_profile_view.render_update_profile_page()

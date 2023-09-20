import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Answer, Course, InstructorProfile, Module, Lesson, Assessment, Question, Resource
from .forms import CourseForm, LessonForm, AssessmentForm, QuestionAnswerForm, ResourceForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
import hashlib
#------------------------------------------------------------



#========================== generate_hash ==============================
def generate_hash(identifier, object_id):
    hashed_url = generate_hash(object_id)
    return hashlib.sha256(str(identifier).encode()).hexdigest()[:10]  # Adjust the length as needed
#------------------------------------------------------------


#============================= is_staff ===========================
# Custom user test function to check if a user is staff
def is_staff(user):
    return user.is_staff
#------------------------------------------------------------


#========================== instructor_dashboard ==============================
@login_required
@user_passes_test(is_staff, login_url='academy:home')  # Redirect non-staff users to the 'home' page
def instructor_dashboard(request):
    # Fetch courses created by the instructor
    courses = Course.objects.filter(instructor=request.user)
    instructor_profile = get_object_or_404(InstructorProfile, user=request.user)
    no_courses_exist = not courses.exists()

    return render(request, 'instructors/instructor_dashboard.html', {'courses': courses, 'instructor_profile': instructor_profile, 'no_courses_exist': no_courses_exist})
#------------------------------------------------------------


#============================ create_course ============================
@login_required
def create_course(request):
    # Check if the user has an associated InstructorProfile and is a creator
    try:
        instructor_profile = InstructorProfile.objects.get(user=request.user)
    except InstructorProfile.DoesNotExist:
        messages.error(request, "You do not have permission to create courses.")
        return redirect('instructors:instructor_dashboard')  # Redirect to instructor dashboard

    if not instructor_profile.is_creator:
        messages.error(request, "You do not have permission to create courses.")
        return redirect('instructors:instructor_dashboard')  # Redirect to instructor dashboard

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructors:create_module', course_slug=course.slug)
    else:
        form = CourseForm()

    return render(request, 'instructors/create_course.html', {'form': form})
#------------------------------------------------------------


#========================== course_detail ==============================
@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = Module.objects.filter(course=course)
    return render(request, 'instructors/course_detail.html', {'course': course, 'modules': modules})
#------------------------------------------------------------


#=========================== create_modules =============================
@login_required
def create_modules(request):
    if request.method == 'POST':
        module_titles_text = request.POST.get('module_titles_textarea')
        course_id = request.POST.get('course')  # Get the selected course ID

        # Split the module titles by commas
        module_titles = [title.strip() for title in module_titles_text.split(',')]

        # Get the selected course
        selected_course = get_object_or_404(Course, pk=course_id)

        # Create and save Module instances associated with the selected course
        for title in module_titles:
            # Check if a module with the same title already exists for the course
            if not Module.objects.filter(module_title=title, course=selected_course).exists():
                module = Module(module_title=title, course=selected_course)
                module.save()

        return redirect('instructors:course_detail', slug=selected_course.slug)  # Redirect to the course detail page

    # Fetch available courses for the select dropdown
    courses = Course.objects.all()

    # If it's not a POST request, render the form
    return render(request, 'instructors/create_module.html', {'courses': courses})
#------------------------------------------------------------


#=========================== create_lesson =============================
@login_required
def create_lesson(request):
    # Fetch courses and modules and pass them as context
    courses = Course.objects.all()
    modules = Module.objects.all()

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.save()
            # You can redirect to a different page after creating the lesson if needed
            return redirect('instructors:course_detail', slug=lesson.module.course.slug)
    else:
        form = LessonForm()

    # Prepare a JSON object containing module data for AJAX
    module_data = [{'id': module.id, 'module_title': module.module_title, 'course_id': module.course_id}
                   for module in modules]

    # If the request is AJAX, return the module data as JSON
    if request.is_ajax():
        return JsonResponse({'modules': module_data})

    return render(request, 'instructors/create_lesson.html', {'form': form, 'courses': courses, 'module_data_json': json.dumps(module_data)})
#------------------------------------------------------------


#============================ save_lesson_data ============================
def save_lesson_data(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        module = request.POST.get('module')
        content = request.POST.get('content')
        
        # Save the data to the database or perform other necessary actions
        # Example:
        lesson = Lesson(course=course, module=module, content=content)
        lesson.save()
        return JsonResponse({'message': 'Form data saved successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)
#------------------------------------------------------------


#============================ load_lesson_data ============================
def load_lesson_data(request):
    # Fetch the saved data from the database or another storage
    # You may need to identify the specific data to load (e.g., based on user or session)
    # Example:
    lesson = Lesson.objects.first()  # Fetch the first lesson (you may need more complex logic)
    if lesson:
        data = {
            'course': lesson.course,
            'module': lesson.module,
            'content': lesson.content,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'No data found'}, status=404)
#------------------------------------------------------------


#============================ create_assessment ============================
@login_required
def create_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            return redirect('instructors:create_assessment')  # Redirect to the assessment detail page
    else:
        form = AssessmentForm()

    return render(request, 'instructors/create_assessment.html', {'form': form})
#------------------------------------------------------------


#============================ get_modules_and_lessons ============================
def get_modules_and_lessons(request):
    course_id = request.GET.get('course_id')
    module_id = request.GET.get('module_id')

    if course_id:
        modules = Module.objects.filter(course_id=course_id)
    else:
        modules = Module.objects.none()

    if module_id:
        lessons = Lesson.objects.filter(module_id=module_id)
    else:
        lessons = Lesson.objects.none()

    module_choices = [{'id': module.id, 'module_title': module.module_title} for module in modules]
    lesson_choices = [{'id': lesson.id, 'title': lesson.title} for lesson in lessons]

    data = {
        'modules': module_choices,
        'lessons': lesson_choices,
    }

    return JsonResponse(data)
#------------------------------------------------------------


#=========================== upload_resource =============================
@login_required
def upload_resource(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.lesson = lesson
            resource.save()
            return redirect('instructors:course_detail', slug=lesson.module.course.slug)
    else:
        form = ResourceForm()
    return render(request, 'instructors/resource_form.html', {'form': form, 'lesson': lesson})
#------------------------------------------------------------


#============================ edit_course ============================
@login_required
def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug)

    # Check if the user is the owner of the course
    if course.instructor != request.user:
        messages.error(request, "You do not have permission to edit this course.")
        return redirect('instructors:course_detail', slug=course.slug)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('instructors:course_detail', slug=course.slug)
    else:
        form = CourseForm(instance=course)

    return render(request, 'instructors/edit_course.html', {'form': form, 'course': course})
#------------------------------------------------------------


#============================ delete_course ============================
@login_required
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug)

    # Check if the user is the owner of the course
    if course.instructor != request.user:
        messages.error(request, "You do not have permission to delete this course.")
        return redirect('instructors:course_detail', slug=course.slug)

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('instructors:instructor_dashboard')

    return render(request, 'instructors/delete_course.html', {'course': course})
#------------------------------------------------------------


#============================ upload_question_answer ============================
def upload_question_answer(request):
    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)
        if form.is_valid():
            assessment = form.cleaned_data['assessment']
            question_text = form.cleaned_data['text']
            answer_text = form.cleaned_data['answer_text']
            is_correct = form.cleaned_data['is_correct']

            # Create the question
            question = Question.objects.create(text=question_text, assessment=assessment)

            # Create the answer
            answer = Answer.objects.create(text=answer_text, question=question, is_correct=is_correct)

            return redirect('upload_success')  # Redirect to a success page

    else:
        form = QuestionAnswerForm()

    return render(request, 'upload_question_answer.html', {'form': form})
#------------------------------------------------------------


#============================ get_todo_list ============================
def get_todo_list(user):
    # Get assessments not taken yet
    assessments_not_taken = Assessment.objects.filter(
        Q(course__in=user.completed_courses.all()) | 
        Q(module__in=user.completed_modules.all()) |
        Q(lesson__in=user.completed_lessons.all()),
        ~Q(assessment_scores__user=user)
    ).distinct()

    return assessments_not_taken
#------------------------------------------------------------


#=========================== todo_list_view =============================
@login_required
def todo_list_view(request):
    user = request.user
    todo_list = get_todo_list(user)
    return render(request, 'todo_list.html', {'todo_list': todo_list})
#------------------------------------------------------------


#========================== upload_question_answer==============================
@login_required
def upload_question_answer(request):
    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)
        if form.is_valid():
            assessment = form.cleaned_data['assessment']
            question_text = form.cleaned_data['text']

            # Create the question
            question = Question.objects.create(text=question_text, assessment=assessment)

            # Create the answers based on the selected correct option
            answers = []
            for i in range(1, 5):
                answer_text = form.cleaned_data[f'answer_option_{i}']
                is_correct = form.cleaned_data[f'is_correct_{i}']

                answer = Answer.objects.create(
                    text=answer_text,
                    question=question,
                    is_correct=is_correct
                )

                answers.append(answer)

            return redirect('upload_success')  # Redirect to a success page

    else:
        form = QuestionAnswerForm()

    return render(request, 'instructors/upload_question_answer.html', {'form': form})
#------------------------------------------------------------


#========================== save_question_answer_ajax==============================
@login_required
def save_question_answer_ajax(request):
    if request.method == 'POST':
        assessment_id = request.POST.get('assessment')
        question_text = request.POST.get('text')

        # Create the question
        question = Question.objects.create(text=question_text, assessment_id=assessment_id)

        # Create answers based on user input
        answers = []
        for i in range(1, 5):
            answer_text = request.POST.get(f'answer_option_{i}')
            is_correct = request.POST.get(f'is_correct_{i}') == 'true'  # Convert 'true' to boolean
            answer = Answer.objects.create(text=answer_text, question=question, is_correct=is_correct)
            answers.append(answer)

        # Return a JSON response to indicate success
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
#------------------------------------------------------------

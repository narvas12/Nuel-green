


# @login_required
# def take_assessment(request, assessment_id):
#     assessment = get_object_or_404(Assessment, id=assessment_id)
#     questions = Question.objects.filter(assessment=assessment)

#     score = None
#     user = request.user
#     assessment_score = AssessmentScore.objects.filter(user=user, assessment=assessment).last()
#     if assessment_score:
#         score = assessment_score.score

#     if request.method == 'POST':
#         total_questions = questions.count()
#         correct_answers = 0
#         error_answers = 0
        
#         for question in questions:
#             user_answer_id = request.POST.get(f'question_{question.id}', None)
#             if user_answer_id:
#                 user_answer = get_object_or_404(Answer, id=user_answer_id)
#                 if user_answer.is_correct:
#                     correct_answers += 1
#                 else:
#                     error_answers += 1
        
#         score = (correct_answers / total_questions) * 100
#         if score < 100:
#             messages.error(request, 'Some of your answers are incorrect. Please review your answers.')
#         else:
#             messages.success(request, 'You passes the test')
#         user = request.user
        
#         # Save user's assessment score
#         assessment_score = AssessmentScore.objects.create(user=user, assessment=assessment, score=score)
#         assessment_score.save()
        
#         if error_answers > 0:
#             error_message = "Some of your answers are incorrect. Please review your answers."
#             return render(request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'error_message': error_message})
        
#         return redirect('academy:view_assessment', assessment_id=assessment.id)

#     return render(request, 'courses/assessments/take_assessment.html', {'assessment': assessment, 'questions': questions, 'score':assessment_score})




# @login_required
# def enroll_course(request, slug):  # Use slug parameter
#     if request.user.is_authenticated:
#         course = get_object_or_404(Course, slug=slug)
#         student, created = Student.objects.get_or_create(user=request.user)

#         if course not in student.enrolled_courses.all():
#             student.enrolled_courses.add(course)
#             return redirect('academy:course_detail', slug=slug)
#         else:
#             messages.info(request, 'You are already enrolled in this course.')
#             return redirect('academy:course_detail', slug=slug)
#     else:
#         # Handle non-authenticated users (redirect to login or show a message)
#         messages.error(request, 'Sign Up to Enroll')
#         return redirect('academy:signin')  # Redirect to your login view


# @login_required
# def projects(request):
#     projects = Project.objects.all()
#     submitted_project_ids = ProjectSubmission.objects.filter(user=request.user).values_list('submitted_project_id', flat=True)
#     project_submissions = ProjectSubmission.objects.filter(user=request.user)

#     if request.method == 'POST':
#         submitted_project_id = request.POST.get('project_id')  # Get the submitted project ID
#         project_link = request.POST.get('project_link')
#         submitted_project = Project.objects.get(id=submitted_project_id)

#         project_submission = ProjectSubmission(user=request.user, submitted_project=submitted_project, project_link=project_link)
#         project_submission.save()

#         return JsonResponse({'project_title': submitted_project.project_title, 'project_link': project_link})

#     return render(request, 'courses/projects/projects.html', {
#         'projects': projects,
#         'submitted_project_ids': submitted_project_ids,
#         'project_submissions': project_submissions
#     })



# @login_required
# def user_dashboard(request):
#     if request.user.is_authenticated:
#         try:
#             student = Student.objects.get(user=request.user)
#             enrolled_courses = student.enrolled_courses.all()

#             progress_data = []
#             for course in enrolled_courses:
#                 user_progress = UserProgress.objects.filter(user=request.user, course=course)
#                 total_weeks = course.duration_in_weeks  # Assuming the course has a duration_in_weeks field

#                 assessment_scores = AssessmentScore.objects.filter(user=request.user, assessment__course=course)

#                 progress_data.append({
#                     'course': course,
#                     'total_weeks': total_weeks,
#                     'user_progress': user_progress,
#                     'assessment_scores': assessment_scores,
#                 })

#             return render(request, 'user/user_dashboard.html', {'enrolled_courses': enrolled_courses, 'progress_data': progress_data})
#         except Student.DoesNotExist:
#             return render(request, 'user/user_dashboard.html', {'message': 'You are not enrolled in any courses yet.'})
#     else:
#         return render(request, 'user/user_dashboard.html', {'message': 'Please log in to access your dashboard.'})



# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             if user.is_authenticated:
#                 login(request, user)
            
#             # Send welcome email
#             subject = "Welcome to Nuel-Green ICT!!"
#             message = (
#                 f"Hello {user.username}!!\n"
#                 "Welcome to Nuel-Green ICT!!\n"
#                 "Thank you for visiting our website.\n"
#                 "We have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\n"
#                 "Thanking You\nAnubhav Madhav"
#             )
#             from_email = settings.EMAIL_HOST_USER
#             to_list = [user.email]
#             send_mail(subject, message, from_email, to_list, fail_silently=True)

#             if not user.is_active:
#                 logout(request)
#                 messages.info(
#                     request,
#                     "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.",
#                 )
#             else:
#                 messages.success(request, "Your Account has been created successfully!!")

#             return redirect("academy:home")
#     else:
#         form = UserCreationForm()

#     return render(request, 'user/signup.html', {'form': form})
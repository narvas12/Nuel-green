from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
from instructors.views import instructor_dashboard

app_name = 'academy'

urlpatterns = [
   
    path('', home, name="home"),
    path('accounts/login/', register_and_login, name='register_and_login'),
    path('signout/', signout, name='signout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create_profile/', update_profile, name='update_profile'),
    
    path('instructor_dashboard/', instructor_dashboard, name='instructor_dashboard'),

    path('html_css/', html_css, name='html_css'),

    
    path('enroll/<slug:slug>/', enroll_course, name='enroll_course'),
    path('unenroll/<slug:slug>/', unenroll_course, name='unenroll_course'),

    path('course/<slug:slug>/', course_detail, name='course_detail'),


    path('save_user_codes/', save_user_codes, name='save_user_codes'),
    path('get_user_codes/', get_user_codes, name='get_user_codes'),


    path('projects/', projects, name='projects'),

    path('notes/', notes, name='make_notes'),
    path('ide/', ide, name='ide'),

    path('image-list/', image_list, name='image_list'),
    path('image/<int:image_id>/', view_image, name='view_image'),

    path('get-course-progress/<int:course_id>/', get_course_progress, name='get_course_progress'),

    # URL pattern for marking a lesson as completed
    path('mark-lesson-completed/', mark_lesson_completed, name='mark_lesson_completed'),
    path('connected_visitors/', connected_visitors, name='connected_visitors'),

] 

urlpatterns += staticfiles_urlpatterns()
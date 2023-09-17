from django.urls import path
from .views import *
from ngict.views import home

app_name = 'instructors'

urlpatterns = [
    path('', home, name="home"),
    path('instructor_dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('create_course/', create_course, name='create_course'),
    path('course/<slug:slug>/', course_detail, name='course_detail'),
    path('create_module/', create_modules, name='create_module'),
    path('create_lesson/', create_lesson, name='create_lesson'),

    path('lesson/<int:lesson_id>/create_assessment/', create_assessment, name='create_assessment'),
    path('lesson/<int:lesson_id>/upload_resource/', upload_resource, name='upload_resource'),
    # Add more URL patterns as needed

    path('edit_course/<slug:slug>/', edit_course, name='edit_course'),
    path('delete_course/<slug:slug>/', delete_course, name='delete_course'),

    path('save_lesson_data/', save_lesson_data, name='save_lesson_data'),
    path('load_lesson_data/', load_lesson_data, name='load_lesson_data'),
]

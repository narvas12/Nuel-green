from django.urls import path
from instructors.views import *
from ngict.views import home
from django.conf import settings
from django.conf.urls.static import static



app_name = 'instructors'

urlpatterns = [
    path('', home, name="home"),
    path('instructor_dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('create_course/', create_course, name='create_course'),
    path('course/<slug:slug>/', course_detail, name='course_detail'),
    path('create_module/', create_modules, name='create_module'),
    path('create_lesson/', create_lesson, name='create_lesson'),
    path('lesson/<int:lesson_id>/upload_resource/', upload_resource, name='upload_resource'),

    path('lesson/<int:lesson_id>/create_assessment/', create_assessment, name='create_assessment'),
    path('create_assessment/', create_assessment, name='create_assessment'),

    path('get_modules_and_lessons/', get_modules_and_lessons, name='get_modules_and_lessons'),

    path('edit_course/<slug:slug>/', edit_course, name='edit_course'),
    path('delete_course/<slug:slug>/', delete_course, name='delete_course'),

    path('save_lesson_data/', save_lesson_data, name='save_lesson_data'),
    path('load_lesson_data/', load_lesson_data, name='load_lesson_data'),

    path('upload_question_answer/', upload_question_answer, name='upload_question_answer'),

    path('save_question_answer_ajax/', save_question_answer_ajax, name='save_question_answer_ajax'),


    path('assessment-list/', assessment_list, name='assessment_list'),
    path('take_assessment/<int:assessment_id>/', take_assessment, name='take_assessment'),
    path('courses/', courses_by_category, name='courses_by_category'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

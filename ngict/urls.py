from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
from instructors.views import instructor_dashboard

app_name = 'academy'

urlpatterns = [
   
    path('', home, name="home"),
    path('accounts/login/', register_and_login, name='register_and_login'),
    # path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create_profile/', update_profile, name='update_profile'),
    
    path('instructor_dashboard/', instructor_dashboard, name='instructor_dashboard'),

    path('html_css/', html_css, name='html_css'),



    path('course_list/', CourseListView.as_view(), name='course_list'),
    
    path('enroll/<slug:slug>/', enroll_course, name='enroll_course'),
    path('unenroll/<slug:slug>/', unenroll_course, name='unenroll_course'),

    path('course/<slug:slug>/', course_detail, name='course_detail'),


    path('save_user_codes/', save_user_codes, name='save_user_codes'),
    path('get_user_codes/', get_user_codes, name='get_user_codes'),


    path('projects/', projects, name='projects'),

    path('notes/', notes, name='notes'),

    path('image-list/', image_list, name='image_list'),
    path('image/<int:image_id>/', view_image, name='view_image'),
]

urlpatterns += staticfiles_urlpatterns()
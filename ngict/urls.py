from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

app_name = 'academy'

urlpatterns = [
   
    path('', home, name="home"),
    # path('htm_lcss/', html_css, name="html_css"),
    path('accounts/login/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create_profile/', update_profile, name='update_profile'),
    

    path('html_css/', html_css, name='html_css'),


    path('course_list/', CourseListView.as_view(), name='course_list'),
    path('enroll/<slug:slug>/', enroll_course, name='enroll_course'),
    path('course/<slug:slug>/', course_detail, name='course_detail'),

    
    path('enroll/<slug:slug>/', enroll_course, name='enroll_course'),

    path('save_user_codes/', save_user_codes, name='save_user_codes'),
    path('get_user_codes/', get_user_codes, name='get_user_codes'),

    # path('course/<slug:course_slug>/assessments/', view_course_assessments, name='view_course_assessments'),
    path('course/<slug:course_slug>/', view_course_assessments, name='view_course_assessments'),
    path('assessment/<int:assessment_id>/', view_assessment, name='view_assessment'),
    path('assessment/<int:assessment_id>/take/', take_assessment, name='take_assessment'),
    path('projects/', projects, name='projects'),

    path('notes/', notes, name='notes'),
]

urlpatterns += staticfiles_urlpatterns()
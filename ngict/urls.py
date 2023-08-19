from django.urls import path
from .views import *

app_name = 'academy'

urlpatterns = [
   
    path('', home, name="home"),
    path('htm_lcss/', html_css, name="html_css"),
    path('accounts/login/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create_profile/', create_profile, name='create_profile'),

    
    path('course_list', CourseListView.as_view(), name='course_list'),
    # path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<slug:slug>/', course_detail, name='course_detail'),
    path('nodejs/', nodejs, name='nodejs'),
    path('enroll/<slug:slug>/', enroll_course, name='enroll_course'),


    path('save_user_codes/', save_user_codes, name='save_user_codes'),
    path('get_user_codes/', get_user_codes, name='get_user_codes')
]
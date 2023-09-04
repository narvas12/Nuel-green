from django.db import models
from core import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from instructors.models import Course, AssessmentScore, Project



class UserCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    html_code = models.TextField()
    css_code = models.TextField()
    js_code = models.TextField()

    # Add any other fields as needed

    def __str__(self):
        return f"UserCode for {self.user}"



class User_Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    edu_qual = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    emp_status = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    how_did_you_hear = models.CharField(max_length=100)
    career_path = models.CharField(max_length=100, default='Software development')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username  # Return the username instead of email



class ProjectSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project_link = models.URLField()
    submitted_project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = ['user', 'submitted_project'] 


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    enrolled_courses = models.ManyToManyField(Course)

    assessment_scores = models.ManyToManyField(AssessmentScore, related_name='students', blank=True)


class UserProgress(models.Model):
    STATUS_NOT_STARTED = 'Not Started'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_COMPLETED = 'Completed'

    STATUS_CHOICES = (
        (STATUS_NOT_STARTED, 'Not Started'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)

    def __str__(self):
        return f"{self.user.username} - {self.course.course_title} - Week {self.week} - Status: {self.get_status_display()}"
    

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField( null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username}"
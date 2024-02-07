from django.db import models
from core import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from instructors.models import Assessment, Course, AssessmentScore, Lesson, Module, Project
from uuid import uuid4
import os


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    browser = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    time_spent = models.FloatField()  # in seconds
    timestamp = models.DateTimeField(auto_now_add=True)
    is_connected = models.BooleanField(default=False)  # Add is_connected field

    def __str__(self):
        return f"{self.ip_address} - {self.browser} - {self.os} - {self.device} - {self.is_connected}"



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

    

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField( null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username}"




def generate_upload_path(instance, filename):
    """
    Generate a unique upload path for each image.
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a unique filename
    unique_filename = f"{uuid4().hex}.{ext}"
    # Generate a folder structure based on the current date (optional)
    folder = instance.uploaded_at.strftime("%Y/%m/%d")
    # Combine the folder and filename to create the upload path
    return os.path.join('uploads', folder, unique_filename)

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=generate_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)
    updated_at =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = os.path.splitext(self.image.name)[0]  # Use the filename as the title
        super().save(*args, **kwargs)



class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    assessments_completed = models.ManyToManyField(Assessment, blank=True)

    class Meta:
        unique_together = ('user', 'course', 'module', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.course.course_title} - {self.module.module_title if self.module else ''} - {self.lesson.title if self.lesson else ''}"



class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Assuming you have a Lesson model
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'lesson')
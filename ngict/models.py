from django.db import models
from core import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class UserCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
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



class Instructor(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    contact_info = models.CharField(max_length=200)


class Course(models.Model):
    course_title = models.CharField(max_length=100)
    video_url = models.URLField(null=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    duration_in_days = models.IntegerField(default=100)
    
    @property
    def duration_in_weeks(self):
        return self.duration_in_days // 7

    class Meta:
        verbose_name_plural = 'Course'
        ordering = ('-course_title',)

    def get_absolute_url (self):
        return reverse('academy:course', args=[self.slug])

    def __str__(self):
        return self.course_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_title)
        super().save(*args, **kwargs)


class Module(models.Model):
    module_title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    order = models.PositiveIntegerField()


    def __str__(self):
        return self.module_title


class Lesson(models.Model):
    course = models.ForeignKey(Course, default=None, null=True, on_delete=models.DO_NOTHING)
    module = models.ForeignKey(Module, default=None, null=True, on_delete=models.DO_NOTHING)
    lesson_title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    order = models.PositiveIntegerField() 

    def __str__(self):
        return self.lesson_title


# assessments section 
class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, default=None, null=True, on_delete=models.DO_NOTHING)
    module = models.ForeignKey(Module, default=None, null=True, on_delete=models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, default=None, null=True, on_delete=models.DO_NOTHING)
    passing_score = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class Question(models.Model):
    text = models.TextField()
    assessment = models.ForeignKey('Assessment', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey('Question', on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField(default=False)


class AssessmentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    assessment = models.ForeignKey(Assessment, on_delete=models.DO_NOTHING)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Store the score as a decimal

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}"


class Resource(models.Model):
    resource_title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')  # Store files like videos, slides, etc.
    lesson = models.ForeignKey('Lesson', on_delete=models.DO_NOTHING)


class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField(max_length=200)
    # Other fields for Project

    class Meta:
        unique_together = ['course', 'project_title']  # Enforce uniqueness per course
    
    def __str__(self):
        return self.project_title


class ProjectSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project_link = models.URLField()
    submitted_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['user', 'submitted_project'] 


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    enrolled_courses = models.ManyToManyField('Course')

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
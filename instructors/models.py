from datetime import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    biography = models.TextField()
    contact_info = models.CharField(max_length=200)
    is_creator = models.BooleanField(default=False)  # Indicates if the instructor can create courses

    def __str__(self):
        return self.user.username


    
class Course(models.Model):
    course_title = models.CharField(max_length=100)
    video_url = models.URLField(null=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    duration_in_days = models.IntegerField(default=100)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)  # Add this line to associate a course with an instructor
    
    
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
    id = models.AutoField(primary_key=True)
    module_title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)


    def __str__(self):
        return self.module_title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, default=None, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = RichTextField(null=True)
    created_at = models.DateTimeField(null=True)  # Make it nullable

    def __str__(self):
        return f"Lesson Created by {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)



# assessments section 
class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, default=None, null=True, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, default=None, null=True, on_delete=models.PROTECT)
    lesson = models.ForeignKey(Lesson, default=None, null=True, on_delete=models.PROTECT)
    passing_score = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class Question(models.Model):
    text = models.TextField()
    assessment = models.ForeignKey('Assessment', on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    is_correct = models.BooleanField(default=False)


class AssessmentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    assessment = models.ForeignKey(Assessment, on_delete=models.PROTECT)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Store the score as a decimal

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}"


class Resource(models.Model):
    resource_title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')  # Store files like videos, slides, etc.
    lesson = models.ForeignKey('Lesson', on_delete=models.PROTECT)


class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField(max_length=10000)
    # Other fields for Project

    class Meta:
        unique_together = ['course', 'project_title']  # Enforce uniqueness per course
    
    def __str__(self):
        return self.project_title
from django.db import models
from core import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify




class UserCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    html_code = models.TextField()
    css_code = models.TextField()
    js_code = models.TextField()

    # Add any other fields as needed

    def __str__(self):
        return f"UserCode for {self.user}"



class User_Profile(models.Model):
    username = models.ForeignKey(User, max_length=20, on_delete=models.PROTECT)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    edu_qual = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email should be unique
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    emp_status = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    how_did_you_hear = models.CharField(max_length=100)
    career_path = models.CharField(max_length=100, default='Software development')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Add additional fields as per your requirement

    def __str__(self):
        return self.email


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    contact_info = models.CharField(max_length=200)


class Course(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField(null=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Course'
        ordering = ('-title',)

    def get_absolute_url (self):
        return reverse('academy:course', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    order = models.PositiveIntegerField()


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # This could hold text, video links, code snippets, etc.
    module = models.ForeignKey('Module', on_delete=models.PROTECT)
    order = models.PositiveIntegerField()



# assessments section 
class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.PROTECT)
    passing_score = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class Question(models.Model):
    text = models.TextField()
    assessment = models.ForeignKey('Assessment', on_delete=models.PROTECT)


class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    is_correct = models.BooleanField(default=False)


class AssessmentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Store the score as a decimal

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}"


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')  # Store files like videos, slides, etc.
    lesson = models.ForeignKey('Lesson', on_delete=models.PROTECT)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    enrolled_courses = models.ManyToManyField('Course')

    assessment_scores = models.ManyToManyField(AssessmentScore, related_name='students', blank=True)







# admin.py
from django.contrib import admin

from .models import Instructor, Course, Module, Lesson, Student, Assessment, Resource, UserCode, Question, Answer, AssessmentScore

@admin.register(AssessmentScore)
class AssessmentScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'score')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'assessment')  # Use select_related for optimization
        return queryset

@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'html_code', 'css_code', 'js_code']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_enrolled_courses', 'display_assessment_scores')

    def display_enrolled_courses(self, obj):
        return ", ".join([course.title for course in obj.enrolled_courses.all()])
    display_enrolled_courses.short_description = 'Enrolled Courses'

    def display_assessment_scores(self, obj):
        return ", ".join([str(score.score) for score in obj.assessment_scores.all()])
    display_assessment_scores.short_description = 'Assessment Scores'


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','description', 'course', 'passing_score')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Number of answer options to show for each question


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
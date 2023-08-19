# admin.py
from django.contrib import admin

from .models import Instructor, Course, Module, Lesson, Student, Assessment, Resource, UserCode

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
    list_display = ('user', 'display_enrolled_courses')

    def display_enrolled_courses(self, obj):
        return ", ".join([course.title for course in obj.enrolled_courses.all()])

    display_enrolled_courses.short_description = 'Enrolled Courses'


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_score')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
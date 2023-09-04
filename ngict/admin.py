# admin.py
from django.contrib import admin

from .models import Note, ProjectSubmission, Student, User_Profile, UserCode, AssessmentScore, Project


@admin.register(User_Profile)
class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'f_name', 'l_name', 'email', 'career_path', 'date_joined']
    list_filter = ['career_path', 'is_active', 'is_staff']
    search_fields = ['user__username', 'email']
    readonly_fields = ['date_joined']

    fieldsets = [
        ('User Information', {'fields': ['user', 'f_name', 'm_name', 'l_name', 'gender']}),
        ('Contact Information', {'fields': ['email', 'phone_number', 'country', 'street_address']}),
        ('Employment', {'fields': ['emp_status', 'career_path', 'how_did_you_hear']}),
        ('Permissions', {'fields': ['is_active', 'is_staff']}),
        ('Dates', {'fields': ['date_joined'], 'classes': ['collapse']}),
    ]

@admin.register(ProjectSubmission)
class SubmitPojectAdmin(admin.ModelAdmin):
    list_display = ['user', 'project_link', 'submitted_project']

class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(Note, NoteAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['course', 'project_title', 'project_description']


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



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_enrolled_courses', 'display_assessment_scores')

    def display_enrolled_courses(self, obj):
        return ", ".join([course.course_title for course in obj.enrolled_courses.all()])
    display_enrolled_courses.short_description = 'Enrolled Courses'

    def display_assessment_scores(self, obj):
        return ", ".join([str(score.score) for score in obj.assessment_scores.all()])
    display_assessment_scores.short_description = 'Assessment Scores'



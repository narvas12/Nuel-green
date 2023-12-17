# admin.py
from django.contrib import admin

from .models import Image, LessonCompletion, Note, ProjectSubmission, Student, User_Profile, UserCode, AssessmentScore, Project, UserProgress, Visitor


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'uploaded_at')



@admin.register(Visitor)
class VisitorsAdmin(admin.ModelAdmin):
        list_display = ('ip_address', 'browser', 'device')



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


admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'module', 'lesson', 'completed', 'timestamp', 'completed_assessments')
    list_filter = ('user', 'course', 'completed')
    search_fields = ('user__username', 'course__course_title', 'module__module_title', 'lesson__title')
    list_per_page = 20  # Number of items displayed per page

    def completed_assessments(self, obj):
        # Display a comma-separated list of completed assessments
        return ", ".join([assessment.title for assessment in obj.assessments_completed.all()])
    
    completed_assessments.short_description = 'Completed Assessments'


    
@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_lesson_title', 'completed_at')  # Add 'get_lesson_title' to list_display
    list_filter = ('user', 'completed_at')
    search_fields = ('user__username',)

    def get_lesson_title(self, obj):
        return obj.lesson.title if obj.lesson else ''  # Fetch the lesson title or return an empty string if it's None
    get_lesson_title.short_description = 'Completed Lesson Title'  # Set a custom column header

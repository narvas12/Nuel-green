from django.contrib import admin

from instructors.models import Answer, Assessment, Course, CourseCategories, InstructorProfile, Lesson, Module, Question, Resource

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'category', 'description')
    prepopulated_fields = {'slug': ('course_title',)}
    list_filter = ('category',)  # Add this line to enable filtering by category



@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_title', 'course')
    list_filter = ('course',)  # Add this line to enable filtering by course



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module', 'user', 'content', 'created_at')
    list_filter = ('course', 'module')  # Add this line to enable filtering by course and module



@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'course', 'module', 'lesson', 'passing_score')
    list_filter = ('course', 'module', 'lesson')  # Add this line to enable filtering by course, module, and lesson



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Number of answer options to show for each question


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'assessment']
    list_filter = ('assessment',) 

admin.site.register(Question, QuestionAdmin)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_title', 'lesson')
    list_filter = ('lesson',)  # Add this line to enable filtering by lesson




class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'biography', 'contact_info', 'is_creator')
    list_filter = ('is_creator',)

# Register the InstructorProfile model with its admin class
admin.site.register(InstructorProfile, InstructorProfileAdmin)

@admin.register(CourseCategories)
class CourseCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate the slug from the title
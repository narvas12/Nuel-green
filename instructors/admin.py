from django.contrib import admin

from instructors.models import Answer, Assessment, Course, InstructorProfile, Lesson, Module, Question, Resource

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'description')
    prepopulated_fields = {'slug': ('course_title',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_title', 'course', 'order')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_title','description', 'module', 'order')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','description', 'course','module', 'lesson', 'passing_score')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Number of answer options to show for each question


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'assessment']

admin.site.register(Question, QuestionAdmin)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_title', 'lesson')



class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'biography', 'contact_info', 'is_creator')
    list_filter = ('is_creator',)

# Register the InstructorProfile model with its admin class
admin.site.register(InstructorProfile, InstructorProfileAdmin)

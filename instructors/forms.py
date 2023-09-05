from django import forms
from .models import Course, Module, Lesson, Assessment, Resource

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_title', 'video_url', 'description', 'duration_in_days']


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'course', 'module', 'lesson', 'passing_score']
        # ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the 'lesson' and 'course' fields to be select inputs
        self.fields['module'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['lesson'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['course'].widget = forms.Select(attrs={'class': 'form-control'})


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resource_title', 'description', 'file']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['module_title', 'course']
        # ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the 'course' field to be a select input
        self.fields['course'].widget = forms.Select(attrs={'class': 'form-control'})



class LessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select a course")
    module = forms.ModelChoiceField(queryset=Module.objects.all(), empty_label="Select a module")

    class Meta:
        model = Lesson
        fields = ('course', 'module', 'content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the 'module' field to be a select input
        self.fields['module'].widget = forms.Select(attrs={'class': 'form-control'})


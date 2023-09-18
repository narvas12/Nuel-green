from django import forms
from .models import Answer, Course, Module, Lesson, Assessment, Question, Resource

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_title', 'video_url', 'description', 'duration_in_days']




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
        fields = ('id', 'title', 'course', 'module', 'content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the 'module' field to be a select input
        self.fields['module'].widget = forms.Select(attrs={'class': 'form-control'})




class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'course', 'module', 'lesson', 'passing_score']

    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select a course")
    module = forms.ModelChoiceField(queryset=Module.objects.none(), empty_label="Select a module")
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.none(), empty_label="Select a lesson")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate choices for course
        self.fields['course'].queryset = Course.objects.all()

        # Initially, set empty choices for module and lesson
        self.fields['module'].choices = [('', 'Select a module')]
        self.fields['lesson'].choices = [('', 'Select a lesson')]

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                # Get modules related to the selected course
                self.fields['module'].queryset = Module.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass  # Handle invalid course ID gracefully

        if 'module' in self.data:
            try:
                module_id = int(self.data.get('module'))
                # Get lessons related to the selected module
                self.fields['lesson'].queryset = Lesson.objects.filter(module_id=module_id)
            except (ValueError, TypeError):
                pass  # Handle invalid module ID gracefully





class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    # Add a field to select the assessment
    assessment = forms.ModelChoiceField(
        queryset=Assessment.objects.all(),
        empty_label="Select an assessment"
    )

    # Add a field to enter the answer text
    answer_text = forms.CharField(
        label="Answer Text",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    # Add a field to specify if the answer is correct
    is_correct = forms.BooleanField(
        required=False,  # Allows for multiple answers, some of which may be correct
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

class Meta:
    model = Answer
    fields = ['text', 'is_correct']
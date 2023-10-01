from django import forms
from .models import Answer, Course, Module, Lesson, Assessment, Question, Resource
from django.forms.widgets import Textarea

class AutoResizeTextarea(Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'auto-resize-textarea', **(attrs or {})})



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        Course.description = forms.CharField(widget=AutoResizeTextarea(attrs={'rows': 1}))

        fields = ['course_title', 'image',  'video_url', 'description', 'duration_in_days']



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


#upload questions and answer form
class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    # Add a field to select the assessment
    assessment = forms.ModelChoiceField(
        queryset=Assessment.objects.all(),
        empty_label="Select an assessment"
    )

    # Add fields for answer options
    answer_option_1 = forms.CharField(
        label="Answer Option 1",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    answer_option_2 = forms.CharField(
        label="Answer Option 2",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    answer_option_3 = forms.CharField(
        label="Answer Option 3",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    answer_option_4 = forms.CharField(
        label="Answer Option 4",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    # Add fields to specify if the answer is correct
    is_correct_1 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    is_correct_2 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    is_correct_3 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    is_correct_4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


# tae assessents form 

class AssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assessment = kwargs.pop('assessment')
        super(AssessmentForm, self).__init__(*args, **kwargs)

        for question in Question.objects.filter(assessment=assessment):
            choices = [(answer.id, answer.text) for answer in question.answer_set.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                choices=choices,
                required=True,
            )
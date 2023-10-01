from django import template
from instructors.models import Module, Lesson, Assessment, Question  # Import your relevant models here

register = template.Library()

@register.filter
def organize_assessments_by_lesson(course):
    modules = Module.objects.filter(course=course)
    lessons = Lesson.objects.filter(module__in=modules)
    
    data = []
    for lesson in lessons:
        assessments = Assessment.objects.filter(lesson=lesson)
        assessment_data = []
        
        for assessment in assessments:
            questions = Question.objects.filter(assessment=assessment)
            assessment_data.append({'assessment': assessment, 'questions': questions})
        
        data.append({'lesson': lesson, 'assessments': assessment_data})
    
    return data

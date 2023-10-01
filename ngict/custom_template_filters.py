from django import template

register = template.Library()

@register.filter
def get_question_answer_id(post_data, question_id):
    return post_data.get(f'question_{question_id}')

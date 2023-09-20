from django.db import models

    


class SurveyResponse(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    
    # Problem-Solving
    problem_solving_approach = models.CharField(max_length=100)

    # Work Preferences
    work_independence = models.CharField(max_length=100)
    # Technical Problem-Solving Skills
    technical_problem_solving = models.PositiveIntegerField(
        help_text="Rate your technical problem-solving skills (1 = Low, 5 = High)"
    )

    # Technical Skills
    technical_skills = models.PositiveIntegerField(
        help_text="Rate your overall technical skills (1 = Low, 5 = High)"
    )

    # Problem-Solving Approach
    systematic_approach = models.PositiveIntegerField(
        help_text="Rate your ability to systematically approach technical problems (1 = Low, 5 = High)"
    )
    creative_approach = models.PositiveIntegerField(
        help_text="Rate your ability to come up with creative solutions to technical problems (1 = Low, 5 = High)"
    )
    analytical_approach = models.PositiveIntegerField(
        help_text="Rate your ability to use analytical methods for technical problem-solving (1 = Low, 5 = High)"
    )
    collaborative_approach = models.PositiveIntegerField(
        help_text="Rate your ability to collaborate with others on technical problem-solving (1 = Low, 5 = High)"
    )

    # Personality Traits
    detail_oriented = models.PositiveIntegerField()
    enjoy_working_with_others = models.PositiveIntegerField()
    adaptable_and_learning = models.PositiveIntegerField()
    comfortable_with_ambiguity = models.PositiveIntegerField()
    enjoys_leadership_roles = models.PositiveIntegerField()
    highly_organized = models.PositiveIntegerField()
    analytical_thinking = models.PositiveIntegerField()
    creativity = models.PositiveIntegerField()
    patience = models.PositiveIntegerField()
    assertiveness = models.PositiveIntegerField()
    empathy = models.PositiveIntegerField()
    resilience = models.PositiveIntegerField()

    # Technical Thinking Traits
    problem_analysis = models.PositiveIntegerField()
    algorithmic_thinking = models.PositiveIntegerField()
    system_design = models.PositiveIntegerField()
    debugging_skills = models.PositiveIntegerField()
    troubleshooting = models.PositiveIntegerField()
    critical_thinking = models.PositiveIntegerField()

    # Analytical Thinking Traits
    data_analysis_skills = models.PositiveIntegerField()
    pattern_recognition = models.PositiveIntegerField()
    attention_to_detail = models.PositiveIntegerField()
    logical_reasoning = models.PositiveIntegerField()
    data_interpretation = models.PositiveIntegerField()
    hypothesis_testing = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# from .models import Result, GradingStructure

# def total_score(student, period):
#     """
#     Returns the total score of a student in a given academic period.
#     """
#     results = Result.objects.filter(student=student, academic_period=period)
#     return sum(r.score for r in results)


# def compute_division(student, period):
#     """
#     Computes the division based on the student's total score and the grading rules.
#     """
#     total = total_score(student, period)  # get total score first

#     # Get grading structures (ordered by highest min_score)
#     grading_rules = GradingStructure.objects.all().order_by('-min_score')

#     # Determine division
#     for rule in grading_rules:
#         if total >= rule.min_score:
#             return rule.division

#     return "Ungraded"

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth


from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.admin.views.decorators import staff_member_required

# from django.http import HttpResponse
# from django.views.generic import View

# from django.template.loader import get_template
# from .utils import render_to_pdf #created in step 4


from .models import *
from .homepage_selector import(get_all_about_us, get_about_us, get_schedules,get_schedule, get_our_partners,get_our_partner)
from .schools_selector import(get_schools,get_school)
from .student_selector import(get_students, get_student)
from .passslip_selector import(get_students,get_student, get_student_in_students, get_results,get_result, get_subjects,get_subject)

from .form import(ContactForm)

from .filters import(School_filter, Student_filter)

# creating lab report using canvas

import io
from django.http import FileResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4




# Create your views here.

# HOME PAGE
def manage_iple(request):
    get_all_aboutus = get_all_about_us()
    get_single_schedules = get_schedules()
    get_sch_list = get_schools()
    get_all_partners = get_our_partners()
    total_num_students = Student.objects.count()
    total_num_schools = School.objects.count()
    first_grades = Student.objects.filter(division=1).count()

    context={
        "get_single_schedules":get_single_schedules,
        "get_sch_list":get_sch_list,
        "get_all_partners":get_all_partners,
        "get_all_aboutus":get_all_aboutus,
        "total_num_students":total_num_students,
        "total_num_schools":total_num_schools,
        "first_grades":first_grades,
    }
    return render(request, 'resultsapp/index.html', context)


# REGISTRATION

def manage_registration(request):
    
    context={
        
    }
    return render(request, 'resultsapp/registration.html', context)

# SCHOOLS
def manage_schools(request):

    get_all_schools = get_schools()

    get_all_schools_filter = School_filter(request.GET, queryset=get_all_schools)
    
    context={
        "get_all_schools_filter":get_all_schools_filter,
        
    }
    return render(request, 'resultsapp/schools.html', context)

# SCHOOL
def manage_single_school(request, school_id):

    get_single_school = get_school(school_id)    

    context={
        "get_single_school":get_single_school,
        
    }
    return render(request, 'resultsapp/school.html', context)

# STUDENTS PAGE
def manage_student_in_students(request):

    get_all_students = get_students()

    get_all_students_filter = Student_filter(request.GET, queryset=get_all_students)
    
    context={
        "get_all_students_filter":get_all_students_filter,
        
    }
    return render(request, 'resultsapp/students.html', context)
   
   # ABOUT US

def manage_about_us(request):

    get_all_aboutus = get_all_about_us()
    context={
        "get_all_aboutus":get_all_aboutus,
    }
    return render(request, 'resultsapp/about_us.html', context)

# contact_us form

def Manage_contact_us(request):
    massege_form = ContactForm()
    if request.method=="POST":
        massege_form = ContactForm(request.POST, request.FILES)
        if massege_form.is_valid():
            massege_form.save()
            user=massege_form.cleaned_data.get('user_name')
            messages.success(request, 'Thanks alot, your message is successfully sent!')
            return redirect("iple")
        else:
            messages.warning(request, 'Operation Not Successfull')
            return redirect("iple")

    context={
        "massege_form":massege_form
    }
    return render(request, "index.html",context)  

# # PASSSLIP PAGE
# class manage_passslip(View):
#     def get(self, request, school_id, *args, **kwargs):
#         template = get_template('resultsapp/pass_slip_school.html')
#         get_single_school = get_school(school_id)
#         context = {
#             "get_single_school": get_single_school,
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('resultsapp/pass_slip_school.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Results_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")



# generate STUDENT pdf file Function
# def generate_pdf_report(request, student_id):
#     # 1. Fetch data from the database
#     try:
#         report_data = Student.objects.get(id=student_id)
#     except Student.DoesNotExist:
#         # Handle the case where the report is not found
#         return HttpResponse("Student not found", status=404)
    
#     # 2. Create a file-like buffer to receive PDF data
#     buffer = io.BytesIO()

#     # 3. Create the PDF object, using the buffer as its "file"
#     p = canvas.Canvas(buffer, pagesize=A4)

#     # 4. Draw things on the PDF using the fetched data
#     p.drawString(100, 800, f"Student Index Number: {report_data.index_number}")
#     p.drawString(100, 780, f"Student Name: {report_data.full_name}")
#     p.drawString(100, 760, f"Student Gender: {report_data.gender}")

#     # 5. Close the PDF object cleanly
#     p.showPage()
#     p.save()

#     # 6. Get the value of the BytesIO buffer and create a FileResponse object
#     buffer.seek(0)
#     # The 'as_attachment=True' will prompt a download dialog
#     return FileResponse(buffer, as_attachment=True, filename=f"lab_report_{student_id}.pdf")



# Student

@staff_member_required(login_url='iple')
def manage_single_student(request, student_id,):

    get_single_school = get_student(student_id)    

    context={
        "get_single_school":get_single_school,
        
    }
    return render(request, 'resultsapp/pass_slip.html', context)



# Single School Student

@staff_member_required(login_url='iple')
def manage_single_school_student(request, student_id,):

    get_single_school = get_student(student_id)    

    context={
        "get_single_school":get_single_school,
        
    }
    return render(request, 'resultsapp/pass_slip_school.html', context)


# creating view for lab report using canvas

def some_pdf_view(request):

    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition'] = 'attachment; filename="hello.pdf"'

    c = canvas.Canvas(response) 
    # title
    
    c.setFont("Helvetica", 24)
    c.drawString(100, 800, "Hello world How are you doing.")
    # Timestamp
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Generated on:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Example text
    c.setFont("Helvetica", 24)
    c.drawString(100, 750, "This is second trial for many words.")

    # 5. Close the PDF object cleanly
    c.showPage()
    c.save()

    return response

# creating view for lab report Method 2 Final

def generate_passslip_pdf(request, student_id):

    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition'] = 'attachment; filename="student_passslip.pdf"'
    # 1. Fetch data from the database
    try:
        report_data = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        # Handle the case where the report is not found
        return HttpResponse("Student not found", status=404)
    
    # 3. Create the PDF object,
    c = canvas.Canvas(response) 

    # 4. Draw things on the PDF using the fetched data
    # title
    c.setFont("Helvetica", 24)
    c.drawString(100, 800, f"Student Index Number: {report_data.index_number}")
    c.drawString(100, 400, f"Student Name: {report_data.full_name}")
    c.drawString(100, 300, f"Student Gender: {report_data.gender}")
    
    # Timestamp
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Generated on:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()

    # The 'as_attachment=True' will prompt a download dialog
    return response
    

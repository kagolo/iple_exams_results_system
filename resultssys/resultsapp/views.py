from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

from .models import *
from .homepage_selector import(get_all_about_us, get_about_us, get_schedules,get_schedule, get_our_partners,get_our_partner)
from .schools_selector import(get_schools,get_school)


# Create your views here.

# HOME PAGE
def manage_iple(request):
    get_all_aboutus = get_all_about_us()
    get_single_schedules = get_schedules()
    get_sch_list = get_schools()
    get_all_partners = get_our_partners()

    context={
        "get_single_schedules":get_single_schedules,
        "get_sch_list":get_sch_list,
        "get_all_partners":get_all_partners,
        "get_all_aboutus":get_all_aboutus,
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
   

# Register your models here.
# admin.py
from django.contrib import admin
from .models import (
    Student, Result, Subject, AcademicPeriod,
    School, GradingStructure, SchoolAdministrator,Schedule,Carousel,Contact_us,Our_partners,About_us
)
from django.http import HttpResponse
from django.template.loader import render_to_string


# -------------------------
# Inline Result for Students
# -------------------------
class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    readonly_fields = ('subject', 'score', 'get_grade', 'get_remark', 'total_score', 'division')
    fields = ('subject', 'score', 'get_grade', 'get_remark', 'total_score', 'division')
    can_delete = False
    show_change_link = True

    def total_score(self, obj):
        return obj.total_score
    total_score.short_description = "Total Score"

    def division(self, obj):
        return obj.division
    division.short_description = "Division"

    def get_grade(self, obj):
        return obj.get_grade()
    get_grade.short_description = "Grade"

    def get_remark(self, obj):
        return obj.get_remark()
    get_remark.short_description = "Remark"

# -------------------------
# School Admin
# -------------------------
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "district","police_station","head_teacher_name","dos_theology_name","contact","school_logo")
    search_fields = ("name", "code", "location")
    list_filter = ("district", "police_station")

# -------------------------
# School Administrator
# -------------------------
@admin.register(SchoolAdministrator)
class SchoolAdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
    search_fields = ('user__username', 'school__name')

# -------------------------
# Other Admins
# -------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name", "code")

@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = ("year", "date")
    list_filter = ("year",)

@admin.register(GradingStructure)
class GradingStructureAdmin(admin.ModelAdmin):
    list_display = ("subject", "grade", "min_score", "max_score", "remark")
    list_filter = ("subject", "grade")
    ordering = ("subject", "-max_score")

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score", "academic_period", "computed_grade", "computed_remark")
    list_filter = ("academic_period", "subject")
    search_fields = ("student__full_name", "student__index_number")

    def computed_grade(self, obj):
        return obj.get_grade()

    def computed_remark(self, obj):
        return obj.get_remark()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Only results belonging to this school
        return qs.filter(student__school=request.user.schooladministrator.school)


# -----------
# About_us
# ------------

@admin.register(About_us)
class About_usAdmin(admin.ModelAdmin):
    list_display = ('admin_name', 'content')
   
# ------------------
# SCHEDULE
# ------------------

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('activity_name','activity_description','activity_image')
    list_filter = ("activity_name","date")
    search_fields = ("date","activity_name")
   
 
 # -------------
# CAROUSEL
# --------------

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('carousel_description','carousel_image')

# --------------
# CONTACT US
# -------------      

@admin.register(Contact_us)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_name','contact','message')

# ---------------
# OUR PARTNERS
# ---------------
@admin.register(Our_partners)
class Our_partnerAdmin(admin.ModelAdmin):
    list_display = ('partner_name','partner_image')
    search_fields = ("partner_name",'partner_image')

# -------------------------
# Student Admin
# -------------------------

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("index_number", "full_name", "school", "gender", "year","quran_marks","quran_grade","fighu_marks","fighu_grade","lugha_marks","lugha_grade","tarbia_marks","tarbia_grade","division","student_image")
    search_fields = ("index_number", "full_name")
    list_filter = ("school", "gender", "year")

    
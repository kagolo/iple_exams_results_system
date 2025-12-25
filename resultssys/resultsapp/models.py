# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# -------------------------
#  SCHOOLS
# -------------------------
class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    school_logo = models.FileField(upload_to='pics')
    police_station = models.CharField(max_length=255) 
    head_teacher_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    dos_theology_name = models.CharField(max_length=255)

    # @property
    # def get_sch_count(self):
    #     total_count = self.name.count() 
    #     return total_count



    def __str__(self):
        return f"{self.code} - {self.name}"


class SchoolAdministrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.school.name}"



# -------------------------
#  ACADEMIC PERIOD / EXAM SESSION
# -------------------------
class AcademicPeriod(models.Model):
    year = models.IntegerField(unique=True)
    date = models.DateField()

    def __str__(self):
        return str(self.year)


# -------------------------
#  SUBJECTS
# -------------------------
class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# -------------------------
#  STUDENTS
# -------------------------
class Student(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    index_number = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    year = models.IntegerField()
    quran_marks = models.IntegerField()
    quran_grade = models.IntegerField()
    fighu_marks = models.IntegerField()
    fighu_grade = models.IntegerField()
    lugha_marks = models.IntegerField()
    lugha_grade = models.IntegerField()
    tarbia_marks = models.IntegerField()
    tarbia_grade = models.IntegerField()
    division = models.IntegerField()

    @property
    def get_total(self):
        total = self.quran_grade + self.fighu_grade + self.lugha_grade + self.tarbia_grade
        return total

    @property
    def get_count(self):
        total_count = self.division.count("1") 
        return total_count

    def __str__(self):
        return f"{self.index_number} - {self.full_name}"
    
    # @property
    # def imageURL(self):
    #     try:
    #         url = self.student_image.url
    #     except:
    #         url = ''
    #     return url



# -------------------------
#  GRADING STRUCTURE
# -------------------------
class GradingStructure(models.Model):
    """
    Defines grade boundaries for each subject or globally.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, help_text="Leave blank for global grading.")
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    grade = models.CharField(max_length=10)
    remark = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("subject", "min_score", "max_score")
        ordering = ["-max_score"]

    def __str__(self):
        if self.subject:
            return f"{self.subject.name}: {self.grade} ({self.min_score}-{self.max_score})"
        return f"Global: {self.grade} ({self.min_score}-{self.max_score})"


# -------------------------
#  RESULTS
# -------------------------

class Result(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    academic_period = models.ForeignKey("AcademicPeriod", on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ("student", "subject", "academic_period")

    def __str__(self):
        return f"{self.student.index_number} - {self.subject.code} - {self.score}"

    # -------------------------
    # Compute grade
    # -------------------------
    def get_grade(self):
        # Subject-specific grading
        grading = GradingStructure.objects.filter(
            subject=self.subject,
            min_score__lte=self.score,
            max_score__gte=self.score
        ).first()

        # Global grading
        if not grading:
            grading = GradingStructure.objects.filter(
                subject__isnull=True,
                min_score__lte=self.score,
                max_score__gte=self.score
            ).first()

        return grading.grade if grading else "N/A"

    # -------------------------
    # Compute remark
    # -------------------------
    def get_remark(self):
        # Subject-specific grading
        grading = GradingStructure.objects.filter(
            subject=self.subject,
            min_score__lte=self.score,
            max_score__gte=self.score
        ).first()

        # Global grading
        if not grading:
            grading = GradingStructure.objects.filter(
                subject__isnull=True,
                min_score__lte=self.score,
                max_score__gte=self.score
            ).first()

        return grading.remark if grading else ""

    # -------------------------
    # Compute total score for the student in this period
    # -------------------------
    @property
    def total_score(self):
        results = Result.objects.filter(
            student=self.student,
            academic_period=self.academic_period
        )
        return sum(r.score for r in results)

    # -------------------------
    # Compute division dynamically based on total_score
    # -------------------------
    @property
    def division(self):
        total = self.total_score
        grading_rules = GradingStructure.objects.all().order_by('-min_score')
        for rule in grading_rules:
            if total >= rule.min_score:
                return rule.grade 
        return "Ungraded"


# ---------------
# ABOUT US
# ----------------
class About_us(models.Model):
    admin_name = models.CharField(max_length=255) 
    content = models.CharField(max_length=5000)
    content_2 = models.CharField(max_length=5000)
    content_3 = models.CharField(max_length=5000)

    def __str__(self):
        return self.admin_name


# ------------------
# SCHEDULE
# ------------------

class Schedule(models.Model):
           date = models.DateField()
           activity_name = models.CharField(max_length=255)
           activity_description = models.CharField(max_length=255)

           activity_image = models.FileField(upload_to='pics')
           
           def __str__(self):
               return self.activity_name

# -------------
# CAROUSEL
# --------------

class Carousel(models.Model):
    carousel_image = models.ImageField(upload_to='c_pic')
    carousel_description = models.CharField(max_length=200)

    def __str__(self):
        return self.carousel_description
    

# ---------------
# CONTACT US
# --------------

class Contact_us(models.Model):
    user_name = models.CharField(max_length=100,null=False)
    contact = models.CharField(max_length=100,null=False)
    message = models.CharField(max_length=1000,null=False)
    
    
    def __str__(self):
        return self.user_name
    
# ---------------
# OUR PARTNERS
# ---------------

class Our_partners(models.Model):
    partner_name = models.CharField(max_length=100,null=False)
    partner_image = models.ImageField(upload_to='c_pic')

    def __str__(self):
        return self.partner_name
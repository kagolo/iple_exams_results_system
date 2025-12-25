from.models import(Student, Subject, Result, GradingStructure)

def get_students():
    return Student.objects.all()



def get_subjects():
    return Subject.objects.all()

def get_subject(subject_id):
    return Subject.objects.get(pk=subject_id)



def get_results():
    return Result.objects.all()

def get_result(result_id):
    return Result.objects.get(pk=result_id)




def get_student_in_students(student):
    return Student.objects.filter(student=student)
    
def get_student(student_id):
    return Student.objects.get(pk=student_id)
   
from.models import(Student)

def get_students():
    return Student.objects.all()

def get_student(student_id):
    return Student.objects.get(pk=student_id)

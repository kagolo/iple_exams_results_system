from.models import(School, SchoolAdministrator)

def get_schools():
    return School.objects.all()

def get_school(school_id):
    return School.objects.get(pk=school_id)

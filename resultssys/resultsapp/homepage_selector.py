from.models import(About_us, Schedule, Our_partners,Carousel,Contact_us)

# About_us
def get_all_about_us():
    return About_us.objects.all()

def get_about_us(about_us_id):
    return About_us.objects.get(pk=about_us_id)

# Schedule
def get_schedules():
    return Schedule.objects.all()

def get_schedule(schedule_id):
    return Schedule.objects.get(pk=schedule_id)

# Our_partners
def get_our_partners():
    return Our_partners.objects.all()

def get_our_partner(our_partners_id):
    return Our_partners.objects.get(pk=our_partners_id)


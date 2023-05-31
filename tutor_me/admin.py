from django.contrib import admin
from .models import *

# Register your models here.
class AppointmentsAdmin(admin.ModelAdmin):
    #list_display = ("appt_id", "tutor_name", "student_name", "course_dept", "course_num", "start", "end")
    list_display = ("student", "course", "start", "end", "confirmed")
    search_fields = ("student", "course", "start", "end", "confirmed")
    #search_fields = ("appt_id", "tutor_name", "student_name", "course_dept", "course_num", "start", "end")

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("user", "start", "end")
    search_fields = ("user", "start", "end")

# # Register your models here.
admin.site.register(Appointment, AppointmentsAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(Course)
admin.site.register(Rate)
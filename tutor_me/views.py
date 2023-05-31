'''
REFERENCES

Title: GPT-3.5 Language Model
Author: OpenAI
Date: 2021-09
Code version: 3.5
URL: https://openai.com/
Software License: <OpenAI API Terms of Service>
Note: Nearly exclusively used for accessing Django objects and their built-in functions

Title: User Registration in Django using Google OAuth
Author: Geoffrey Mungai
Date: 2020-12
Code version: N/A
URL: https://www.section.io/engineering-education/django-google-oauth/
Software License: N/A
Note: Used for the google authentication login
'''

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
import pytz
import requests
from tutor_me.models import Course, Appointment, Availability, RequestNotification, Rate


def get_url_page(page):
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=" + \
        str(page)
    return requests.get(url).json()


def set_classes():
    counter = 1
    url_list = get_url_page(counter)
    done = {}
    while len(url_list) > 0:
        for c in url_list:
            if c['subject'] + c["catalog_nbr"] not in done:
                course = Course(number=c['catalog_nbr'], mnemonic=c['subject'], name=c['descr'],)
                course.save()
                done[c['subject'] + c["catalog_nbr"]] = True
        counter += 1
        url_list = get_url_page(counter)


def is_student(user):
    return user.groups.filter(name='student').exists()


def is_tutor(user):
    return user.groups.filter(name='tutor').exists()


def is_not_registered(user):
    return is_student(user) or is_tutor(user)


def get_user(request):
    return request.user


def get_url_page(page):
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=" + \
        str(page)
    return requests.get(url).json()

# Some code from GPT-3.5 Language Model
def get_classes():
    # retrieve all Course objects from the database
    courses = Course.objects.all()

    # construct the list of strings
    classes = [f"{course.mnemonic} {course.number} - {course.name}" for course in courses]
    # classes = list(set(classes))
    # classes.sort()
    return classes

def get_course_str(course):
    se_list = course.split()
    mnemonic = se_list[0]
    number = se_list[1]
    return [mnemonic, number]

# Some code from GPT-3.5 Language Model
def tutor(request):

    #set_classes()
    user = get_user(request)
    if not is_tutor(user):
        return HttpResponse("You are not logged in as a tutor, so you cannot view this page.")
    user_classes = user.course_set.all()
    classes = get_classes()
    current_time = datetime.now()
    all_available = Availability.objects.filter(user=request.user, end__gt=current_time)
    requests = Appointment.objects.filter(availability__user=user, end__gt=current_time)
    appts = requests.filter(confirmed=True)
    rate_obs = Rate.objects.filter(user=user)
    username = user.first_name + " " + user.last_name
    rate = ""
    if rate_obs:
        rate = rate_obs[0].rate


    context = {
        "classes": classes, "timeslots": all_available, "user_classes": user_classes,
        "requests":requests, "appointments": appts, "rate": rate, "username": username,
        }

    if rate:
        context["int_rate"] = int(rate)

    # Set hourly rate
    try:
        rate = request.POST.get("set_rate")
        all_rates = Rate.objects.all()
        int_rate = int(rate)
        context['int_rate'] = int_rate
        for rates in all_rates:
            if rates.user == user:
                rates.rate = int(rate)
                rates.save()
                context['rate'] = rate
                return render(request, 'tutor_me/tutor_view.html', context)
        else:
            hourly_rate = Rate(user=user, rate=int(rate))
            hourly_rate.save()
            context['rate'] = rate
            return render(request, 'tutor_me/tutor_view.html', context)


    except:
        pass


    # Dropdown Request Process
    try:
        search = request.POST['class-dropdown']
        se_list = search.split()
        mnemonic = se_list[0]
        number = se_list[1]
        course = get_object_or_404(Course, number=number, mnemonic=mnemonic)
        user.course_set.add(course)
        return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass

    # Delete tutor class
    try:
        tutor_class_id = request.POST.get('tutor_class_id')
        if tutor_class_id:
            user.course_set.remove(tutor_class_id)
            return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass

    # Availability Form Process

    try:
        #available = request.POST['save_availability']
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if end_time <= start_time:
            context["error_message"] = "Invalid times entered. Start time must come before end time. Please try again."
            return render(request, 'tutor_me/tutor_view.html', context)
        my_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        my_end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        if my_start.date() != my_end.date():
            context["error_message"] = "Invalid times entered. Start and end time must be on the same day. Please try again."
            return render(request, 'tutor_me/tutor_view.html', context)
        available_times = Availability.objects.filter(user=request.user, end__gt=current_time)
        for availi in available_times:
            eastern_timezone = pytz.timezone('US/Eastern')
            if availi.start <= my_start.astimezone(eastern_timezone)+timedelta(hours=1) <= availi.end \
                    or availi.start <= my_end.astimezone(eastern_timezone)+timedelta(hours=1) <= availi.end:
                context["error_message"] = "Invalid times entered. Times cannot conflict with another availability " \
                                           "slot. Please try again. "
                return render(request, 'tutor_me/tutor_view.html', context)
        availability = Availability(start=my_start, end=my_end, user=user)
        availability.save()

        context["timeslots"] = Availability.objects.filter(user=request.user, end__gt=current_time)
        return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass
    #delete available slots if needed
    try:
        avail_id = request.POST.get('delete_avail_id')
        if avail_id:
            avail = all_available.get(id=avail_id)
            avail.delete()
            return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass

    #handle student appointment requests
    #--------->accept request
    try:
        request_id = request.POST.get('request_accept')
        if request_id:
            req_yes = requests.get(id=request_id)
            req_yes.confirmed=True
            req_yes.save()
            return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass

    #--------->deny request
    try:
        request_id = request.POST.get('request_deny')
        if request_id:
            req_no = requests.get(id=request_id)
            notification = "Your request with " + req_no.availability.user.first_name
            notification += " " + req_no.availability.user.last_name + " for " + req_no.course.mnemonic
            notification += " " + req_no.course.number + " on " + (req_no.end+timedelta(hours=-5)).strftime("%B%e")
            notification += " from " + (req_no.start+timedelta(hours=-5)).strftime("%I:%M %p") + " to "
            notification += (req_no.end+timedelta(hours=-5)).strftime("%I:%M %p") + " was denied."
            notif = RequestNotification(student=req_no.student, notification=notification)
            notif.save()
            req_no.delete()
            return render(request, 'tutor_me/tutor_view.html', context)
    except:
        pass

    return render(request, 'tutor_me/tutor_view.html', context)



def view_redirect(request):
    user = get_user(request)
    error = False
    try:
        selected_choice = request.POST['group']
    except:
        error = True
        pass
    if not error:
        user.groups.add(selected_choice)
        user.save()
    if is_student(user):
        return student(request, is_redirect=True)
    elif is_tutor(user):
        return tutor(request)
    # DOES NOT ALLOW FOR CHANGING GROUP
    return HttpResponse("Error at view_redirect")


def index(request):
    user = get_user(request)
    anon = user.is_anonymous
    if anon:
        return render(request, 'tutor_me/google_login.html')
    elif not anon and (is_tutor(user) or is_student(user)):
        return view_redirect(request)
    else:
        groups = Group.objects
        return render(request, 'tutor_me/signup.html', {'user': user, 'groups': groups})

# User Registration in Django using Google OAuth
def login(request):
    return render(request, 'tutor_me/google_login.html')

# Some code from GPT-3.5 Language Model
def student(request, is_redirect=False):
    user = get_user(request)
    if is_student(user):
        notifications = RequestNotification.objects.filter(student=request.user)
        requests = Appointment.objects.filter(student=user)
        current_time = datetime.now()
        appts = requests.filter(confirmed=True, end__gt=current_time)
        if request.method == "GET":
            if request.GET.get('name') != None:
                course = request.GET.get("course")
                course_data = get_course_str(course)
                tutor = extract_user_info(request.GET.get('tutor'))
                context = {'course': course_data[0] + " " + course_data[1], "tutor": tutor[0] + " " + tutor[1],
                           "id": tutor[2], "date": tutor[4], "start": tutor[3], "end": tutor[5]}
                return render(request, 'tutor_me/submit_request.html', context)
        classes = get_classes()
        tutors = []
        context = {'classes': classes, 'tutors': tutors, "course": "", "appointments": appts, "notifications": notifications}

        all_availabilities = Availability.objects.filter(end__gt=current_time)

        #submitting request for appointment
        if request.method == "POST":
            try:
                notif_id = request.POST.get('delete_notification_id')
                if notif_id:
                    notif = notifications.get(id=notif_id)
                    notif.delete()
                    context["notifications"] = RequestNotification.objects.filter(student=request.user)
                    return render(request, 'tutor_me/student_view.html', context)
            except:
                pass
            try:
                course = request.POST.get("class-dropdown")
                course_data = get_course_str(course)
                all_availabilities = all_availabilities.filter(
                    user__course__mnemonic=course_data[0],
                    user__course__number=course_data[1],
                    end__gt=current_time
                )
                message = ""
                if course != "":
                    message = "Choose the tutor availability for " + course
                tutors.append(find_tutor(all_availabilities))
                course_data = get_course_str(course)
                availabilities = get_availability_array(all_availabilities)
                context = {
                    'classes': classes, 'tutors': tutors, "message": message,
                    "course": course_data[0] + " " + course_data[1], 'availabilities': availabilities, "appointments": appts, "notifications": notifications
                }
            except:
                try:
                    return submit_request(request)
                except:
                    pass
        return render(request, 'tutor_me/student_view.html', context)
    else:
        return HttpResponse("You are not logged in as a student, so you cannot view this page.")



def extract_user_info(info):
    # split the string by whitespace
    parts = info.split()

    # find the indices of "first_name" and "last_name"

    # extract the first name and last name using the indices
    first_name = parts[0]  # add 2 to skip "is" and "available"
    last_name = parts[1]
    id = parts[16]
    start = parts[9] + " " + parts[10]
    date = parts[6] + " " + parts[7]
    end = parts[12] + " " + parts[13][0:-1]

    return (first_name, last_name, id, start, date, end)


def find_tutor(all_availability):
    eastern_timezone = pytz.timezone('US/Eastern')
    all = get_availability_array(all_availability)
    possible_tutors = []
    for available in all:
        info = available["title"] + " is available on "
        dt = datetime.fromisoformat(available["start"]).astimezone(eastern_timezone)
        # info += dt.strftime('%I:%M %p') + " on " + dt.strftime('%B %d') + " to "
        info += dt.strftime('%B %d') + " from " + dt.strftime('%I:%M %p') + " to "
        dt = datetime.fromisoformat(available["end"]).astimezone(eastern_timezone)
        info += dt.strftime('%I:%M %p') + ". Appointment ID: " + str(available["id"])
        possible_tutors.append(info)
    return possible_tutors


def student_appointment(request):
    classes = get_classes()
    context = {'classes': classes}
    return render(request, 'tutor_me/student_appointment.html', context)

# Some code from GPT-3.5 Language Model
def submit_request(request):
        user = get_user(request)
        if request.method == 'POST':
            # Get the submitted form data
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            course_data = get_course_str(request.POST['course'])
            note = request.POST['note']
            id = request.POST['id']
            date = request.POST['date']
            start = request.POST['start']
            end = request.POST['end']
            context = {'course': request.POST['course'], "tutor": request.POST['tutor'],
                       "id": request.POST['id'], "date": date, "start": start, "end": end}
            if start_time == "" or end_time == "":
                error_message = "Time(s) not entered. Both start and end time must be entered. Please try again."
                context["error_message"] = error_message
                return render(request, 'tutor_me/submit_request.html', context)

            start_app = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_app = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
            start_avail = datetime.strptime(date + " 2023 " + start, '%B %d %Y %I:%M %p')
            end_avail = datetime.strptime(date + " 2023 " + end, '%B %d %Y %I:%M %p')

            if start_app >= end_app:
                error_message = "Invalid times entered. Start time must come before end time. Please try again."
                context["error_message"] = error_message
                return render(request, 'tutor_me/submit_request.html', context)
            if (start_avail > start_app) or (start_app > end_avail) or (start_avail > end_app) or (end_app > end_avail):
                error_message = "Invalid times entered. Times entered must fall within availability slot. Please try again."
                context["error_message"] = error_message
                return render(request, 'tutor_me/submit_request.html', context)
            appointment = Appointment(
                start=start_app,
                end=end_app,
                note=note,
                student=user,
                course=get_object_or_404(Course, mnemonic=course_data[0], number=course_data[1]),
                availability=get_object_or_404(Availability, id=int(id)),
            )
            appointment.save()
            classes = get_classes()
            tutors = []
            success_message = "Your request has been submitted successfully!"
            context = {'classes': classes, 'tutors': tutors, "course": "", "success_message": success_message}
            return render(request, 'tutor_me/student_view.html', context)
        return render(request, 'tutor_me/submit_request.html')

def success(request):
    return render(request, 'tutor_me/success.html')

# Some code from GPT-3.5 Language Model
def get_availability_array(all_availabilities):
    availabilities = []
    for a in all_availabilities:
        # Get all appointments that overlap with the availability block
        rate = Rate.objects.filter(user=a.user)[0].rate
        appointments = Appointment.objects.filter(
            availability=a,
            # start__lt=a.end,
            # end__gt=a.start,
            confirmed=True,
        ).order_by('start')
        if not appointments.exists():
            availabilities.append({
                "title": a.user.first_name + " " + a.user.last_name + " ($" + str(rate) + ")",
                "start": (a.start - timedelta(hours=1)).isoformat(),
                "end": (a.end - timedelta(hours=1)).isoformat(),
                "id": str(a.id)
            })
            continue

        start_time = a.start
        # Split the availability block into smaller blocks that do not overlap with the appointments
        for appointment in appointments:
            if start_time < appointment.start:
                # Add the availability block before the appointment
                availabilities.append({
                    "title": a.user.first_name + " " + a.user.last_name + " ($" + str(rate) + ")",
                    "start": (start_time - timedelta(hours=1)).isoformat(),
                    "end": (appointment.start - timedelta(hours=1)).isoformat(),
                    "id": str(a.id)
                })
            start_time = appointment.end

        if start_time < a.end:
            # Add the availability block after the last appointment
            availabilities.append({
                "title": a.user.first_name + " " + a.user.last_name + " ($" + str(rate) + ")",
                "start": (start_time - timedelta(hours=1)).isoformat(),
                "end": (a.end - timedelta(hours=1)).isoformat(),
                "id": str(a.id)
            })
    return availabilities


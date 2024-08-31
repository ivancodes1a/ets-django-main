import hashlib
from .models import Event
from django.template import loader
from profiles.models import Profile
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from .forms import EventCreationForm, EventEditForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homeView(request):
    profile = Profile.objects.get(user=request.user)
    form    = EventCreationForm(request.POST or None, request.FILES or None)
    events  = Event.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = profile  
            event.save()
            event.attendees.add(profile)  

            # Set a flag in the session to indicate a successful event creation
            request.session['eventCreated'] = True

    template = loader.get_template('events/home.html')
    context  = {
        "profile": profile,
        'form'   : form,
        'events' : events,
    }
    return HttpResponse(template.render(context, request))


@login_required
def eventDetailView(request, id):
    profile = Profile.objects.get(user=request.user)
    event   = Event.objects.get(pk=id)

    profileEmail   = profile.email 
    senderEmail    = "2004668@students.kcau.ac.ke"
    eventName      = event.title
    uuid           = generateUUID(profileEmail)
    profileSubject = f'Your UID for {eventName}'

    if request.method == 'POST':
        if profile not in event.attendees.all():
            sendUUID(profileSubject, senderEmail, profileEmail, uuid)
            event.attendees.add(profile)
            request.session['eventBooked'] = True

    template = loader.get_template('events/eventDetail.html')
    context = {
        'event'  : event,
        'profile': profile,
        'uuid'   : uuid,  
    }
    return HttpResponse(template.render(context, request))


def generateUUID(email):
    hashObject = hashlib.sha1(email.encode())
    hexDigit   = hashObject.hexdigest()
    uuid       = '-'.join([hexDigit[:3], hexDigit[4:7], hexDigit[8:11]])
    return uuid


def sendUUID(eventName, senderEmail, receiverEmail, uuid):
    subject = eventName
    message = f'Here is your 9-character UUID from the event organizer: {uuid}'
    send_mail(subject, message, senderEmail, [receiverEmail], fail_silently=False)


@login_required
def eventEditView(request, id):
    profile = Profile.objects.get(user=request.user)
    event   = Event.objects.get(pk=id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home:eventDetail', id=id)
    else:
        form = EventEditForm(instance=event)

    template = loader.get_template('events/eventEdit.html')
    context = {
        'event'   : event,
        'profile' : profile,
        'form'    : form,
    }
    return HttpResponse(template.render(context, request))
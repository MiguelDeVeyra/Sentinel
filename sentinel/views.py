from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.forms.models import model_to_dict

# Python
import datetime as dt

# Utilities
from .camera import video_camera, generate

# Ploty
from plotly.offline import plot
import plotly.graph_objs as go

# Models
from .models import end_user

# Global Variables
SESSION_TIMEOUT = (60*5)
cam = video_camera()

# Created Views
def index(request):     # to Login Page
    request.session.set_expiry(SESSION_TIMEOUT)
    return render(request, 'sentinel/index.html')

def home(request):      # to Home Page
    valid = {}
    if request.method == 'POST':
        valid['email'] = request.POST['email']
        valid['password'] = request.POST['pass']
    else: # gets session variables
        valid = check_session(request)

    if valid:
        if end_user.objects.filter(email = valid['email']).exists(): # validation
            temp_user = end_user.objects.get(email = valid['email'])
            if valid['password'] == temp_user.password:
                request.session['user'] = model_to_dict(temp_user)
                request.session.set_expiry(SESSION_TIMEOUT)
                return render(request, 'sentinel/home.html')
            else:
                error_msg = 'Invalid Password'
        else:
            error_msg = 'Email does not Exist'
    else:
        error_msg = 'Session has Expired'

    context = {
        'error_msg': error_msg,
    }
    return render(request, 'sentinel/index.html', context)

def generalReports(request):
    valid = check_session(request)
    if valid:
        Incidents = go.Scatter(
            x=[dt.date(2017, 1, 1), dt.date(2017, 1, 3), dt.date(2017, 1, 3)],
            y=[dt.time(8, 0, 0), dt.time(12, 0, 0), dt.time(16, 0, 0)],
            mode='markers',
            name='Incident',
        )

        fig = go.Figure([Incidents])
        fig.update_xaxes(tickformat='%m/%d/%y', tickangle=45)
        fig.update_yaxes(range=[dt.time(0,0,0), dt.time(23,0,0)])

        plot_div = plot(fig, output_type='div')

        context = {
            'plot_div': plot_div,
        }
        request.session.set_expiry(SESSION_TIMEOUT)
        return render(request, 'sentinel/generalReports.html', context)
    else:
        error_msg = 'Session has Expired'

    context = {
        'error_msg': error_msg,
    }
    return render(request, 'sentinel/index.html', context)

def incidentList(request):
    valid = check_session(request)
    if valid:
        request.session.set_expiry(SESSION_TIMEOUT)
        return render(request, 'sentinel/incidentList.html')
    else:
        error_msg = 'Session has Expired'

    context = {
        'error_msg': error_msg,
    }
    return render(request, 'sentinel/index.html', context)

def incidentReport(request):
    valid = check_session(request)
    if valid:
        request.session.set_expiry(SESSION_TIMEOUT)
        return render(request, 'sentinel/incidentReport.html')
    else:
        error_msg = 'Session has Expired'

    context = {
        'error_msg': error_msg,
    }
    return render(request, 'sentinel/index.html', context)

def notifications(request):
    valid = check_session(request)
    if valid:
        request.session.set_expiry(SESSION_TIMEOUT)
        return render(request, 'sentinel/notifs.html')
    else:
        error_msg = 'Session has Expired'

    context = {
        'error_msg': error_msg,
    }
    return render(request, 'sentinel/index.html', context)

def video_feed(request):
    try:
        return StreamingHttpResponse(generate(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

# helper functions
def check_session(request):
    context = {}
    try:
        context['email'] = request.session['user']['email']
        context['password'] = request.session['user']['password']
    except KeyError as ke: # no session
        print('[WARNING] Session not valid')

    return context

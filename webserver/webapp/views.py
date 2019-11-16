from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from rest_framework.decorators import api_view

from webapp.user_api import user_register

from rest_framework.status import \
    HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN, \
    HTTP_409_CONFLICT


@api_view(['POST'])
def user_registration(request):
    """
    Result view for the user.
    Renders a failure page in case an image has not been processed yet
    """
    r = user_register(request)
    if r == HTTP_400_BAD_REQUEST:
        return HttpResponse(render_to_string('registration.html', r))
    if r == HTTP_201_CREATED:
        return HttpResponse(render_to_string('choose_countries.html', r))
    else:
        return HttpResponseNotFound()


@api_view(['GET'])
def user_registration(request):
    """
    Result view for the user.
    Renders a failure page in case an image has not been processed yet
    """

    return HttpResponse(render_to_string('registration.html'))

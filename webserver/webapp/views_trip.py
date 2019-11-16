from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import render_to_string

from rest_framework.request import Request
from rest_framework.decorators import api_view

from webapp import api_trip
from webapp.Trip import Trip


@api_view(['GET'])
def trip_get(request: Request):
    """
    Get a Trip (which may have already been or have not been prepared)
    """
    trip_id = request.query_params.get('id')
    if trip_id is None:
        return HttpResponseBadRequest()

    try:
        trip = api_trip.get_trip(trip_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    return HttpResponse(render_to_string('trip.html', _trip_to_view(trip)))


@api_view(['GET'])
def trip_step(request: Request):
    parameters = request.query_params

    home_country = parameters.get('hc')
    if home_country is None:
        return HttpResponse(render_to_string('step_hc.html'))

    interests = parameters.get('in')
    if interests is None:
        return HttpResponse(render_to_string('step_in.html', {
            'hc': home_country
        }))

    destinations = parameters.get('dst')
    if destinations is None:
        return HttpResponse(render_to_string('step_dst.html', {
            'hc': home_country,
            'in': interests
        }))

    trip = api_trip.create_trip(home_country, interests, destinations)
    return HttpResponseRedirect('/result?id={}'.format(trip.id))


def _trip_to_view(trip: Trip) -> dict:
    """
    Transform a Trip object into a dictionary for the HTML template
    """
    # TODO
    return {
        'id': trip.id
    }

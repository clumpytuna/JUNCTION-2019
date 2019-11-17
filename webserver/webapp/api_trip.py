import json

from utils.id_generator import gen_uuid

from webapp.CategoryInCountry import CategoryInCountry
from webapp.Category import Category
from webapp.Trip import Trip
from webapp.Product import Product
from webapp.Country import Country


def _generate_trip(trip: Trip) -> Trip:
    """
    Re-generate the trip using the countries and the user data
    :param trip: a trip to process
    :return: the resulting Trip object, saved in the database
    """
    if trip is None:
        raise Exception("The provided Trip is None")

    # All other fields of the Trip must be validated

    # Select the required products
    category_in_country_rs = CategoryInCountry.objects.all()\
        .filter(id_country__in=trip.countries, id_category__in=trip.interests)\
        .order_by('id_category', 'price')

    result = dict()
    for country_id in trip.countries:
        result[country_id] = []

    # Iterate over categories in countries
    previous_category_in_country = None
    for category_in_country in category_in_country_rs:
        if not(
                previous_category_in_country is not None or
                category_in_country.id_category != previous_category_in_country.id_category
        ):
            continue
        previous_category_in_country = category_in_country
        result[category_in_country.country_id].append(category_in_country)

    # Get categories data. This requires us to make multiple SQL requests
    for country_id in result.keys():
        if len(result[country_id]) == 0:
            result[country_id] = None
        for i in range(len(result[country_id])):
            category_in_country = result[country_id][i]
            category = Category.objects.get(category_in_country.id_category)
            products = Product.objects.all().filter(id_category=category.id, id_country=country_id)
            result_for_category_in_country = {
                'id_category': category_in_country.id,
                'name': category.name,
                'description': category.description,
                'price': category_in_country.price,
                'products': [
                    {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'link': product.link,
                    }
                    for product in products
                ],
            }
            result[country_id][i] = result_for_category_in_country

    # Now result is complete. Write it to our model
    results = []
    for country_id in trip.countries:
        results.append(json.dumps(result[country_id]))

    trip.results = results
    trip.prepared = True
    trip.save()
    trip.refresh_from_db()
    return trip


def get_trip(trip_id: str) -> Trip:
    """
    Get a Trip object. If it is not prepared, prepare it
    :raises: ObjectDoesNotExist
    """
    trip = Trip.objects.get(id=trip_id)

    if not trip.prepared:
        _generate_trip(trip)

    return trip


def _check_countries(countries: list) -> bool:
    """
    Check the given 'countries' exist
    """
    countries_count = Country.objects.all() \
        .filter(id__in=countries) \
        .distinct().count()

    if countries_count != len(set(countries)):
        return False

    return True


def _check_categories(categories: list) -> bool:
    """
    Check the given 'categories' exist
    """
    categories_count = Category.objects.all() \
        .filter(id__in=categories) \
        .distinct().count()

    if categories_count != len(set(categories)):
        return False

    return True


def create_trip(home_country: str, interests: list, destinations: list) -> Trip:
    """
    Create a new Trip
    :return: the new trip, saved in the database
    """
    if home_country is None or interests is None or destinations is None:
        raise Exception("One or more of the provided parameters are None")

    if len(interests) == 0 or len(destinations) == 0:
        raise Exception("One or more of the provided parameters have length 0")

    if not _check_categories(interests):
        raise Exception("One or more interests do not exist")

    if not _check_countries(destinations + [home_country]):
        raise Exception("A home country or one of the destination countries does not exist")

    # The data is now validated. Create a Trip object
    trip = Trip(id=gen_uuid(), home_country=home_country, interests=interests, countries=destinations)

    trip.save()
    return trip

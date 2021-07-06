import requests
import os


def get_place_id(name):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={0}&inputtype=textquery&key={1}'.format(name, os.getenv('API_KEY'))).json()
    # place_id = response['']
    print(response)

    return response


def get_place_details(name):
    place_id = get_place_id(name)

    place_details = requests.get(
        'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=business_status,formatted_address,geometry,name,type,formatted_phone_number,opening_hours,price_level,rating,review&key={}'.format(place_id, os.getenv('API_KEY')))

    return place_details

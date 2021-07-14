import requests, os

def get_place_id(name):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={0}&inputtype=textquery&key={1}'.format(name, os.getenv('API_KEY'))).json()
    print(response)
    place_id = None if len(response['candidates']) == 0 else response['candidates'][0]['place_id']
    return place_id


def get_place_details(name):
    place_id = get_place_id(name)
    if place_id == None:
        return {}

    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/details/json?place_id={0}&language=pt-BR&fields=business_status,formatted_address,geometry/location,name,formatted_phone_number,opening_hours/weekday_text,price_level&key={1}'.format(place_id, os.getenv('API_KEY'))).json()

    place_details = {} if response == {} else response['result']

    return place_details

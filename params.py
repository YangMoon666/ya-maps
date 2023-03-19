import const


def params_func(ll=[52.29723, 54.901171], spn=0.001, l='map', search_place='Альметьевск', pt='', params_type='static'):
    if params_type == 'static':
        params = {
            "ll": ",".join([str(ll[0]), str(ll[1])]),
            'spn': ",".join([str(spn), str(spn)]),
            "l": l,
            'pt': pt
        }
    elif params_type == 'geocoder':
        params = {
            "apikey": const.GEOCODER_API,
            "geocode": search_place,
            "format": "json"
        }
    return params or False
def params_func(ll=['52.29723', '54.901171'], spn=0.001, l='map'):
    params = {
        "ll": ",".join(ll),
        'spn': ",".join([str(spn), str(spn)]),
        "l": l
    }

    return params
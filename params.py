def params_func(ll=['52.29723', '54.901171'], spn='0.01', l='map'):

    params = {
        "ll": ",".join(ll),
        'spn': ",".join([spn, spn]),
        "l": l
    }

    return params
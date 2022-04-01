import logging

def show_raw(opts):
    raw = False
    for i in range(len(opts)):
        arg = opts[i]
        match arg:
            case '-r' | '--raw':
                raw = True
                logging.info('Set raw : %s', raw)
    return raw

def show_response(results):
    ''' Display the filtered response '''
    if (results is None):
        return

    if (len(results) > 0):
        for result in results:
            print(result)
            print()
    else:
        print(results)
    return

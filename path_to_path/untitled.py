def secondsToText(secs):
    days = secs // 86400
    hours = (secs - days * 86400) // 3600
    minutes = (secs - days * 86400 - hours * 3600) // 60
    seconds = str("{0:.2f}".format(secs - days * 86400 - hours * 3600 - minutes * 60)).split('.')[0]
    msec = str("{0:.2f}".format(secs - days * 86400 - hours * 3600 - minutes * 60)).split('.')[1]

    return [int(hours),
    		int(minutes),
    		int(seconds),
    		int(msec)]

print(secondsToText(15236.1))

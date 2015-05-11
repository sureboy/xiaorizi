from LifeApi.models import NewEventTable

def count_events_info():
    count = {}
    count['from_info_count'] = {}
    count['relevant_count'] = {}
    
    i = 0
    z = 0
    length = NewEventTable.objects.count()


    for event in NewEventTable.objects.all():

        key = event.from_info.count()
        if key in count:
            count['from_info_count'][key] += 1
        else:
            count['from_info_count'][key] = 0
        
        key = event.relevant.count()
        if key in count:
            count['relevant_count'][key] += 1
        else:
            count['relevant_count'][key] = 0

        i += 1

        d = i - z
        df = d / float(length)
        j = int(df / 0.1)
        if j > 0:
            z = i
            print i / float(length) * 100 ,'%'

    return count

if __name__ == '__main__':
    print count_events_info()

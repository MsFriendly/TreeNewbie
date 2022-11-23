import json
import urllib.parse
import requests

#Set you Google Map Static API key here. 
API_KEY = 'AIzaSyAV5sMuLbN9Gn0uuLLcDRoy26bwq75qkpA'
#Set the radius of your searching range. (meters)
RANGE = 500
#Debug Mode: a txt file will be created for debugging
DEBUG = True

def download_images(query:'str'):
    lat, lon = get_center(query)
    l = get_addrs(lat,lon)
    get_images(l)


def get_images(addr_list: list):
    i = 0
    while i < len(addr_list) and i < 30:
        addr = addr_list[i].replace(" ", "+")

        x = requests.get('https://maps.googleapis.com/maps/api/staticmap?',
                         params={'center': addr,
                                 'zoom': 21,
                                 'size': '640x640',
                                 'maptype': 'satellite',
                                 'key': API_KEY})

        addr_sc = addr.replace('+','_')
        with open(f'results/{addr_sc}.png', 'wb') as f:
            f.write(x.content)

        i += 1


def get_addrs(lat,lon):

    addr_list = []

    http = 'https://overpass-api.de/api/interpreter?data='
    query = urllib.parse.quote(
                                f'[out:json][timeout:25];'
                                f'way["building"~"residential|yes|terrace"]["addr:housenumber"]'
                                f'(around:{RANGE},{lat},{lon});'
                                f'out tags;'
                                )
    x = requests.get(http+query);
    datalist = json.loads(x.content)['elements']
    for i in datalist:
        try:
            numberstr = i['tags']['addr:housenumber']
            if ',' in numberstr:
                numbers = numberstr.split(',')
                for j in numbers:
                    addr_list.append(j + " " + i['tags']['addr:street'] + " " + i['tags']['addr:city'])
            else:
                addr_list.append(numberstr +" "+ i['tags']['addr:street']+" "+i['tags']['addr:city'])
        except KeyError:
            continue
    
    # if DEBUG:
    #     with open(f'results/addr_list.txt', 'w') as f:
    #         f.write(str(lat)+","+str(lon)+'\n')
    #         f.write(str(len(addr_list))+'\n')
    #         f.write('\n'.join([i for i in addr_list]))
    
    return addr_list


def get_center(zipcode:str) -> tuple:
    x = requests.get(f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote_plus(zipcode)}&format=json&countrycodes=us')
    lat, lon = json.loads(x.content)[0]['lat'], json.loads(x.content)[0]['lon']
    print(lat,lon)
    return lat, lon


def set_range(range: str):
    RANGE = int(range)


# if __name__ == '__main__':

#     set_range(500)
#     print(RANGE, type(RANGE))

    # query = input("Query: ")
    # download_images(query)
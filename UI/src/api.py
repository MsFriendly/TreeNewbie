# This is a sample Python script.
import json
import urllib.parse

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
# from bs4 import BeautifulSoup

API_KEY = 'AIzaSyAV5sMuLbN9Gn0uuLLcDRoy26bwq75qkpA'
SAVE_API = True
RANGE = 500


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

        with open(f'results/{addr}.png', 'wb') as f:
            addr = addr_list[i].replace("+", "_")
            f.write(x.content)

        i += 1


def get_addrs_area(areaid: int = 3610840804):
    repeat = False

    if SAVE_API:
        with open('results/addr_list.txt', 'r') as f:
            lastid = f.readline()
            if areaid == int(lastid):
                repeat = True

    addr_list = []

    if not repeat:
        # areaid = '3610840806'# + 3600000000
        x = requests.get(f'https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A25%5D%3Bway%5B%22building%22%5D%28area%3A{areaid}%29%3Bout%20tags%3B');
        # print(x.content)
        datalist = json.loads(x.content)['elements']
        for i in datalist:
            try:
                # print(i['tags']['addr:housenumber'] +" "+ str(type(i['tags']['addr:housenumber'] )))
                numberstr = i['tags']['addr:housenumber']
                if(',' in numberstr):
                    numbers = numberstr.split(',')
                    for j in numbers:
                        addr_list.append(j + " " + i['tags']['addr:street'] + " " + i['tags']['addr:city'])
                else:
                    addr_list.append(numberstr +" "+ i['tags']['addr:street']+" "+i['tags']['addr:city'])
            except KeyError:
                continue

        with open(f'results/addr_list.txt', 'w') as f:
            f.write(str(areaid)+'\n')
            f.write(str(len(addr_list))+'\n')
            f.write('\n'.join([i for i in addr_list]))
    else:
        with open('results/addr_list.txt', 'r') as f:
            addr_list = f.read().split('\n')[2:]

    return addr_list


def get_addrs_center(lat,lon):
    repeat = False

    #NEED CHANGE
    # if SAVE_API:
    #     with open('results/addr_list.txt', 'r') as f:
    #         lastid = f.readline()
    #         if areaid == int(lastid):
    #             repeat = True

    addr_list = []

    if not repeat:
        http = 'https://overpass-api.de/api/interpreter?data='
        query = urllib.parse.quote(
                                    f'[out:json][timeout:25];'
                                    f'way["building"~"residential|yes|terrace"]["addr:housenumber"]'
                                    f'(around:{RANGE},{lat},{lon});'
                                    f'out tags;'
                                   )
        # print(http+query)
        # return []
        x = requests.get(http+query);
        # print(x.content)
        datalist = json.loads(x.content)['elements']
        for i in datalist:
            try:
                # print(i['tags']['addr:housenumber'] +" "+ str(type(i['tags']['addr:housenumber'] )))
                numberstr = i['tags']['addr:housenumber']
                if ',' in numberstr:
                    numbers = numberstr.split(',')
                    for j in numbers:
                        addr_list.append(j + " " + i['tags']['addr:street'] + " " + i['tags']['addr:city'])
                else:
                    addr_list.append(numberstr +" "+ i['tags']['addr:street']+" "+i['tags']['addr:city'])
            except KeyError:
                continue

        with open(f'results/addr_list.txt', 'w') as f:
            f.write(str(lat)+","+str(lon)+'\n')
            f.write(str(len(addr_list))+'\n')
            f.write('\n'.join([i for i in addr_list]))
    else:
        with open('results/addr_list.txt', 'r') as f:
            addr_list = f.read().split('\n')[2:]

    return addr_list


def get_area(zipcode: str):
    x = requests.get(f'https://nominatim.openstreetmap.org/search?q={zipcode}&format=json&countrycodes=us')
    placeid = json.loads(x.content)[0]['place_id']
    print(placeid)
    y = requests.get(f'https://nominatim.openstreetmap.org/details?place_id={placeid}&format=json')
    areaid = json.loads(y.content)['osm_id']
    print(areaid)
    return areaid


def get_center(zipcode:str) -> tuple:
    x = requests.get(f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote_plus(zipcode)}&format=json&countrycodes=us')
    lat, lon = json.loads(x.content)[0]['lat'], json.loads(x.content)[0]['lon']
    print(lat,lon)
    return lat, lon


# if __name__ == '__main__':
#     # print_hi('PyCharm')
#     # l = ['2500', '2504', '2510', '2514', '2518', '2522', '2526', '2530', '2600', '2606']
#     # get_images(l)
#     zipcode = input("Query: ")
#     # areaid = get_area(zipcode)
#     # print(areaid+3600000000)
#     # l = get_addrs_area(areaid+3600000000)#areaid+3600000000)

#     lat, lon = get_center(zipcode)
#     l = get_addrs_center(lat,lon)
#     # print(l)
#     get_images(l)

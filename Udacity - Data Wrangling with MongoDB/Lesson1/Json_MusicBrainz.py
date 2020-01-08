'''
Created on Jun 26, 2016

@author: matar
'''
import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/" #The web service root URL
ARTIIST_URL = BASE_URL+"artist/"

#    We have 11 resources on our web service which represent core entities in our database
#       area, artist, event, instrument, label, recording, release, release-group, series, work, url

# query Parametes are given to request.get() functions as dictionary {}; this Variable contains some starter parameters
query_type = { "simple" : {},
                "art" : {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}
               }


def query_site(url, params, uid="", fmt="json"):
    # main function to make queries to Musicbrainz api
    # A json Document should be returned
    params["fmt"] = fmt
    r = requests.get(url + uid, params = params)
    print("requesting", r.url)
    
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # add artist name to params to query_site() function before calling api
    params["query"] = "artist:"+name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)

def main():
    results = query_by_name(ARTIIST_URL, query_type["simple"], "Nirvana")
    pretty_print(results)
    
    artist_id = results["artists"][1]["id"]
    print("\nArtist")
    pretty_print(results["artists"][1])
    
    
    artist_date = query_site(ARTIIST_URL, query_type["releases"], artist_id)
    releases = artist_date["releases"]
    #print("\nONE RELEASE:")
    #pretty_print(releases[0])
    
    release_titles = [r["title"] for r in releases]
    print("\nAll Titles")
    for t in release_titles:
        print(t)
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
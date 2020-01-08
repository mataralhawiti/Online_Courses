

'''
Created on Jun 26, 2016

@author: matar
'''


# To experiment with this code freely you will have to run this code locally.
# Take a look at the main() function for an example of how to use the code.
# We have provided example json output in the other code editor tabs for you to
# look at, but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    '''
    Modify the function calls and indexing below to answer the questions on
    the next quiz. HINT: Note how the output we get from the site is a
    multi-level JSON document, so try making print statements to step through
    the structure one level at a time or copy the output to a separate output
    file.
    '''
    results_Direction = query_by_name(ARTIST_URL, query_type["simple"], "One Direction ")
    pretty_print(results_Direction)

    artist_id_Dir = results_Direction["artists"][0]["id"]
    #print("\nARTIST:")
    #pretty_print(results_Direction["artists"][0])
    
    one_direction_data = results_Direction["artists"][0]
    print("\nOne Direction was formed in :")
    print(one_direction_data["life-span"]["begin"])
    print("\n")
    
    print("#------------------------------------------------------- ")

    #-------------------------------------------------------
    #-------------------------------------------------------
    results_Kit = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    #pretty_print(results_Kit)
    kit_data = results_Kit["artists"] # list
    count = 0
    for name in kit_data:
        if name["name"] == "First Aid Kit" :
            count += 1
    
    print("\nFirst Aid Kit count :")
    print(count)
#     artist_id_Kit = results_Direction["artists"][0]["id"]
#     print("\nARTIST:..............")
#     pretty_print(results_Kit["artists"])
#     Kit_data = results_Direction["artists"][0]
#     print("\nOne Direction was formed in :")
    #print(Kit_data["life-span"]["begin"])
    
    #-------------------------------------------------------
    #-------------------------------------------------------
    print("#------------------------------------------------------- ")
    #-------------------------------------------------------"

    result_alias = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    #pretty_print(result_alias)
    
    beatles_id = result_alias["artists"][0]["id"]
    #print(beatles_id)
    
    beatles_data = query_site(ARTIST_URL, query_type["aliases"], beatles_id)
    
    #pretty_print(beatles_data)
    
    
    for ali in beatles_data["aliases"]:
        if ali["locale"] == "es":
            print("\nBeatles ali in espaniol :")
            print(ali["name"])

    print("#------------------------------------------------------- ")

    #-------------------------------------------------------
    #-------------------------------------------------------

    Queen = query_by_name(ARTIST_URL, query_type["simple"], "Queen_")
    
    #pretty_print(Queen)
    
    begin_area_Queen = None
    for art in Queen["artists"] :
        if "name" and "type" and "begin-area" in art :
            if art["name"] == "Queen" and art["type"] == "Group" :
                begin_area_Queen = art["begin-area"]["name"]
            else:
                pass
        else:
            pass
    
    print("\nQueen begin area :")
    print(begin_area_Queen)
    
    print("#------------------------------------------------------- ")

    
    
    #-------------------------------------------------------
    #-------------------------------------------------------

    Nirvana = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    #pretty_print(Nirvana)
    
    Nirvana_disambiguation = None
    
    for nir in Nirvana["artists"]:
        if "tags" in nir:
            for tag in nir["tags"]:
                if tag["name"] == "kurt cobain" :
                    Nirvana_disambiguation = nir["disambiguation"]
                else:
                    pass
        else:
            pass
    
    print("\nNirvana disambiguation")
    print(Nirvana_disambiguation)
            
        








#   artist_data = query_site(ARTIST_URL, query_type["simple"], artist_id)
#    pretty_print(artist_data)
#     releases = artist_data["releases"]
#     print("\nONE RELEASE:")
#     pretty_print(releases[0], indent=2)
#     release_titles = [r["title"] for r in releases]
# 
#     print("\nALL TITLES:")
#     for t in release_titles:
#         print(t)


if __name__ == '__main__':
    main()

import requests
import json

def find_cafes_within(lat, lon, radius): 
    overpass_query = '''
        [out:json][timeout:25];
        // gather results
        (
        // query part for: “cafe”
        node(around:%s,%s,%s)["amenity"="cafe"];
        relation(around:%s,%s,%s)["amenity"="cafe"];
        );
        // print results
        out body;
        >;
        out skel qt;    
        ''' % (float(radius), lat, lon, float(radius), lat, lon)

    overpass_interpreter_url = "https://overpass-api.de/api/interpreter"
    response = requests.post(overpass_interpreter_url, data=overpass_query)

    if response.status_code == 200:
        data = response.json()
        return data['elements']

    else:
        raise Exception("Something went wrong during Overpass query.")
        

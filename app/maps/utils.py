from shapely.geometry import Point  
from app.maps.overpass import Overpass

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

    overpass_result = Overpass.query(overpass_query)

    return overpass_result["elements"]

def find_pedestrian_roads_within(lat, lon, radius):
    overpass_query = '''
        [out:json][timeout:25];
        (
        way(around:%s, %s, %s)["highway"="footway"];
        way(around:%s, %s, %s)["highway"="path"];
        way(around:%s, %s, %s)["highway"="pedestrian"];
        );
        out body;
        >;
        out skel qt;
    ''' % (float(radius), lat, lon, float(radius), lat, lon, float(radius), lat, lon)

    overpass_result = Overpass.query(overpass_query)

    return overpass_result['elements']

def get_meeting_location(lat, lon) -> dict:
    cafe_list = find_cafes_within(lat, lon, 200)
    nearest_cafe = get_nearest_cafe_or_none(lat, lon, cafe_list)
    
    if nearest_cafe is not None:
        return cafe
    
    fallback_meeting_place = find_pedestrian_roads_within(lat, lon, 200)

    return {} 

def get_nearest_cafe_or_none(lat, lon, cafe_list) -> dict | None:    
    if len(cafe_list) == 0:
        return None

    point_between_people = Point(lat, lon)

    closest_cafe = cafe_list[0]
    distance_to_closest_cafe = Point(closest_cafe['lat'], closest_cafe['lon']).distance(point_between_people)

    for cafe in cafe_list:
        distance_to_current_cafe = Point(cafe['lat'], cafe['lon']).distance(point_between_people)
        
        if distance_to_closest_cafe > distance_to_current_cafe:
            # print(f"{cafe['tags']['name']} is closer than {closest_cafe['tags']['name']} difference in distance is {distance_to_closest_cafe - distance_to_current_cafe}")
            closest_cafe = cafe
            distance_to_closest_cafe = distance_to_current_cafe

    return closest_cafe

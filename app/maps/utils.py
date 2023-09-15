from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
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
        out ids geom;
        >;
    ''' % (float(radius), lat, lon, float(radius), lat, lon, float(radius), lat, lon)

    overpass_result = Overpass.query(overpass_query)

    return overpass_result['elements']

def get_meeting_location(lat, lon) -> dict:
    cafe_list = find_cafes_within(lat, lon, 200)
    nearest_cafe = get_nearest_cafe_or_none(lat, lon, cafe_list)
    
    if nearest_cafe is not None:
        return nearest_cafe
    
    pedestrian_fallback_roads = find_pedestrian_roads_within(lat, lon, 200)
    nearest_pedestrian_road = get_nearest_pedestrian_road(lat, lon, pedestrian_fallback_roads)

        
    return {'lat': nearest_pedestrian_road.x, 'lon': nearest_pedestrian_road.y}

def get_nearest_pedestrian_road(lat, lon, pedestrian_roads_list) -> Point | None:
    if len(pedestrian_roads_list) == 0:
        return None

    main_point = Point(lat, lon)

    ways_as_linestring = []

    for element in pedestrian_roads_list:
        points = []
        for element_lat_lon in element['geometry']:
            points.append((element_lat_lon['lat'], element_lat_lon['lon'],))

        ways_as_linestring.append(LineString(points))

    closest_point, _ = nearest_points(ways_as_linestring[0], main_point)

    for way in ways_as_linestring:
        temp_point, _ = nearest_points(way, main_point)
        
        if temp_point.distance(main_point) < closest_point.distance(main_point):
            closest_point = temp_point
        
    return closest_point 


def get_nearest_cafe_or_none(lat, lon, cafe_list) -> dict | None:    
    if len(cafe_list) == 0:
        return None

    main_point = Point(lat, lon)

    closest_cafe = cafe_list[0]
    distance_to_closest_cafe = Point(closest_cafe['lat'], closest_cafe['lon']).distance(main_point)

    for cafe in cafe_list:
        distance_to_current_cafe = Point(cafe['lat'], cafe['lon']).distance(main_point)
        
        if distance_to_closest_cafe > distance_to_current_cafe:
            # print(f"{cafe['tags']['name']} is closer than {closest_cafe['tags']['name']} difference in distance is {distance_to_closest_cafe - distance_to_current_cafe}")
            closest_cafe = cafe
            distance_to_closest_cafe = distance_to_current_cafe

    return closest_cafe

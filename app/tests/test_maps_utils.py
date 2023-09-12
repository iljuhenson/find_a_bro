from app.maps import utils
from shapely.geometry import Point

def test_find_cafes_within():

    assert 6 == len(utils.find_cafes_within(52.229785, 20.973891, 500))
    assert 0 == len(utils.find_cafes_within(52.229785, 20.973891, 1))

def test_get_nearest_cafe_or_none():
    cafe_list = utils.find_cafes_within(52.229785, 20.973891, 500)
    assert utils.get_nearest_cafe_or_none(52.229785, 20.973891, cafe_list)['id'] == 5379085437

    modified_cafe_list = [cafe for cafe in cafe_list if cafe['id'] != 5379085437]
    assert utils.get_nearest_cafe_or_none(52.229785, 20.973891, modified_cafe_list)['id'] == 9972944145

    assert utils.get_nearest_cafe_or_none(52.229785, 20.973891, []) is None

def test_find_pedestrian_roads_within():
    roads: list = utils.find_pedestrian_roads_within(52.229785, 20.973891, 100)

    way_counter = 0
    node_counter = 0
    for element in roads:
        if element['type'] == 'way':
            way_counter += 1
        if element['type'] == 'node':
            node_counter += 1

    assert node_counter == 155 
    assert way_counter == 21 

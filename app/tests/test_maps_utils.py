from app.maps import utils

def test_find_cafes_within():
    
    assert 6 == len(utils.find_cafes_within(52.229785, 20.973891, 500))
    assert 0 == len(utils.find_cafes_within(52.229785, 20.973891, 1))

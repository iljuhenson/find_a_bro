import requests


class Overpass:
    _interpreter_url = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
    
    @classmethod
    def query(cls, query_string):
        response = requests.post(cls._interpreter_url, data=query_string)

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            raise Exception("Something went wrong during Overpass query.")

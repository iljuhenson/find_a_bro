import requests


class Overpass:
    _interpreter_url = "https://overpass-api.de/api/interpreter"
    
    @classmethod
    def query(cls, query):
        response = requests.post(cls._interpreter_url, data=query)

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            raise Exception("Something went wrong during Overpass query.")

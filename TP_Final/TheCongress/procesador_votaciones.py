import os
import json
from time import sleep
import requests
import responses
from the_congress import TheCongress


class ProcesadorDeVotaciones:
    """Le pasamos anios para las cuales busca votaciones y el nombre de la carpeta donde las pone"""

    HEADERS = {'X-API-KEY': '8BVo6M72OP7w7F9sXFjg'}

    def __init__(self, begin, end, folder):
        self.begin = begin
        self.end = end
        self.folder = folder #data
        self.headers = ProcesadorDeVotaciones.HEADERS
        self._create_folder()


    def _create_folder(self):
        if not os.path.isdir(f'{self.folder}'):
            os.mkdir(f'{self.folder}')

    def procesar(self):
      congress = TheCongress()
      for year in range(self.begin, self.end + 1):
          for month in range(1, 12):
              voting_list = self._get_vote(year, month)
              for vote_json in voting_list:
                  congress.add_votes(vote_json, year, month)
      return congress

    def _get_vote(self, year, month):
       path = f'{self.folder}/{year}/{month}'
       if os.path.isdir(path):
           print(f'Loading from {path}')
           data = []
           files = os.listdir(path)
           for file in files:
               with open(f'{path}/{file}') as json_file:
                   data.append(json.load(json_file))
           return data

       else:
           os.makedirs(path)
           print(f'Getting {path} from API')
           if month != 12:
               url = f'https://api.hcdn.gob.ar/votaciones/api/v1/votaciones/busqueda?desde={year}-{month}-1T00%3A00%3A00Z&hasta={year}-{month + 1}-1T00%3A00%3A00Z'
           else:
               url = f'https://api.hcdn.gob.ar/votaciones/api/v1/votaciones/busqueda?desde={year}-{month}-1T00%3A00%3A00Z&hasta={year}-{month}-31T00%3A00%3A00Z'
           sleep(1) #no sobrecargar la API
           answer = requests.get(url, headers = self.headers)
           #code = answer.status_code
           #if code != 200:
               #print(answer)
           vote_list = answer.json()
           data = []
           for vote in vote_list:
               vote_id = vote['id']
               url = f'https://api.hcdn.gob.ar/votaciones/api/v1/votacion/{vote_id}'
               sleep(1)
               response = requests.get(url, headers = self.headers).json()
               with open(f'{path}/{vote_id}.json', 'w') as json_file:
                   json.dump(response, json_file)
               data.append(response)
           return data

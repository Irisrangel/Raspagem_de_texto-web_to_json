import json
import os
import requests
from bs4 import BeautifulSoup

# Link de origem
BASE_URL = "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/pronunciamentos/pronunciamentos-do-presidente-da-republica"
# Pasta de destino para salvar os pronunciamentos em Json
DATA_DIR = "pronunciamentos"

response = requests.get(BASE_URL)

bs = BeautifulSoup(response.text)

articles = bs.find_all("article")

class Pronouncement:
  def __init__(self, bs_article=None):

    if bs_article is not None:
      self.url = bs_article.find(class_="summary url")["href"]
      self.tags = [t.text for t in bs_article.find_all(rel="tag")]
      
      datetime = bs_article.find_all(class_="summary-view-icon")
      self.date = canonical_date(datetime[0].text.strip())
      self.time = time = datetime[1].text.strip()
    
      self.text = self._extract_text()

  def _extract_text(self):
    r = requests.get(self.url)
    bs = BeautifulSoup(r.text)
    return bs.find(id="parent-fieldname-text").text.strip()

  def save_tojson(p, savedir, name=None):
    if name is None:
      name = f"{p.date}-{p.time}.json"
    path = os.path.join(savedir, name)
    with open(path, "w") as jsonfile:
      json.dump(p.__dict__, jsonfile)    

  def load_fromjson(filepath):
    with open(filepath, "r") as jsonfile:
      data = json.load(jsonfile)
      p = Pronouncement()
      p.date = data["date"]
      p.time = data["time"]
      p.tags = data["tags"]
      p.url = data["url"]
      p.text = data["text"]
      return p

def main():
    pronouncements = [Pronouncement(art) for art in articles]

    # Salvando os pronuncimaneto em Json
    for p in pronouncements:
        Pronouncement.save_tojson(p, DATA_DIR)

    # Recuperando os dados salvos em Json
    filenames = os.listdir(DATA_DIR)

    pronunciamentos = []
    for name in filenames:
        path = os.path.join(DATA_DIR, name)
        pronunciamentos.append(Pronouncement.load_fromjson(path))

    for i in range(2, 8, 2):
        print("Num:", i)
        print(pronunciamentos[i].text)
        print("===========================")

if __name__ == "__main__":
   sys.exit(main()) 

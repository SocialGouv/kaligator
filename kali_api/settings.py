import os

MONGO_URI = os.environ["MONGODB_URI"]
MONGO_AUTH_SOURCE = "admin"
MONGO_DBNAME = 'kali'
DOMAIN = {
  'article': {},
  'section_ta': {},
  'texte': {},
  'conteneur': {},
}
ALLOW_UNKNOWN = True

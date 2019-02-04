import os

MONGO_URI = os.environ["MONGODB_URI"]
MONGO_AUTH_SOURCE = "admin"
MONGO_DBNAME = 'kali'
DOMAIN = {
  'articles': {},
  'section_tas': {},
  'textes': {},
  'conteneurs': {},
}
ALLOW_UNKNOWN = True

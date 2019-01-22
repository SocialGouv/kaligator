import collections
from lxml import html
import requests

link = "https://www.legifrance.gouv.fr/initRechConvColl.do"
response = requests.get(link)
html_element = html.document_fromstring(response.content)
idcc_options = html_element.xpath("//*[@id='champ1']/option")

kalicont_ids = [o.get("value").split("#")[0] for o in idcc_options]

duplicate_kalicont_ids = [kid for kid, count in collections.Counter(kalicont_ids).items() if count > 1]

for duplicate_kalicont_id in duplicate_kalicont_ids:
    print("list of duplicates for %s" % duplicate_kalicont_id)
    for option in idcc_options:
        if option.get("value").split("#")[0] == duplicate_kalicont_id:
            print("%s || points to %s" % (option.text.strip(), option.get("value")))
    print("")

# => this LEGIFRANCE home list feels quite messy, i don't think it's worth going any further

# list of duplicates for KALICONT000019074623
# Guides et accompagnateurs en milieu amazonien du 12 mai 2007 || points to KALICONT000019074623#KALITEXT000019074628
# Travail des guides d'expédition, guides accompagnateurs et guides animateurs en milieu amazonien ... || points to KALICONT000019074623#KALITEXT000024146455

# list of duplicates for KALICONT000019765628
# Magasins prestataires de services de cuisine à usage domestique du 17 juillet 2008 || points to KALICONT000019765628#KALITEXT000019942821
# Magasins prestataires de services de cuisine à usage domestique du  17 juillet 2008 || points to KALICONT000019765628#KALITEXT000005687127


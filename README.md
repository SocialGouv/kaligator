# KALI Dumps scripts

This collection of scripts helps using KALI dumps (the French Conventions collectives nationales database).

These scripts were created for the [Code Du Travail Numérique](https://incubateur.social.gouv.fr/startups/code-du-travail-numerique/) project.

You can see an example of a Convention Collective on Legifrance [here](https://www.legifrance.gouv.fr/affichIDCC.do;jsessionid=345B979AD534CB99791356E28B8A9CB0.tplgfr35s_1?idSectionTA=KALISCTA000005733781&cidTexte=KALITEXT000005639851&idConvention=KALICONT000005635890)

## Schema docs

You can find some work-in-progress docs on a [Google Spreadsheet here](https://github.com/SocialGouv/kali_dumps_scripts.git).

![docs screenshot](https://i.imgur.com/8XgOmhL.png)

The infos in this documentation come from:
- the DTD files available on Data Gouv
- exploring the MongoDB database that these scripts help create. The M3T tool is very helpful for this.

## Download source data dumps

You can find the original source KALI dumps on Data Gouv :
[https://www.data.gouv.fr/fr/datasets/kali-conventions-collectives-nationales/](https://www.data.gouv.fr/fr/datasets/kali-conventions-collectives-nationales/)

You should then extract the archive.

## Local setup

You need to install some light dependencies for the script :

```sh
mkvirtualenv cdtn-scripts
pip3 install -r requirements.txt
```

## Usage

```sh
python3 convert_xml_to_json.py --mode mongodb /Users/jean/Downloads/kali_dump
```

you can use `python3 convert_xml_to_json.py -h` to get more info on the accepted arguments

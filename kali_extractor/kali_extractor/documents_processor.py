from xml.etree import ElementTree
import html
from kali_extractor.custom_xml_parser import custom_xml_parser
from kali_extractor.dict_utils import deep_get, deep_set
from xmljson import abdera


class DocumentProcessor(object):
    def __init__(
        self, xml_path, html_fields=None, array_fields=None, **kwargs
    ):
        self.xml_path = xml_path
        self.html_fields = [] if html_fields is None else html_fields
        self.array_fields = [] if array_fields is None else array_fields

    def parse_xml(self):
        """
            reads and parses the XML into a json-formatted dictionary object.
            drops the root tag (<ARTICLE>, <IDCC> ...)
        """
        with open(self.xml_path, "r") as f:
            element = ElementTree.parse(f)
        self.root = element.getroot()
        parsed_root = custom_xml_parser.data(self.root)
        root_keys = list(parsed_root.keys())
        if len(root_keys) > 1:
            raise Exception(
                "parsed XML has more than one element at the root level: %s" %
                ",".join(root_keys)
            )
        self.json = parsed_root[root_keys[0]]

    def format_array_fields(self):
        """
            Enforce some fields to always be arrays, even with a single entry.
            By default, you get a mixed schema, with single items as objects,
            and multiple items as arrays
        """
        for field in self.array_fields:
            for value, selector in deep_get(self.json, field):
                if value is not None and not isinstance(value, list):
                    deep_set(self.json, selector, [value])

    def format_html_fields(self):
        """
            Enforce some fields to contain their content as unformatted HTML.
            By default, all the fields are parsed and split into objects but
            we want to treat HTML content as raw text.
        """
        for field in self.html_fields:
            xpath_selector = "./%s" % "/".join(field.split("."))
            value = self.root.find(xpath_selector)
            if value is None:
                continue
            sub_strings = [
                ElementTree.tostring(sub_element).decode("utf-8")
                for sub_element in value
            ]
            parsed_contenu_html = html.unescape("".join(sub_strings))
            deep_set(self.json, field, parsed_contenu_html)

    def process(self):
        self.parse_xml()
        self.format_html_fields()
        self.format_array_fields()
        return self.json


class ArticleProcessor(DocumentProcessor):
    def __init__(self, xml_path, **kwargs):
        super(ArticleProcessor, self).__init__(
            xml_path,
            html_fields=["BLOC_TEXTUEL/CONTENU", "NOTA/CONTENU"],
            array_fields=["VERSIONS/VERSION", "LIENS/LIEN"],
            **kwargs
        )


class IDCCProcessor(DocumentProcessor):
    def __init__(self, xml_path, **kwargs):
        super(IDCCProcessor, self).__init__(
            xml_path,
            html_fields=[],
            array_fields=[
                "STRUCTURE_TXT/TM", "ACTS_PRO/ACT_PRO",
                "NUMS_BROCH/NUM_BROCH", "STRUCTURE_TXT/TM/LIEN_TXT"
            ],
            **kwargs
        )


class SectionTaProcessor(DocumentProcessor):
    def __init__(self, xml_path, **kwargs):
        super(SectionTaProcessor, self).__init__(
            xml_path,
            html_fields=[],
            array_fields=[
                "STRUCTURE_TA/LIEN_ART", "STRUCTURE_TA/LIEN_SECTION_TA",
                "CONTEXTE/TEXTE/TITRE_TXT", "CONTEXTE/TEXTE/TM/TITRE_TM"
            ],
            **kwargs
        )


def flatten_abdera_item(item):
    """
        takes a dict parsed by the abdera algorithm and returns one
        that is formatted like a custom one
    """
    keys = list(item.keys())
    if len(keys) != 1:
        raise Exception("found %s abdera tag names instead of 1" % len(keys))
    key = keys[0]
    abdera_obj = item[key]
    new_object = {}
    for name, value in abdera_obj.get("attributes").items():
        new_object[name] = value
    if "children" in abdera_obj:
        if not isinstance(abdera_obj["children"], list):
            raise Exception(
                "children should be a list but was a %s" %
                abdera_obj["children"].__class__
            )
        if len(abdera_obj["children"]) != 1:
            raise Exception(
                "children should contain a single item but has %s" %
                len(abdera_obj["children"])
            )
        new_object["_text"] = abdera_obj["children"][0]
    return {key: new_object}


class TexteProcessor(DocumentProcessor):
    def __init__(self, xml_path, **kwargs):
        super(TexteProcessor, self).__init__(
            xml_path,
            html_fields=[],
            array_fields=["VERSIONS/VERSION"],
            **kwargs
        )

    def parse_xml(self):
        """
            slightly hacky, this fixes #6, as the STRUCT contains a mixed
            list of two different tags, we cannot treat it as the array fields
        """
        super(TexteProcessor, self).parse_xml()
        if 'STRUCT' not in self.json:
            return
        doc = abdera.data(self.root)
        subdocs = [
            d for d in doc["TEXTEKALI"]["children"]
            if ["STRUCT"] == list(d.keys())
        ]
        if len(subdocs) != 1:
            raise Exception(
                "found %s STRUCT tags in TEXTEKALI instead of 1" % len(subdocs)
            )
        if not subdocs[0]["STRUCT"].get("children"):
            return
        children = subdocs[0]["STRUCT"]["children"]
        flat_children = [flatten_abdera_item(c) for c in children]
        self.json["STRUCT"] = flat_children

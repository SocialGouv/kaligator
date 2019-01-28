from xml.etree import ElementTree
import html
from custom_xml_parser import custom_xml_parser
from dict_utils import deep_get, deep_set


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


class TexteProcessor(DocumentProcessor):
    def __init__(self, xml_path, **kwargs):
        super(TexteProcessor, self).__init__(
            xml_path,
            html_fields=[],
            array_fields=[
                "STRUCT/LIEN_SECTION_TA", "STRUCT/LIEN_ART", "VERSIONS/VERSION"
            ],
            **kwargs
        )

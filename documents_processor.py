from xml.etree import ElementTree
import html
from custom_xml_parser import custom_xml_parser
from dict_utils import deep_get, deep_set


class DocumentProcessor(object):
    def __init__(self, xml_path, html_fields=None, array_fields=None, **kwargs):
        self.xml_path = xml_path
        self.html_fields = [] if html_fields is None else html_fields
        self.array_fields = [] if array_fields is None else array_fields

    def parse_xml(self):
        with open(self.xml_path, "r") as f:
            element = ElementTree.parse(f)
        self.root = element.getroot()
        self.json = custom_xml_parser.data(self.root)["ARTICLE"]

    def format_array_fields(self):
        for field in self.array_fields:
            value = deep_get(self.json, field)
            if value is not None and not isinstance(value, list):
                deep_set(self.json, field, [value])

    def format_html_fields(self):
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
            html_fields=["BLOC_TEXTUEL.CONTENU", "NOTA.CONTENU"],
            array_fields=["VERSIONS.VERSION", "LIENS.LIEN"],
            **kwargs
        )

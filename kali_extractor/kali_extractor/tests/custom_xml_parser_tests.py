import unittest
import os
from kali_extractor.custom_xml_parser import CustomXmlParser
from xml.etree import ElementTree

dirname = os.path.dirname(__file__)
xml_path = os.path.join(dirname, 'fixtures/KALITEXT_STRUCT_1.xml')


class CustomXmlParserTests(unittest.TestCase):

    def test_2099_parsing(self):
        with open(xml_path, "r") as f:
            element = ElementTree.parse(f)
        root = element.getroot()
        parsed = CustomXmlParser().data(root)
        self.assertEqual(
            parsed["TEXTEKALI"]["VERSIONS"]["VERSION"]["LIEN_TXT"]["fin"],
            None
        )

    def test_empty_tags(self):
        with open(xml_path, "r") as f:
            element = ElementTree.parse(f)
        root = element.getroot()
        parsed = CustomXmlParser().data(root)
        meta = parsed["TEXTEKALI"]["META"]["META_SPEC"]["META_TEXTE_CHRONICLE"]
        self.assertEqual(
            meta["PAGE_DEB_PUBLI"],
            None
        )

    def test_numerical_text(self):
        with open(xml_path, "r") as f:
            element = ElementTree.parse(f)
        root = element.getroot()
        parsed = CustomXmlParser().data(root)
        meta = parsed["TEXTEKALI"]["META"]["META_SPEC"]["META_TEXTE_CHRONICLE"]
        self.assertEqual(
            meta["NUM_SEQUENCE"],
            "13"  # should not be parsed to int
        )

    def test_numerical_attribute(self):
        with open(xml_path, "r") as f:
            element = ElementTree.parse(f)
        root = element.getroot()
        parsed = CustomXmlParser().data(root)
        self.assertEqual(
            parsed["TEXTEKALI"]["VERSIONS"]["VERSION"]["LIEN_TXT"]["num"],
            "31"  # should not be parsed to int
        )

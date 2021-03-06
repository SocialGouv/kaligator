import unittest
import os
from kali_extractor.documents_processor import \
    flatten_abdera_item, TexteStructProcessor

dirname = os.path.dirname(__file__)


class TexteStructProcessorTests(unittest.TestCase):

    maxDiff = None

    def test_flatten_abdera(self):
        self.assertEqual(
            flatten_abdera_item(
                {
                    'TAG_NAME': {
                        'attributes': {
                            'att1': 'val1',
                            'att2': 'val2'
                        },
                        'children': ['Blah']
                    }
                }
            ),
            {
                '_type': "TAG_NAME",
                'att1': 'val1',
                'att2': 'val2',
                '_text': 'Blah'
            }
        )

    def test_struct_1(self):
        filename = os.path.join(dirname, 'fixtures/KALITEXT_STRUCT_1.xml')
        parsed = TexteStructProcessor(filename).process()
        self.assertEqual(
            parsed["STRUCT"],
            [
                {
                    "_type": "LIEN_SECTION_TA",
                    "cid": "KALISCTA000032593516",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALISCTA000032593516",
                    "niv": "1",
                    "url": "/KALI/SCTA/00/00/32/59/35/KALISCTA000032593516.xml",  # noqa: E501
                    "_text": "Pr\u00e9ambule"
                },
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032593517",
                    "num": "1er",
                    "origine": "KALI"
                },
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032593518",
                    "num": "2",
                    "origine": "KALI"
                },
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032593522",
                    "num": "3",
                    "origine": "KALI"
                },
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032593523",
                    "num": "4",
                    "origine": "KALI"
                },
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032593524",
                    "num": "5",
                    "origine": "KALI"
                },
                {
                    "_type": "LIEN_SECTION_TA",
                    "cid": "KALISCTA000032593525",
                    "debut": "2016-06-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALISCTA000032593525",
                    "niv": "1",
                    "url": "/KALI/SCTA/00/00/32/59/35/KALISCTA000032593525.xml",  # noqa: E501
                    "_text": "Annexe I"
                }
            ]
        )

    def test_struct_2(self):
        filename = os.path.join(dirname, 'fixtures/KALITEXT_STRUCT_2.xml')
        parsed = TexteStructProcessor(filename).process()
        self.assertEqual(
            parsed["STRUCT"],
            [
                {
                    "_type": "LIEN_ART",
                    "debut": "2016-09-01",
                    "etat": "VIGUEUR_ETEN",
                    "fin": None,
                    "id": "KALIARTI000032611648",
                    "num": None,
                    "origine": "KALI"
                }
            ]
        )


if __name__ == '__main__':
    unittest.main()

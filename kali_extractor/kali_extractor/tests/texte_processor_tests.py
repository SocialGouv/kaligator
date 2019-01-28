import unittest
import os
from kali_extractor.documents_processor import \
    flatten_abdera_item, TexteProcessor

dirname = os.path.dirname(__file__)


class TexteProcessorTests(unittest.TestCase):

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
                'TAG_NAME': {
                    'att1': 'val1',
                    'att2': 'val2',
                    '_text': 'Blah'
                }
            }
        )

    def test_struct_1(self):
        filename = os.path.join(dirname, 'fixtures/KALITEXT_STRUCT_1.xml')
        parsed = TexteProcessor(filename).process()
        self.assertEqual(
            parsed["STRUCT"],
            [
                {
                    "LIEN_SECTION_TA": {
                        "cid": "KALISCTA000032593516",
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALISCTA000032593516",
                        "niv": 1,
                        "url": "/KALI/SCTA/00/00/32/59/35/KALISCTA000032593516.xml",  # noqa: E501
                        "_text": "Pr\u00e9ambule"
                    },
                },
                {
                    "LIEN_ART": {
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALIARTI000032593517",
                        "num": "1er",
                        "origine": "KALI"
                    },
                },
                {
                    "LIEN_ART": {
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALIARTI000032593518",
                        "num": 2,
                        "origine": "KALI"
                    },
                },
                {
                    "LIEN_ART": {
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALIARTI000032593522",
                        "num": 3,
                        "origine": "KALI"
                    },
                },
                {
                    "LIEN_ART": {
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALIARTI000032593523",
                        "num": 4,
                        "origine": "KALI"
                    },
                },
                {
                    "LIEN_ART": {
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALIARTI000032593524",
                        "num": 5,
                        "origine": "KALI"
                    },
                },
                {
                    "LIEN_SECTION_TA": {
                        "cid": "KALISCTA000032593525",
                        "debut": "2016-06-01",
                        "etat": "VIGUEUR_ETEN",
                        "fin": "2999-01-01",
                        "id": "KALISCTA000032593525",
                        "niv": 1,
                        "url": "/KALI/SCTA/00/00/32/59/35/KALISCTA000032593525.xml",  # noqa: E501
                        "_text": "Annexe I"
                    }
                }
            ]
        )


if __name__ == '__main__':
    unittest.main()

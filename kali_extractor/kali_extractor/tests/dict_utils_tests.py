import unittest
from kali_extractor.dict_utils import deep_get, deep_set, xpath_to_keys

SOME_OBJ = {
    'first': {
        'easy': {
            'peasy': 10,
            'nested': [1, 2, 3]
        }
    },
    'less_easy': {
        'nasty': [
            {
                'sub_1': 'abc'
            },
            {
                'sub_1': 'def'
            },
            {
                'nope': 'sh'
            },
            {
                'sub_1': None
            }
        ]
    }
}


class DictUtilsTests(unittest.TestCase):

    def test_deep_get_easy(self):
        self.assertEqual(
            list(deep_get(SOME_OBJ, '/first/easy')),
            [(
                {
                    'peasy': 10,
                    'nested': [1, 2, 3]
                },
                '/first/easy'
            )]
        )

    def test_deep_get_peasy(self):
        self.assertEqual(
            list(deep_get(SOME_OBJ, '/first/easy/peasy')),
            [(10, '/first/easy/peasy')]
        )

    def test_deep_get_nested(self):
        self.assertEqual(
            list(deep_get(SOME_OBJ, '/first/easy/nested')),
            [([1, 2, 3], '/first/easy/nested')]
        )

    def test_deep_get_less_easy(self):
        self.assertEqual(
            list(deep_get(SOME_OBJ, '/less_easy/nasty/sub_1')),
            [
                ('abc', '/less_easy/nasty[0]/sub_1'),
                ('def', '/less_easy/nasty[1]/sub_1'),
                (None, '/less_easy/nasty[3]/sub_1')
            ]
        )

    def test_deep_get_nonexisting(self):
        self.assertEqual(
            list(deep_get(SOME_OBJ, '/not/at/all')),
            []
        )

    def test_deep_set_1(self):
        d = {"par": {"child": 'value'}}
        deep_set(d, '/par/child', 'new_value')
        self.assertEqual(d, {"par": {"child": "new_value"}})

    def test_deep_set_2(self):
        d = {"par": [{"child": 'val1'}, {"child": "val2"}]}
        deep_set(d, '/par[1]/child', 'new_value')
        self.assertEqual(
            d, {"par": [{"child": 'val1'}, {"child": "new_value"}]}
        )

    def test_xpath_to_keys_1(self):
        self.assertEqual(
            xpath_to_keys('/test/thing/chop'),
            ['test', 'thing', 'chop']
        )

    def test_xpath_to_keys_2(self):
        self.assertEqual(
            xpath_to_keys('/test/thing[201]/chop'),
            ['test', 'thing', 201, 'chop']
        )


if __name__ == '__main__':
    unittest.main()

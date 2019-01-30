from xmljson import XMLData, Abdera
# from xmljson import parker as custom_xml_parser
from collections import OrderedDict


def custom_from_string(value):
    if value == "" or value == '2999-01-01':
        return None
    return value


class CustomXmlParser(XMLData):
    '''
    Converts between XML and json using a custom convention.
    - simple tags only with text content will be parsed to:
      {tag_name: "some content"}
    - a more complex tag with attributes and text will be parsed to:
      {tag_name: {attr1: "val1", attr2: "val2", _text: "some content"}}
    - no type casting will be done, everything will be parsed to strings
    - empty tags will be parsed to {tag_name: null}
    - attributes with empty string values will be parsed to null:
      {tag_name: {attr1: null}}
    - attributes with string value "2999-01-01" will be parsed to null:
      {tag_name: {attr1: null}}
    '''
    @staticmethod
    def _fromstring(value):
        return custom_from_string(value)

    def __init__(self, **kwargs):
        # kwargs.setdefault('xml_fromstring', False)
        super(CustomXmlParser, self).__init__(
            text_content='_text', simple_text=True, **kwargs
        )

    def data(self, root):
        '''Convert etree.Element into a dictionary, empty dicts become null'''
        res = super(CustomXmlParser, self).data(root)
        if len(res) == 1:
            key, value = list(res.items())[0]
            if isinstance(value, OrderedDict) and len(value) == 0:
                res[key] = None
        return res


class CustomAbderaParser(Abdera):
    @staticmethod
    def _fromstring(value):
        return custom_from_string(value)


custom_abdera_parser = CustomAbderaParser()
custom_xml_parser = CustomXmlParser()

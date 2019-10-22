import unittest
import lxml
from iso_template import (get_alternate_text_wrapper,
                          pretty_xml,
                          get_instruments_from_record)


class TestISOTemplateFunctions(unittest.TestCase):

    def test_get_alternate_text_wrapper(self):

        # get_alternate_text_wrapper
        record = {"language": "eng",
                  "title": "title in english",
                  "title_fra": "title in french"}

        get_alternate_text = get_alternate_text_wrapper(record)

        out = get_alternate_text('title')
        self.assertEqual([('fra', 'title in french')], out)

    def test_get_alternate_text_no_language(self):
        # error: missing language
        record = {"title": "title in english"}
        self.assertRaises(Exception, get_alternate_text_wrapper, record)

    def test_get_alternate_text_bad_key(self):
        # error: there is an alternate language set to the default language
        record = {"language": "eng",
                  "title_eng": "title in english"}
        get_alternate_text = get_alternate_text_wrapper(record)
        self.assertRaises(Exception, get_alternate_text, 'title')

    def test_pretty_xml(self):
        self.assertEqual(
            '<?xml version="1.0" encoding="utf-8"?>\n<xml>sdf</xml>\n',
            pretty_xml('<xml>sdf</xml>'))
        # check that bad xml throws an error
        self.assertRaises(lxml.etree.XMLSyntaxError, pretty_xml,
                          '<xml>sdf</xml')

    def test_get_instruments_from_record(self):
        record = {
            "instrument_2_id": "instrument_2_id",
            "instrument_2_sensor_1_id": "sensor_id",
        }
        self.assertEqual({
            '2': {
                'id': 'instrument_2_id',
                'sensor': {
                    '1': {
                        'id': 'sensor_id'
                    }
                }
            }
        }, get_instruments_from_record(record))


if __name__ == '__main__':
    unittest.main()

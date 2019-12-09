#!/usr/bin/env python3

import unittest
import lxml
from iso_template import (get_alternate_text_wrapper,
                          pretty_xml,
                          get_instruments_from_record,
                          iso_template,
                          sanitize_record
                          )

from validation import (list_intersection,
                        check_date,
                        get_alternate_language,
                        get_missing_fields,
                        has_eov_in_keywords)


class TestISOTemplateFunctions(unittest.TestCase):

    def test_get_alternate_text_wrapper(self):

        # get_alternate_text_wrapper
        record = {"language": "eng",
                  "title": "title in english",
                  "title_fra": "title in french"
                  }

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

    def test_iso_template_minimal(self):
        # this is a minimal record
        record = {"language": "eng",
                  "summary": "summary",
                  "summary_fra": "summary_fr",
                  'title': "title",
                  "title_fra": "title in french",
                  'institution': 'institution',
                  'id': 'id',
                  'keywords': 'keywords, oxygen',
                  'keywords_fra': "keywords in french"
                  }
        iso_template(record)

    def test_iso_template_absolutely_minimal(self):
        # without validation, just language needs to be set
        record = {"language": "eng"}
        iso_template(record, use_validation=False)

    def test_get_missing_fields(self):
        record = {"language": "eng",
                  'title': "title",
                  'institution': 'institution',
                  'id': 'id',
                  'keywords': 'keywords, oxygen'
                  }
        self.assertEqual(get_missing_fields(record), ['summary'])

    def test_get_alternate_language(self):
        self.assertEqual(get_alternate_language({"language": "eng"}), 'fra')
        self.assertEqual(get_alternate_language({"language": "fra"}), 'eng')

    def test_sanitize_record(self):
        self.assertEqual(sanitize_record({"title": None}), {})
        self.assertEqual(
            sanitize_record(
                {"erddap_dataset_url": "http://example.com?a&b"}),
            {"erddap_dataset_url": "http://example.com?a&amp;b"}
        )

    def test_list_intersection(self):
        self.assertEqual(list_intersection([1, 2], [2, 3]), [2])

    def test_check_date(self):
        good_dates = ['20161022',
                      '2010-09-28',
                      '20140102T12:01:22',
                      ]
        bad_dates = ['Monday January 3rd, 2017', '2010-31-01']
        for date in good_dates:
            self.assertTrue(check_date(date))
        for date in bad_dates:
            self.assertFalse(check_date(date))

    def test_has_eov_in_keywords(self):
        record = {"language": "fra",
                  "keywords": "kw1 in french",
                  "keywords_eng": "oxygen"
                  }
        self.assertTrue(has_eov_in_keywords(record))

        record = {"language": "eng",
                  "keywords_fra": "kw1 in french",
                  "keywords": "oxygen"
                  }
        self.assertTrue(has_eov_in_keywords(record))

        record = {"language": "eng",
                  "keywords": "kw1 in english"
                  }
        self.assertFalse(has_eov_in_keywords(record))


if __name__ == '__main__':
    unittest.main()

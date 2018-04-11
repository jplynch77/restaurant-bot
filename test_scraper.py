import unittest
import scraper
import pandas as pd

# https://docs.python.org/3/library/unittest.html#assert-methods

class UrlTestCase(unittest.TestCase):
    def test_new_york_url(self):

        test_url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.7127&lng=-74.0059&city=New%20York&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=40'

        self.assertIsInstance(scraper.url_scraper(test_url), pd.DataFrame)

if __name__ == '__main__':
    unittest.main()

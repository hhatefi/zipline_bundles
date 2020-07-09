from context import ingester as ig

import os
import unittest

class CSVIngesterTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_csvdir(self):
        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir=None, csvdir_env=None)

        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir='some nonexisting directory', csvdir_env=None)

        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir='/tmp', csvdir_env=None), '/tmp')

        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir=None, csvdir_env='some nonexisting environment variable')

        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir='some nonexisting directory', csvdir_env='some nonexisting environment variable')

        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir='/tmp', csvdir_env='some nonexisting environment variable'), '/tmp')

        os.environ['CSVDIR_TEST']='some nonexisting directory'
        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir=None, csvdir_env='CSVDIR_TEST')

        with self.assertRaises(ValueError):
            ig.csv_ingester.get_csvdir(csvdir='some nonexisting directory', csvdir_env='CSVDIR_TEST')

        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir='/tmp', csvdir_env='CSVDIR_TEST'), '/tmp')

        os.environ['CSVDIR_TEST']='/etc'
        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir=None, csvdir_env='CSVDIR_TEST'), '/etc')

        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir='some nonexisting directory', csvdir_env='CSVDIR_TEST'), '/etc')

        self.assertEqual(ig.csv_ingester.get_csvdir(csvdir='/tmp', csvdir_env='CSVDIR_TEST'), '/etc')
if __name__ == '__main__':
    unittest.main()

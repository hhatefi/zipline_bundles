from context import ingester as igt

import os
import unittest

class CSVIngesterTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_csvdir(self):
        ig=igt.csv_ingester('test_ingester', csvdir=None, csvdir_env=None)
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='some nonexisting directory', csvdir_env=None)
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='/tmp', csvdir_env=None)
        self.assertEqual(ig._get_csvdir(), '/tmp')

        ig=igt.csv_ingester('test_ingester', csvdir=None, csvdir_env='some nonexisting environment variable')
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='some nonexisting directory', csvdir_env='some nonexisting environment variable')
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='/tmp', csvdir_env='some nonexisting environment variable')
        self.assertEqual(ig._get_csvdir(), '/tmp')

        os.environ['CSVDIR_TEST']='some nonexisting directory'
        ig=igt.csv_ingester('test_ingester', csvdir=None, csvdir_env='CSVDIR_TEST')
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='some nonexisting directory', csvdir_env='CSVDIR_TEST')
        with self.assertRaises(ValueError):
            ig._get_csvdir()

        ig=igt.csv_ingester('test_ingester', csvdir='/tmp', csvdir_env='CSVDIR_TEST')
        self.assertEqual(ig._get_csvdir(), '/tmp')

        os.environ['CSVDIR_TEST']='/etc'
        ig=igt.csv_ingester('test_ingester', csvdir=None, csvdir_env='CSVDIR_TEST')
        self.assertEqual(ig._get_csvdir(), '/etc')

        ig=igt.csv_ingester('test_ingester', csvdir='some nonexisting directory', csvdir_env='CSVDIR_TEST')
        self.assertEqual(ig._get_csvdir(), '/etc')

        ig=igt.csv_ingester('test_ingester', csvdir='/tmp', csvdir_env='CSVDIR_TEST')
        self.assertEqual(ig._get_csvdir(), '/etc')
if __name__ == '__main__':
    unittest.main()

from context import ingester as ig

import os
import unittest
import pandas as pd

_g_start_date = pd.Timestamp('2020.01.01')

df_A=pd.DataFrame({'open': range(10),
                   'high': range(10, 20),
                   'low': range(20, 30),
                   'close': range(30, 40),
                   'volume': range(40, 50),
                   'dividend': [0]*10,
                   'split': [1]*10}, index= [_g_start_date + pd.Timedelta(days=i) for i in range(10)])

df_B=df_A + 5

def downloader(symbol):
    df = None
    if symbol == 'A':
        df = df_A
    elif symbol == 'B':
        df = df_B
    return df

class DirectIngesterTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_create_symbol_list(self):
        self.assertEqual(len(ig.direct_ingester.create_symbol_list('SYM_LIST', [])), 0)
        self.assertEqual(len(ig.direct_ingester.create_symbol_list('SYM_LIST', None)), 0)
        symlst = ig.direct_ingester.create_symbol_list('SYM_LIST', ['A', 'B'])
        self.assertEqual(len(symlst), 2)
        self.assertTrue('A' in symlst)
        self.assertTrue('B' in symlst)
        symlst = ig.direct_ingester.create_symbol_list('SYM_LIST', ['A', ''])
        self.assertEqual(len(symlst), 1)
        self.assertTrue('A' in symlst)
        os.environ['SYM_LIST'] = 'A,B,,  ,'
        symlst = ig.direct_ingester.create_symbol_list('SYM_LIST', ['A', 'B'])
        self.assertEqual(len(symlst), 2)
        self.assertTrue('A' in symlst)
        self.assertTrue('B' in symlst)

    def test_read_and_convert(self):
        class fake_adjustment_writer:
            def write(self):
                pass

        class fake_bar_writer:
            def write(self, gen, show_progress):
                self.dfs = list(gen)

        class fake_db_writer:
            def write(self,equities): # asset_db_writer
                self.df_metadata = equities

        ingester=ig.direct_ingester('EXX', False, None, downloader, symbol_list = ('A', 'B'))
        self.assertEqual(len(ingester._symbols), 2)

        adjustment_writer=fake_adjustment_writer()
        bar_writer=fake_bar_writer()
        db_writer=fake_db_writer()
        ingester(environ=None,
                 asset_db_writer=db_writer,
                 minute_bar_writer=None,
                 daily_bar_writer=bar_writer,
                 adjustment_writer=adjustment_writer,
                 calendar=None,
                 start_session=None,
                 end_session=None,
                 cache=None,
                 show_progress=True,
                 output_dir=None)
        self.assertEqual(len(bar_writer.dfs), 2)
        self.assertEqual(bar_writer.dfs[0][0], 0)
        self.assertEqual(bar_writer.dfs[1][0], 1)
        find_sym_idx=lambda df,sym: df[df.symbol == sym].index[0]
        idx_A=find_sym_idx(db_writer.df_metadata, 'A')
        idx_B=find_sym_idx(db_writer.df_metadata, 'B')
        self.assertTrue(bar_writer.dfs[idx_A][1].equals(df_A))
        self.assertTrue(bar_writer.dfs[idx_B][1].equals(df_B))

        self.assertEqual(len(db_writer.df_metadata), 2)
        self.assertEqual(db_writer.df_metadata.symbol.loc[idx_A], 'A')
        self.assertEqual(db_writer.df_metadata.symbol.loc[idx_B], 'B')
        for d in db_writer.df_metadata.start_date:
            self.assertEqual(d, pd.Timestamp('2020.01.01'))
        for d in db_writer.df_metadata.end_date:
            self.assertEqual(d, pd.Timestamp('2020.01.10'))


if __name__ == '__main__':
    unittest.main()

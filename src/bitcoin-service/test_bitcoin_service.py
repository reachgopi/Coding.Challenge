import unittest
from unittest.mock import patch
from bitcoin_service import BitcoinService 
import json
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import warnings
import numpy as np

class TestBitcoinService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
        warnings.simplefilter(action="ignore", category=FutureWarning)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        
        self.bitcoin_service = BitcoinService()

    def tearDown(self):
        return super().tearDown()
    
    @patch("bitcoin_service.pd.read_json")
    def test_fetch_bitcoin_historical_data(self, mocked_df):
        mocked_df.return_value = {"status":"success","data":{"change":-25.85,"history":[{"price":"61514.9224686475","timestamp":1618660800000},{"price":"61598.7846813559","timestamp":1618664400000}]}}

        historical_data = self.bitcoin_service.fetch_bitcoin_historical_data('1','30d')
        mocked_df.assert_called_once()
        mocked_df.assert_called_with('https://api.coinranking.com/v1/public/coin/1/history/30d')
        self.assertEqual(historical_data.empty,False)
    
    @patch("bitcoin_service.pd.read_json")
    def test_get_bitcoin_historical_data_empty_response(self, mocked_df):
        mocked_df.return_value = {}

        final_json = self.bitcoin_service.get_bitcoin_historical_data()
        self.assertRaises(Exception,self.bitcoin_service.get_bitcoin_historical_data())
        self.assertEqual(final_json,{'status': 'Failure while fetching bitcoin data'})

    @patch("bitcoin_service.pd.read_json")
    def test_get_bitcoin_historical_data_na_response(self, mocked_df):
        #Mock contains data 2 dates  Sunday, April 18, 2021 00:00:00 and Tuesday, April 19, 2021 00:00:00
        # Final Json contains only 2 date data 
        mocked_df.return_value = {
            "status":"success",
            "data":
            {
                "change":-27.03,
                "history":[
                {
                    "price": "60832.9681441684",
                    "timestamp": 1618704000000
                }, 
                {
                    "price": "57092.1052704172",
                    "timestamp": 1618790400000
                }
                ]
            }
        }
        final_json = self.bitcoin_service.get_bitcoin_historical_data()
        final_json_val = json.loads(final_json)
        self.assertEqual(len(final_json_val),2)
        # Check Prices Rounded to 2 decimals
        self.assertAlmostEqual(final_json_val[0]['price'],60832.9681441684, places=2)
        # Check Date Format contains T00:00:00
        self.assertEqual(final_json_val[0]['date'][10:],'T00:00:00')
        self.assertEqual(final_json_val[0]['dayOfWeek'],'Sunday')
        self.assertEqual(final_json_val[0]['direction'],'na')
        self.assertEqual(final_json_val[0]['change'],'na')
        self.assertEqual(final_json_val[0]['highSinceStart'],'na')
        self.assertEqual(final_json_val[0]['lowSinceStart'],'na')

    @patch("bitcoin_service.pd.read_json")
    def test_get_bitcoin_historical_data_non_na_response(self, mocked_df):
        # Mock contains data 2 dates  Sunday, April 18, 2021 00:00:00 and Tuesday, April 19, 2021 00:00:00
        # Final Json contains only 2 days of data 
        mocked_df.return_value = {
            "status":"success",
            "data":
            {
                "change":-27.03,
                "history":[
                {
                    "price": "60832.9681441684",
                    "timestamp": 1618704000000
                }, 
                {
                    "price": "57092.1052704172",
                    "timestamp": 1618790400000
                }
                ]
            }
        }

        final_json = self.bitcoin_service.get_bitcoin_historical_data()
        final_json_val = json.loads(final_json)
        self.assertEqual(len(final_json_val),2)
        # Check Prices Rounded to 2 decimals
        self.assertAlmostEqual(final_json_val[1]['price'],57092.1052704172, places=2)
        # Check Date Format contains T00:00:00
        self.assertEqual(final_json_val[0]['date'][10:],'T00:00:00')
        self.assertEqual(final_json_val[1]['dayOfWeek'],'Monday')
        self.assertEqual(final_json_val[1]['direction'],'down')
        self.assertEqual(final_json_val[1]['change'],-3740.86)
        self.assertEqual(final_json_val[1]['highSinceStart'],False)
        self.assertEqual(final_json_val[1]['lowSinceStart'],True)

    @patch("bitcoin_service.pd.read_json")
    def test_get_bitcon_historical_stats_empty_response(self, mocked_df):
        mocked_df.return_value = {}

        final_json = self.bitcoin_service.get_bitcon_historical_stats()
        self.assertRaises(Exception,self.bitcoin_service.get_bitcon_historical_stats())
        self.assertEqual(final_json,{'status': 'Failure while fetching bitcoin historical stats data'})

    @patch("bitcoin_service.pd.read_json")
    def test_get_bitcon_historical_stats(self, mocked_df):
        # Mock contains one day of data (Apr 18 starting from 00:00) to check average, variance and standard deviation
        # Final Json contains only 2 days of data 
        mock_json = {
            "status":"success",
            "data":{"change":-27.03,
            "history":[{
                "price": "60832.9681441684",
                "timestamp": 1618704000000
            }, {
                "price": "60376.6080762022",
                "timestamp": 1618707600000
            }, {
                "price": "59962.2277983529",
                "timestamp": 1618711200000
            }, {
                "price": "56941.9979747833",
                "timestamp": 1618714800000
            }, {
                "price": "55707.8847873915",
                "timestamp": 1618718400000
            }, {
                "price": "56007.984773762",
                "timestamp": 1618722000000
            }, {
                "price": "56706.1511186773",
                "timestamp": 1618725600000
            }, {
                "price": "56773.1229502206",
                "timestamp": 1618729200000
            }, {
                "price": "56923.3440352815",
                "timestamp": 1618732800000
            }, {
                "price": "55647.7098349653",
                "timestamp": 1618736400000
            }, {
                "price": "55595.259805046",
                "timestamp": 1618740000000
            }, {
                "price": "55282.3579473798",
                "timestamp": 1618743600000
            }, {
                "price": "54276.6335836324",
                "timestamp": 1618747200000
            }, {
                "price": "55604.1907123282",
                "timestamp": 1618750800000
            }, {
                "price": "55995.5829362097",
                "timestamp": 1618754400000
            }, {
                "price": "56065.3472949581",
                "timestamp": 1618758000000
            }, {
                "price": "56137.9119214635",
                "timestamp": 1618761600000
            }, {
                "price": "56157.7147409821",
                "timestamp": 1618765200000
            }, {
                "price": "55924.0260698999",
                "timestamp": 1618768800000
            }, {
                "price": "56333.832428869",
                "timestamp": 1618772400000
            }, {
                "price": "56383.2606523681",
                "timestamp": 1618776000000
            }, {
                "price": "56906.5511349983",
                "timestamp": 1618779600000
            }, {
                "price": "56950.4950439236",
                "timestamp": 1618783200000
            }, {
                "price": "57283.6769581103",
                "timestamp": 1618786800000
            }]}}

        mocked_df.return_value = mock_json
        # from same data just getting history array to calculate mean and variance from numpy to compare against the dataframe values
        np_array = np.array([])
        for json_val in mock_json['data']['history']:
            np_array = np.append(np_array,float(json_val['price']))
        final_json = self.bitcoin_service.get_bitcon_historical_stats()
        final_json_val = json.loads(final_json)
        self.assertEqual(len(final_json_val),1)
        self.assertEqual(final_json_val[0]['date'][10:],'T00:00:00')
        # Check Prices Rounded to 2 decimals
        self.assertAlmostEqual(final_json_val[0]['price'],60832.9681441684, places=2)
        # Check Date Format contains T00:00:00
        self.assertAlmostEqual(final_json_val[0]['dailyAverage'],np.mean(np_array,axis=0), places=2)
        #self.assertAlmostEqual(final_json_val[0]['dailyVariance'],np.var(np_array, axis=0), places=2)
        mean = np.mean(np.around(np_array),axis=0)
        std_dev = np.std(np.around(np_array),axis=0)
        high_range = mean + 2 * std_dev
        low_range = mean - 2 * std_dev
        high_occurence = np_array > high_range
        low_occurence = np_array < low_range
        volatile_flag = False
        if high_occurence.sum() > 0 or low_occurence.sum() > 0:
            volatile_flag = True
        self.assertEqual(final_json_val[0]['volatilityAlert'], volatile_flag)

if __name__ == '__main__':
    unittest.main()
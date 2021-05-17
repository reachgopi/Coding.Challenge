import pandas as pd
from pandas.io.json import json_normalize
import json
import math
import constants

class BitcoinService():
    def __init__(self):
        super().__init__()

    def fetch_bitcoin_historical_data(self, coin_id, timeframe):
        '''
            input: accepts timeframe as parameter
            fetch the bitcoin historical data from coinranking api for the given timeframe
            output: returns the historical data pandas dataframe
        '''
        try:
            api_url = constants.BITCOIN_HISTORY_API_URL.format(coin_id, timeframe)
            df = pd.read_json(api_url)
            historical_data = json_normalize(df['data']['history'])
            return historical_data
        except Exception as e:
            print(f'Exception occured while fetching data for timeframe:{timeframe} from Bitcoin Service and the error is: {e}')
            raise

    def get_bitcoin_historical_data(self, coin_id = 1, timeframe ='30d'):
        '''
        Accepts coin_id and timeframe as input parameter (if not provided defaulted to bitcoin id (1) and timeframe 30 days)
        By default retrieves last 30days bitcoin historical data and 
        parses the data into the JSON array contains the following schema JSON object
        Output schema:
        {
            "date": "{date}",
            "price": "{value}",
            "direction": "{up/down/same}",
            "change": "{amount}",
            "dayOfWeek": "{name}”,
            "highSinceStart": "{true/false}”,
            "lowSinceStart": "{true/false}”
        }
        '''
        final_json = {}
        try:
            # Bitcoin API Dataframe
            bitcoin_api_df = self.fetch_bitcoin_historical_data(coin_id, timeframe)
            
            #Output format data gets saved into this datframe
            output_data = pd.DataFrame()
            
            #Formatting different fields (date,price,dayOfWeek,) of data as per specs
            output_data['datetime'] = pd.to_datetime(bitcoin_api_df['timestamp'], unit='ms')\
                                        .dt.strftime('%Y-%m-%d %H:%M:%S')
            output_data['datetime'] = output_data['datetime'].astype('datetime64[ns]')
            output_data['date'] = pd.to_datetime(bitcoin_api_df['timestamp'], unit='ms')\
                                    .dt.strftime('%Y-%m-%dT%H:%M:%S')
            output_data['price'] = bitcoin_api_df['price'].astype(float).round(2)
            output_data['dayOfWeek'] = pd.to_datetime(bitcoin_api_df['timestamp'], unit='ms')\
                                        .dt.day_name()
            
            #Sorting the dataframe by datetime as there is no explicit information given in api that the data is sorted by oldest value
            output_data.sort_values(by='datetime')

            #Filtering the output data just to keep only the 00:00:00 values for every day
            filtered_output_data = output_data[output_data['date'].str.contains('T00:00:00', regex=False)]
            
            # Initializing variables
            high_since_start = -math.inf
            low_since_start = math.inf
            prev_price = 0.0
            count = 0
        
            # For loop to iterate and populate the following fields in filtered_output_data dataframe
            # 1. direction 
            # 2. change
            # 3. highSinceStart 
            # 4. lowSinceStart
            for index in filtered_output_data.index:
                if count == 0:
                    filtered_output_data.loc[index,'direction'] = "na"
                    filtered_output_data.loc[index,'change'] ="na"
                    filtered_output_data.loc[index,'highSinceStart'] ="na"
                    filtered_output_data.loc[index,'lowSinceStart'] ="na"
                    high_since_start = max(high_since_start,filtered_output_data.loc[index,'price'])
                    low_since_start = min(low_since_start,filtered_output_data.loc[index,'price'])
                    prev_price = filtered_output_data.loc[index,'price']
                else:
                    current_price = filtered_output_data.loc[index,'price']
                    change_val = current_price - prev_price
                    filtered_output_data.loc[index,'change'] = change_val
                    filtered_output_data.loc[index,'highSinceStart'] =False
                    filtered_output_data.loc[index,'lowSinceStart'] =False
                    if change_val < 0 :
                        filtered_output_data.loc[index,'direction'] = "down"
                    elif change_val > 0 :
                        filtered_output_data.loc[index,'direction'] = "up"
                    else:
                        filtered_output_data.loc[index,'direction'] = "same"
                    high_since_start = max(high_since_start,current_price)
                    low_since_start = min(low_since_start,current_price)
                    if high_since_start == current_price:
                        filtered_output_data.loc[index,'highSinceStart'] = True
                    if low_since_start == current_price:
                        filtered_output_data.loc[index,'lowSinceStart'] = True
                    prev_price = current_price
                count += 1

            filtered_output_data.drop(['datetime'], axis='columns', inplace=True)
            final_json = filtered_output_data.to_json(orient ='records')
        except Exception as e:
            print(f'Exception occured in get_bitcoin_historical_data with following error {e} --->>>>')
            final_json = {"status":"Failure while fetching bitcoin data"}

        return final_json

    def get_bitcon_historical_stats(self, coin_id = 1, timeframe = '30d'):
        '''
            Accepts coin_id and timeframe as parameter (if not provided defaulted to bitcoin id (1) and timeframe 30 days)
            By default retrieves last 30days bitcoin historical data and 
            parses the data into the JSON array contains the following schema JSON object
            Output schema:
            {
                "date": "{date}",
                "price": "{value}",
                "dailyAverage": "{value}",
                "dailyVariance": "{value}",
                "volatilityAlert:": "{true/false}”
             }
        '''
        final_json = {}
        try:
            # Bitcoin API Dataframe
            bitcoin_api_df = self.fetch_bitcoin_historical_data(coin_id, timeframe)

            #Output format data gets saved into this datframe
            output_data = pd.DataFrame()
            
            #Formatting different fields (date,price) of data as per specs
            output_data['datetime'] = pd.to_datetime(bitcoin_api_df['timestamp'], unit='ms')\
                                        .dt.strftime('%Y-%m-%d %H:%M:%S')
            output_data['datetime'] = output_data['datetime'].astype('datetime64[ns]')
            output_data['date'] = pd.to_datetime(bitcoin_api_df['timestamp'], unit='ms')\
                                    .dt.strftime('%Y-%m-%dT%H:%M:%S')
            output_data['price'] = bitcoin_api_df['price'].astype(float).round(2)
            output_data.sort_values(by='datetime')

            filtered_data = output_data[output_data['date'].str.contains('T00:00:00')]
            
            # For loop to calculate the following
            # 1. dailyAverage: average price for a given day is calculated by taking a df between 00:00:00 to 23:00:00 for the day and calling mean method in df
            # 2. dailyVariance: price variance for a given day is by applying variance in the sub dataframe
            # 3. volatilityAlert: volatility_flag is identified by checking the price is varying by 2 standard deviation in high and low range 
            for index in filtered_data.index:
                date_val = filtered_data.loc[index,'datetime']
                start = str(date_val) + " "+ "00:00:00"
                end = str(date_val) + " "+ "23:00:00"
                mask = (output_data['datetime'] >= start) & (output_data['datetime'] <= end)
                df = output_data.loc[mask]
                mean = df['price'].mean()
                variance = df.var(ddof=0)['price']
                std_dev = df.std(ddof=0)['price']
                high_range = mean + 2 * std_dev
                low_range = mean - 2 * std_dev
                volatility_flag = ((df['price'] > high_range).any() or (df['price'] < low_range).any())
                filtered_data.loc[index,'dailyAverage'] = mean
                filtered_data.loc[index,'dailyVariance'] = variance
                filtered_data.loc[index,'volatilityAlert'] = volatility_flag
        
            filtered_data.drop(['datetime'], axis='columns', inplace=True)
            final_json = filtered_data.to_json(orient ='records')
        except Exception as e:
            print(f'Exception occured in get_bitcon_historical_stats with following error {e} --->>>>')
            final_json = {"status":"Failure while fetching bitcoin historical stats data"}
        return final_json
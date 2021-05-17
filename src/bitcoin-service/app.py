from flask import Flask
from bitcoin_service import BitcoinService
app = Flask(__name__)

@app.route("/")
def health_check():
    ''' 
    Returns health status of the API
    '''
    return "Success!"

@app.route("/history/bitcoin-data")
def get_bitcoin_historical_data():
    ''' 
        Returns bitcoin historical price data by calling the coinranking getcoinhistory API
    '''
    return BitcoinService().get_bitcoin_historical_data()

@app.route("/history/bitcoin-stats")
def get_bitcoin_historical_data_stats():
    ''' 
        Returns bitcoin historical price stats data by calling the coinranking getcoinhistory API
    '''
    return BitcoinService().get_bitcon_historical_stats()
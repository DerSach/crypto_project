import sys
import requests
import pandas as pd
import os.path
import pyinputplus as pyip
from datetime import datetime

def get_crypto_df():
    ''' Upload our portfolio csv or create one if it does not exist '''
    if os.path.isfile('data/v1/crypto_portfolio.csv'):
        crypto_df = pd.read_csv('data/v1/crypto_portfolio.csv', index_col=[0])
        if list(crypto_df.columns) != ['date','crypto','trade_price','amount','currency']:
            return print('Your portfolio csv does not have the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
    else:
        col_list = ['date','crypto','trade_price','amount','currency']
        crypto_df = pd.DataFrame(columns = col_list)
    crypto_df.sort_values(by = 'date', inplace = True)
    crypto_df.reset_index(inplace = True, drop  = True)
    return crypto_df

def print_portfolios(df):
    ''' Displays your current portfolio and, if it exists, your historical profit csv'''
    if len(df) == 0:
        print('Your portfolio is emplty')
    else:
        print()
        print('YOUR CRYPTO PORTFOLIO')
        print(df)
    if os.path.isfile('data/v1/crypto_historical_profit.csv'):
        hist_profit_df = pd.read_csv('data/v1/crypto_historical_profit.csv', index_col=[0])
        print()
        print('YOUR HISTORICAL PROFIT')
        print(hist_profit_df)

def add_crypto(df):
    ''' Add a crypto to your portfolio df '''
    date = pyip.inputDate('Please enter date of trade (YYYY/mm/dd): ', formats=['%Y/%m/%d'])
    crypto = pyip.inputStr('Please enter the crypto symbol traded (BTC, DOGE, ...): ')
    price = pyip.inputNum('Please enter the price of the trade: ')
    amount = pyip.inputNum('Please enter the amount of your trade: ')
    currency = pyip.inputStr('Please enter the currency symbol of your trade (EUR, USD, ...): ')
    list_x = [date, crypto.upper(), float(price), float(amount), currency.upper()]
    len_df = len(df)
    df.loc[len_df] = list_x
    if not os.path.isdir('data/v1'):
        os.makedirs('data/v1')
    df.to_csv('data/v1/crypto_portfolio.csv')
    return df

def remove_crypto(df):
    ''' Removing a trade in our portfolio '''
    if len(df) == 0:
        print('Your portfolio is emplty')
    else:
        print(df)
        index_removed = pyip.inputNum('Which trade number do you want to remove? ')
        df.drop(index = index_removed, inplace = True)
        df.reset_index(drop=True, inplace = True)
        df.to_csv('data/v1/crypto_portfolio.csv')
    
def adding_spot_profit_cols(df, dic):
    ''' Get lastest crypto spot prices (if not already asked) and computing the current profit in the currency of the trade for each trade '''

    ''' Getting the latest crypto sport prices and storing it in our dic '''
    for crypto, currency in zip(df['crypto'],df['currency']):
        pair = f'{crypto.upper()}/{currency.upper()}'
        if pair not in dic:
            print(f'Requesting {crypto.upper()} spot {currency.upper()} price...')
            url = f'https://rest.coinapi.io/v1/exchangerate/{pair}'
            headers = {'X-CoinAPI-Key' : sys.argv[1]}
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                print('You have exceeded your API key last 24 hour requests executed limit, please wait for new requests or contact support for upgrading your existing plan or enabling overage.')
                sys.exit(1)
            if response.status_code == 401:
                print('Invalid API key. If this is a new API Key, then CoinAPI needs a few minutes to propagate it through its independent server sites.')
                sys.exit(1)
            if response.status_code != 200:
                print('Wrong crypto or currency symbol added, please remove it from csv before launching the app again')
                sys.exit(1)
            spot_price = response.json()['rate']
            print(spot_price)
            dic[pair] = spot_price

    ''' Enables to store our dic as global variable spot_dic not to later make new API calls for the same exchange rates already asked '''
    global spot_dic
    spot_dic = dic
    
    ''' Modifying our df without saving it to csv to compute our profit in the currency of the trade '''
    df['pair'] = df['crypto']+'/'+df['currency']
    df['spot_price'] = df['pair'].map(dic)
    df['pct_chg_since_trade'] = (df['spot_price'] - df['trade_price'])/df['trade_price']
    df['profit (in currency of trade)'] = df['pct_chg_since_trade']*df['amount']
    return df

def get_final_profit(df, target_currency, dic):
    ''' Computing the sum of profits for all the trades in the desired currency '''
    
    ''' Getting all the exchange rates to convert our trades profits in the target currency '''
    for base_curr in df['currency']:
        pair = f'{base_curr.upper()}/{target_currency.upper()}'
        if pair not in dic:
            if base_curr.upper() != target_currency.upper():
                print(f'Requesting {base_curr.upper()}/{target_currency.upper()} exchange rate...')
                url =f'https://rest.coinapi.io/v1/exchangerate/{pair}'
                headers = {'X-CoinAPI-Key' : sys.argv[1]}
                response = requests.get(url, headers=headers)
                if response.status_code == 429:
                    print('You have exceeded your API key last 24 hour requests executed limit, please wait for new requests or contact support for upgrading your existing plan or enabling overage.')
                    sys.exit(1)
                if response.status_code == 401:
                    print('Invalid API key. If this is a new API Key, then CoinAPI needs a few minutes to propagate it through its independent server sites.')
                    sys.exit(1)
                if response.status_code != 200:
                    print('Wrong crypto or currency symbol added, please remove it from csv before launching the app again.')
                exch_rate = response.json()['rate']
                print(exch_rate)
                dic[pair] = exch_rate
            else:
                dic[pair] = 1

    ''' Enables to store our dic as global variable curr_dic not to later make new API calls for the same exchange rates already asked '''
    global curr_dic
    curr_dic = dic
    
    ''' Modifying our df without saving it to csv to compute our profit in the target currency '''
    df['target_currency'] = target_currency.upper()
    df['pair'] = df['currency']+'/'+df['target_currency']
    df['exch_rate_to_target_currency'] = df['pair'].map(dic)
    df['profit (in target currency)'] = df['profit (in currency of trade)'] * df['exch_rate_to_target_currency']

    ''' Summing all trades profits to get the final profit '''
    final_profit = df['profit (in target currency)'].sum()
    return final_profit

def get_historical_profit_df(profit, currency):
    ''' Create or amend our historical profit csv file '''
    if os.path.isfile('data/v1/crypto_historical_profit.csv'):
        hist_profit_df = pd.read_csv('data/v1/crypto_historical_profit.csv', index_col=[0])
        if list(hist_profit_df.columns) != ['date','profit','currency']:
            return print('Cannot update your historical profit csv as not the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
    else:
        col_list = ['date','profit','currency']
        hist_profit_df = pd.DataFrame(columns = col_list)
    date = datetime.now()
    hist_profit_df.loc[len(hist_profit_df)] = [date, profit, currency]
    if not os.path.isdir('data/v1'):
        os.makedirs('data/v1')
    hist_profit_df.to_csv('data/v1/crypto_historical_profit.csv')
    return print('Profit added to your historical profit csv. ')

def main():
    ''' Main function '''
    choice = input('Do you want to [see] your portfolio, [add] a crypto trade to your portfolio, [remove] a crypto trade from your portfolio, or get your current [profit]? ')  
    if choice not in ['see','add','remove','profit']:
        print('Please enter either "see", "add", "remove" or "profit"')
        sys.exit(1)
    else: 
        crypto_df = get_crypto_df()
        if choice == 'see':
            print_portfolios(crypto_df)
        if choice == 'add':
            crypto_df = add_crypto(crypto_df)
            print('Crypto successfully added!')
        if choice == 'remove':
            remove_crypto(crypto_df)
        elif choice == 'profit':
            if len(crypto_df) == 0:
                print('Your portfolio is empty! Please add crypto before computing your profit.')
            else:
                currency = input('In which currency do you want your profit? ')
                crypto_df = adding_spot_profit_cols(crypto_df, spot_dic)
                profit = round(get_final_profit(crypto_df, currency, curr_dic),2)
                print(f'Your current profit is {profit} {currency.upper()}')
                historical = pyip.inputYesNo('Would you like to add it to your historical profit csv? ')
                if historical == 'yes':
                    get_historical_profit_df(profit, currency.upper())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python crypto_project_v1.py YourCoinAPIKey")
        sys.exit(1)
    else:
        ''' First call of the program, no API calls have been made yet, so initializing our spot_dic and curr_dic global variables '''
        spot_dic = {}
        curr_dic = {}
        try:
            while True:
                main()
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit(0)
            
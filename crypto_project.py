import sys
import requests
import pandas as pd
import os.path
import pyinputplus as pyip

def get_crypto_df():
    ''' Upload our portfolio csv or create one if it does not exist '''
    if os.path.isfile('crypto_portfolio.csv'):
        crypto_df = pd.read_csv('crypto_portfolio.csv', index_col=[0])
    else:
        col_list = ['date','crypto','trade_price','amount','currency']
        crypto_df = pd.DataFrame(columns = col_list)
    return crypto_df

def print_portfolio(df):
    ''' Displays your current portfolio'''
    if len(df) == 0:
        print('Your portfolio is emplty')
    else:
        print(df)

def add_crypto(df):
    ''' Add a crypto to your portfolio df '''
    date = pyip.inputDate('Please enter date of trade (YYYY/mm/dd): ', formats=['%Y/%m/%d'])
    crypto = pyip.inputStr('Please enter the crypto symbol traded (BTC, DOGE, ...): ')
    price = pyip.inputNum('Please enter the price of the trade: ')
    amount = pyip.inputNum('Please enter the amount of your trade: ')
    currency = pyip.inputStr('Please enter the currency symbol of your trade (EUR, USD, ...): ')
    list_x = [date, crypto, float(price), float(amount), currency]
    len_df = len(df)
    df.loc[len_df] = list_x
    df.to_csv('crypto_portfolio.csv')
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
        df.to_csv('crypto_portfolio.csv')
    
def adding_spot_profit_cols(df, dic):
    ''' Get lastest crypto spot prices (if not already asked) and computing the current profit in the currency of the trade for each trade '''

    ''' Getting the latest crypto sport prices and storing it in our dic '''
    for crypto, currency in zip(df['crypto'],df['currency']):
        pair = f'{crypto}/{currency}'
        if pair not in dic:
            print(f'Requesting {crypto} spot {currency} price...')
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

# Final profit
def get_final_profit(df, target_currency, dic):
    ''' Computing the sum of profits for all the trades in the desired currency '''
    
    ''' Getting all the exchange rates to convert our trades profits in the target currency '''
    for base_curr in df['currency']:
        if base_curr not in dic:
            if base_curr != target_currency:
                print(f'Requesting {base_curr}/{target_currency} exchange rate...')
                url =f'https://rest.coinapi.io/v1/exchangerate/{base_curr}/{target_currency}'
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
                dic[base_curr] = exch_rate
            else:
                dic[base_curr] = 1

    ''' Enables to store our dic as global variable curr_dic not to later make new API calls for the same exchange rates already asked '''
    global curr_dic
    curr_dic = dic
    
    ''' Modifying our df without saving it to csv to compute our profit in the target currency '''
    df['exch_rate_to_target_currency'] = df['currency'].map(dic)
    df['profit (in target currency)'] = df['profit (in currency of trade)'] * df['exch_rate_to_target_currency']

    ''' Summing all trades profits to get the final profit '''
    final_profit = df['profit (in target currency)'].sum()
    return final_profit

# Main function
def main():
    choice = input('Do you want to [see] your portfolio, [add] a crypto trade to your portfolio, [remove] a crypto trade from your portfolio, or get your current [profit]? ')  
    if choice not in ['see','add','remove','profit']:
        print('Please enter either "see", "add", "remove" or "profit"')
        sys.exit(1)
    else: 
        crypto_df = get_crypto_df()
        if choice == 'see':
            print_portfolio(crypto_df)
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
                print(f'Your current profit is {round(get_final_profit(crypto_df, currency, curr_dic),2)} {currency}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python crypto_project.py YourCoinAPIKey")
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
            
import sys
import requests
import pandas as pd
import os.path
import pyinputplus as pyip
import datetime

def get_trades_portfolio_and_stop_orders_dfs():
    ''' Upload our trades and portoflio csvs or create one if it does not exist '''
    if os.path.isfile('data/v2/crypto_trades.csv'):
        trades_df = pd.read_csv('data/v2/crypto_trades.csv', index_col=[0])
        if list(trades_df.columns) != ['date','crypto','b/s','trade_price','amount','currency','crypto_unit']:
            print('Your trades csv does not have the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
            sys.exit(1)
    else:
        col_list = ['date','crypto','b/s','trade_price','amount','currency','crypto_unit']
        trades_df = pd.DataFrame(columns = col_list)
    trades_df.sort_values(by = 'date', inplace = True)
    trades_df.reset_index(inplace = True, drop  = True)
    
    ''' Same for portfolio dfs '''
    if os.path.isfile('data/v2/crypto_portfolio.csv'):
        portfolio_df = pd.read_csv('data/v2/crypto_portfolio.csv', index_col=[0])
        if list(portfolio_df.columns) != ['crypto','crypto_unit']:
            print('Your portfolio csv does not have the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
            sys.exit(1)
    else:
        col_list = ['crypto','crypto_unit']
        portfolio_df = pd.DataFrame(columns = col_list)
    portfolio_df.sort_values(by = 'crypto', inplace = True)
    portfolio_df.reset_index(inplace = True, drop  = True)
    
    ''' Same for stop orders dfs '''
    if os.path.isfile('data/v2/crypto_stop_orders.csv'):
        stop_orders_df = pd.read_csv('data/v2/crypto_stop_orders.csv', index_col=[0])
        if list(stop_orders_df.columns) != ['date','crypto','b/s','stop_order_price','amount','currency','crypto_unit']:
            print('Your stop orders csv does not have the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
            sys.exit(1)
    else:
        col_list = ['date','crypto','b/s','trade_price','amount','currency','crypto_unit']
        stop_orders_df = pd.DataFrame(columns = col_list)
    stop_orders_df.sort_values(by = 'date', inplace = True)
    stop_orders_df.reset_index(inplace = True, drop  = True)
    
    return trades_df, portfolio_df, stop_orders_df

def print_portfolios(trades_df, portfolio_df, stop_orders_df):
    ''' Displays your trades and current portfolio and, if it exists, your historical profit csv'''
    if len(trades_df) == 0:
        print('Your trades csv is empty')
    else:
        print()
        print('YOUR CRYPTO TRADES HISTORY')
        print(trades_df)
        
    if len(portfolio_df) == 0:
        print('Your portfolio is empty')
    else:
        print()
        print('YOUR CRYPTO PORTFOLIO')
        print(portfolio_df)
                
    if len(stop_orders_df) == 0:
        print('Your stop market orders csv is empty')
    else:
        print()
        print('YOUR CRYPTO STOP MARKET ORDERS')
        print(stop_orders_df)
        
    if os.path.isfile('data/v2/crypto_historical_profit.csv'):
        hist_profit_df = pd.read_csv('data/v2/crypto_historical_profit.csv', index_col=[0])
        print()
        print('YOUR HISTORICAL PROFIT')
        print(hist_profit_df)

def add_crypto_trade():
    
    ''' Create if need be our trades history csv file '''
    if os.path.isfile('data/v2/crypto_trades.csv'):
        trades_df = pd.read_csv('data/v2/crypto_trades.csv', index_col=[0])
        if list(trades_df.columns) != ['date','crypto','b/s','trade_price','amount','currency','crypto_unit']:
            return print('Cannot update your trades history csv as it has not the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
    else:
        col_list = ['date','crypto','b/s','trade_price','amount','currency','crypto_unit']
        trades_df = pd.DataFrame(columns = col_list)
        
    ''' Add a crypto trade to your trades df and updates your portfolio csv '''
    date = pyip.inputDate('Please enter date of trade (YYYY/mm/dd): ', formats=['%Y/%m/%d'])
    crypto = pyip.inputStr('Please enter the crypto symbol traded (BTC, DOGE, ...): ')
    buyorsell = pyip.inputChoice(['Buy', 'Sell'])
    price = pyip.inputNum('Please enter the price of the trade: ')
    amount = pyip.inputNum('Please enter the amount of your trade: ')
    currency = pyip.inputStr('Please enter the currency symbol of your trade (EUR, USD, ...): ')
    if buyorsell == 'Buy':
        crypto_unit = float(amount)/float(price)
    elif buyorsell == 'Sell':
        crypto_unit = -float(amount)/float(price)
    list_x = [date, crypto.upper(), buyorsell, float(price), float(amount), currency.upper(), crypto_unit]
    len_df = len(trades_df)
    trades_df.loc[len_df] = list_x
    if not os.path.isdir('data/v2'):
        os.makedirs('data/v2')
    trades_df.to_csv('data/v2/crypto_trades.csv')
    portfolio_df = trades_df.groupby('crypto',as_index=False)['crypto_unit'].sum()
    portfolio_df.to_csv('data/v2/crypto_portfolio.csv')
    return trades_df, portfolio_df


def add_stop_order():
    
    ''' Create if need be our trades history csv file '''
    if os.path.isfile('data/v2/crypto_stop_orders.csv'):
        stop_orders_df = pd.read_csv('data/v2/crypto_stop_orders.csv', index_col=[0])
        if list(stop_orders_df.columns) != ['date','crypto','b/s','stop_order_price','amount','currency','crypto_unit']:
            return print('Cannot update your stop orders history csv as it has not the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
    else:
        col_list = ['date','crypto','b/s','stop_order_price','amount','currency','crypto_unit']
        stop_orders_df = pd.DataFrame(columns = col_list)
        
    ''' Add a stop order to your stop orders df '''
    date = pyip.inputDate('Please enter date of trade (YYYY/mm/dd): ', formats=['%Y/%m/%d'])
    crypto = pyip.inputStr('Please enter the crypto symbol traded (BTC, DOGE, ...): ')
    buyorsell = pyip.inputChoice(['Buy', 'Sell'])
    stop_order_price = pyip.inputNum('Please enter the stop market order price of the trade: ')
    currency = pyip.inputStr('Please enter the currency symbol of your trade (EUR, USD, ...): ')
    crypto_unit = pyip.inputNum('Please enter the number of crypto units that will be traded if this stop market order is executed: ')
    if buyorsell == 'Buy':
        amount = - float(crypto_unit) * float(stop_order_price)
    elif buyorsell == 'Sell':
        amount = float(crypto_unit) * float(stop_order_price)
    list_x = [date, crypto.upper(), buyorsell, float(stop_order_price), float(amount), currency.upper(), float(crypto_unit)]
    len_df = len(stop_orders_df)
    stop_orders_df.loc[len_df] = list_x
    if not os.path.isdir('data/v2'):
        os.makedirs('data/v2')
    stop_orders_df.to_csv('data/v2/crypto_stop_orders.csv')
    return stop_orders_df


def remove_crypto():
    ''' Removing a trade and updating the portfolio '''
    trades_df = pd.read_csv('data/v2/crypto_trades.csv', index_col=[0])
    if len(trades_df) == 0:
        print('Your trades history is empty')
    else:
        print(trades_df)
        index_removed = pyip.inputNum('Which trade number do you want to remove? ')
        trades_df.drop(index = index_removed, inplace = True)
        trades_df.reset_index(drop=True, inplace = True)
        trades_df.to_csv('data/v2/crypto_trades.csv')
        portfolio_df = trades_df.groupby('crypto',as_index=False)['crypto_unit'].sum()
        portfolio_df.to_csv('data/v2/crypto_portfolio.csv')
        
        
def remove_stop_order():
    ''' Removing a stop market order '''
    stop_orders_df = pd.read_csv('data/v2/crypto_stop_orders.csv', index_col=[0])
    if len(stop_orders_df) == 0:
        print('Your stop market order history is empty')
    else:
        print(stop_orders_df)
        index_removed = pyip.inputNum('Which trade number do you want to remove? ')
        stop_orders_df.drop(index = index_removed, inplace = True)
        stop_orders_df.reset_index(drop=True, inplace = True)
        stop_orders_df.to_csv('data/v2/crypto_stop_orders.csv')
        
        
def get_trade_amount_target_currency(trades_df, target_currency, dic):
    ''' Get the amount for each trade (buy or sell) in the target currency'''
    
    for i, row in trades_df.iterrows():
        pair = f'{row.currency}/{target_currency.upper()}'
        trade_forex_id = f'{i} - {pair}'
        if row.currency.upper() != target_currency.upper():
            if trade_forex_id not in dic:
                url = f'https://rest.coinapi.io/v1/exchangerate/{pair}/history?period_id=1DAY&time_start={pd.to_datetime(row.date).date()}T00:00:00&time_end={pd.to_datetime(row.date).date() + datetime.timedelta(days=1)}T00:00:00'
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
                prevailing_forex = response.json()[0]['rate_close']
                dic[trade_forex_id] = prevailing_forex 
            else:
                prevailing_forex = dic[trade_forex_id]
        else:
            prevailing_forex = 1.000000
        trades_df.loc[i,'prevailing_forex'] = prevailing_forex
        
    ''' Enables to store our dic as global variable spot_dic not to later make new API calls for the same exchange rates already asked '''
    global curr_dic
    curr_dic = dic
    
    ''' Modifying our trades_df without saving it to csv to compute the total amount sold and bought in the target currency '''
    trades_df['amount_target_currency'] = trades_df['amount'] * trades_df['prevailing_forex']
    amount_invested = round(trades_df[trades_df['b/s'] == 'Buy']['amount_target_currency'].sum(),3)
    amount_recovered = round(trades_df[trades_df['b/s'] == 'Sell']['amount_target_currency'].sum(),3)
    return amount_invested, amount_recovered

def get_portfolio_value(portfolio_df, target_currency, dic):
    ''' Computing the current value of the portfolio '''
    
    ''' Getting all the exchange rates to get the current value of the portfolio per crypto '''
    for crypto in portfolio_df['crypto']:
        pair = f'{crypto}/{target_currency.upper()}'
        if pair not in dic:
            print(f'Requesting {crypto}/{target_currency.upper()} exchange rate...')
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
            spot_price = response.json()['rate']
            print(spot_price)
            dic[pair] = spot_price

    ''' Enables to store our dic as global variable curr_dic not to later make new API calls for the same exchange rates already asked '''
    global spot_dic
    spot_dic = dic
    
    ''' Modifying our portfolio_df without saving it to csv to compute our portfolio current value in the target currency '''
    portfolio_df['target_currency'] = target_currency.upper()
    portfolio_df['pair'] = portfolio_df['crypto']+'/'+ portfolio_df['target_currency']
    portfolio_df['value_in_target_currency'] = portfolio_df['pair'].map(dic) * portfolio_df['crypto_unit']

    ''' Summing all trades profits to get the final profit '''
    final_profit = round(portfolio_df['value_in_target_currency'].sum(),3)
    return final_profit

def get_historical_profit_df(profit, currency):
    ''' Create or amend our historical profit csv file '''
    if os.path.isfile('data/v2/crypto_historical_profit.csv'):
        hist_profit_df = pd.read_csv('data/v2/crypto_historical_profit.csv', index_col=[0])
        if list(hist_profit_df.columns) != ['date','profit','currency']:
            return print('Cannot update your historical profit csv as it has not the right columns names. Please change it, remove it or move it to another folder and relaunch the program. ')
    else:
        col_list = ['date','profit','currency']
        hist_profit_df = pd.DataFrame(columns = col_list)
    date = datetime.datetime.now()
    hist_profit_df.loc[len(hist_profit_df)] = [date, profit, currency]
    if not os.path.isdir('data/v2'):
        os.makedirs('data/v2')
    hist_profit_df.to_csv('data/v2/crypto_historical_profit.csv')
    return print('Profit added to your historical profit csv. ')

def main():
    ''' Main function '''
    choice = input('Do you want to [see] your portfolio, [add] a crypto trade to your portfolio, [remove] a crypto trade from your portfolio, get your current [profit], [add_stop] market order, or [remove_stop] market order? ')  
    print("Remember to check your Stop Market orders")
    if choice not in ['see','add','remove','profit','add_stop','remove_stop']:
        print('Please enter either "see", "add", "remove", "profit", "add_stop" or "remove_stop"')
        sys.exit(1)
    else: 
        trades_df, portfolio_df, stop_orders_df = get_trades_portfolio_and_stop_orders_dfs()
        if choice == 'see':
            print_portfolios(trades_df, portfolio_df, stop_orders_df)
            print()    
        if choice == 'add':
            trades_df, portfolio_df = add_crypto_trade()
            print('Crypto trade successfully added and portfolio updated!')
            print()
        if choice == 'remove':
            remove_crypto()
            print()
            print('Crypto trade successfully removed and portfolio updated!')
            print()
        if choice == 'add_stop':
            stop_orders_df = add_stop_order()
            print('Crypto stop market order successfully added!')
            print()
        if choice == 'remove_stop':
            remove_stop_order()
            print('Crypto stop market order successfully removed!')
            print()
        elif choice == 'profit':
            trades_df, portfolio_df, stop_orders_df = get_trades_portfolio_and_stop_orders_dfs()
            if len(trades_df) == 0:
                print('Your trades history is empty! Please add crypto before computing your profit.')
            else:
                currency = input('In which currency do you want your profit? ')
                print()
                amount_invested, amount_recovered = get_trade_amount_target_currency(trades_df, currency, curr_dic)
                portfolio_value = get_portfolio_value(portfolio_df, currency, curr_dic)
                profit = round(amount_recovered + portfolio_value - amount_invested,2)
                print()
                print(f'Your current profit is:') 
                print(f'- Amount invested (total crypto bought): {amount_invested} {currency.upper()}')
                print(f'- Amount recovered (total crypto sold): {amount_recovered} {currency.upper()}')
                print(f'- Portfolio current value : {portfolio_value} {currency.upper()}')
                print(f'-- TOTAL PROFIT IS: {profit} {currency.upper()}')
                print()
                historical = pyip.inputYesNo('Would you like to add it to your historical profit csv? ')
                print()
                if historical == 'yes':
                    get_historical_profit_df(profit, currency.upper())
                    print()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python crypto_project_v2.py YourCoinAPIKey")
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
            
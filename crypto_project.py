import sys
import requests
import pandas as pd

# Generate own portfolio df
def get_crypto_df():
    crypto_df = pd.read_csv('crypto_portfolio.csv', index_col=[0])
    return crypto_df

# Add a crypto to your portfolio df
def add_crypto(df):
    date = input('Please enter date of trade (dd/mm/yy): ')
    crypto = input('Please enter crypto symbol traded: ')
    price = input('Please enter price of trade: ')
    eur_amount = input('Please enter the amount in EUR of trade: ')
    list_x = [date, crypto, float(price), float(eur_amount)]
    len_df = len(df)
    df.loc[len_df] = list_x
    df.to_csv('crypto_portfolio.csv')
    return df
    
# Adding Spot, %chg, and Profit columns
def adding_spot_profit_cols(df):

    spot_dic = {}

    for crypto in df['crypto']:
        if crypto not in spot_dic:
            print(f'Requesting {crypto} spot price...')
            url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
            headers = {'X-CoinAPI-Key' : sys.argv[1]}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print('Wrong crypto symbol added, please remove it from csv before launching the app again')
                sys.exit(1)
            spot_price = response.json()['rate']
            spot_dic[crypto] = spot_price

    df['spot_price'] = df['crypto'].map(spot_dic)
    df['pct_chg_since_trade'] = (df['spot_price'] - df['trade_price'])/df['trade_price']
    df['profit'] = df['pct_chg_since_trade']*df['amount (EUR)']
    
    return df

# Final profit
def get_final_profit(df):
    final_profit = df['profit'].sum()
    return final_profit

# Main function
def main():
    choice = input('Do you want to [add] a crypto to your portfolio or see your current [profit]? ')  
    if choice not in ['add','profit']:
        print('Please enter either "add" or "profit"')
        sys.exit(1)
    else: 
        crypto_df = get_crypto_df()
        if choice == 'add':
            crypto_df = add_crypto(crypto_df)
            print('Crypto successfully added!')
        elif choice == 'profit':
            crypto_df = adding_spot_profit_cols(crypto_df)
            print(f'Your current profit is {round(get_final_profit(crypto_df),2)} EUR')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python crypto_project.py CoinAPIKey")
        sys.exit(1)
    else:
        try:
            while True:
                main()
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit(0)
            
# crypto_project
Create your own portfolio of crypto currencies by entering each trade you made (Buy or Sell), see your current profit and keep track of your profit over time.

## **Prerequisite**

`pip install pandas`

`pip install requests`

`pip install pyinputplus`

Get a free CoinAPI Key: https://www.coinapi.io/ (free account limited to 100 requests per 24h)

## **Versions history**

- V1: enables to build a portfolio of crypto by only adding Buy orders (and not Sell orders), as well as removing some trades and getting the current value of your crypto portfolio, as well as storing it in a historical profit csv file
- V2: adding ability to enter Sell orders. Your profit is now composed of three parts: the amount recovered (amount of crypto sold) + your current outstanding crypto portfolio market value - the amount invested (amount of crypto bought). (Update Jan 2025) Also adding the possibility to register stop market orders (but won't affect your trade and portfolios dfs, for information only).

## **Usage (v2)**

Execute from terminal this way:

`python crypto_project_v2.py YourCoinAPIKey`

You will then have the possibility to either type "see", "add", "remove", "profit", "add_stop", or "remove_stop" if you want to (i) "see" your current portfolio and historical profit as well as your stop orders, (ii) "add" a crypto trade (Buy or Sell) to your portfolio, (iii) "remove" a crypto trade from your portfolio, (iv) get your current "profit" and, if you want, save it to your historical profit csv file, (v) add a stop market order (Buy or Sell), or (vi) remove a stop market order.

### See your current portfolio, stop market orders, and historical profits ###

You have nothing more to do than typing "see" when asked, and you will see (i) your trades history, (ii) your current crypto portfolio, (iii) your stop market orders, and, if it exists, (iv) your historical profits

### Add a crypto trade to your portfolio ###

If you type "add" in order to add a currency to your portfolio, you need to fill in:
- the date (YYYY/mm/dd) of trade
- the crypto symbol you bought (see here: https://en.wikipedia.org/wiki/List_of_cryptocurrencies)
- if it was a 'Buy' or 'Sell' order
- the price at which you bought a unit of the crypto (in the currency of your trade)
- the amount of your trade
- the currency of your trade

For example if you bought for 100 US dollars of Bitcoin at a price of 30,000 USD per bitcoin on June 1st 2021, then you will need to fill the form this way:

> *Please enter date of trade (dd/mm/yy): 2021/06/01*
> 
> *Please enter the crypto symbol traded (BTC, DOGE, ...): BTC*
> 
> *Please select one of: Buy, Sell: Buy*
> 
> *Please enter the price of the trade: 30000*
> 
> *Please enter the amount of your trade: 100*
> 
> *Please enter the currency symbol of your trade (EUR, USD, ...): USD*

### Remove a crypto trade from your portfolio ###

After typing "remove", your current portfolio will be displayed.
Choose the trade you want to remove by selecting its index number in the leftmost column you see (be careful, it starts at 0 and not 1!)

### Add or Remove a crypto stop market order ###

When typing "add_stop" the process is the same that for "add" unless we rather ask you the number of crypto units that will be traded if this stop market order is executed rather than the amount of the trade (this one being automatically computed).

The "remove_stop" function works in the same way as the "remove" function.


### Compute your total profit ###

If you type "profit", you will be asked the currency in which you want your profit to be displayed (EUR, USD, ...).
You will then have the option to add this profit to a csv file to keep track of your historical profits.

## **Directory structure**

In the end, after adding your first trades and adding your first historical profits to a csv as offered by the program, you will have this directory structure:

```
.
├── crypto_project_v1.py # program running the v1
├── crypto_project_v2.py # program running the v2
└── data
    ├── v1
    │   ├── crypto_historical_profit.csv # historical profits csv built with the v1
    │   └── crypto_portfolio.csv # current crypto portfolio csv built with the v1
    └── v2
        ├── crypto_historical_profit.csv # historical profits csv built with the v2
        ├── crypto_stop_orders.csv # current crypto stop orders csv built with the v2
        ├── crypto_portfolio.csv # current crypto portfolio csv built with the v2
        └── crypto_trades.csv # trades history csv built with the v2
```

Hope it helps :) !

DerSach



## **Old usage (v1)**

Execute from terminal this way:

`python crypto_project_v1.py YourCoinAPIKey`

You will then have the possibility to either type "see", "add", "remove", or "profit" if you want to (i) "see" your current portfolio and historical profit, (ii) "add" a crypto trade (onyl Buy) to your portfolio, (iii) "remove" a crypto trade from your portfolio, or (iv) get your current "profit" and, if you want, save it to your historical profit csv file

### See your current portfolio and historical profits ###

You have nothing more to do than typing "see" when asked, and you will see (i) your current crypto portfolio and, if it exists, (ii) your historical profits

### Add a crypto trade to your portfolio ###

If you type "add" in order to add a currency to your portfolio, you need to fill in:
- the date (YYYY/mm/dd) of trade
- the crypto symbol you bought (see here: https://en.wikipedia.org/wiki/List_of_cryptocurrencies)
- the price at which you bought a unit of the crypto (in the currency of your trade)
- the amount of your trade
- the currency of your trade

For example if you bought for 100 US dollars of Bitcoin at a price of 30,000 USD per bitcoin on June 1st 2021, then you will need to fill the form this way:

> *Please enter date of trade (dd/mm/yy): 2021/06/01*
> 
> *Please enter the crypto symbol traded (BTC, DOGE, ...): BTC*
> 
> *Please enter the price of the trade: 30000*
> 
> *Please enter the amount of your trade: 100*
> 
> *Please enter the currency symbol of your trade (EUR, USD, ...): USD*

### Remove a crypto trade from your portfolio ###

After typing "remove", your current portfolio will be displayed.
Choose the trade you want to remove by selecting its index number in the leftmost column you see (be careful, it starts at 0 and not 1!)

### Compute your total profit ###

If you type "profit", you will be asked the currency in which you want your profit to be displayed (EUR, USD, ...).
You will then have the option to add this profit to a csv file to keep track of your historical profits.


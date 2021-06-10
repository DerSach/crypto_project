# crypto_project
Create your own portfolio of crypto and see your current profit

## **Prerequisite**

`pip install pandas`

`pip install requests`

`pip install pyinputplus`

Get a free CoinAPI Key: https://www.coinapi.io/ (free account limited to 100 requests per 24h)

## **Usage**

Execute from terminal this way:

`python crypto_project.py YourCoinAPIKey`

You will then have the possibility to either type "see", "add", "remove", or "profit" if you want to (i) "see" your current portfolio, (ii) "add" a crypto trade to your portfolio, (iii) "remove" a crypto trade from your portfolio, or (iv) get your current "profit"

### See your current portfolio ###

You have nothing more to do than typing "see" when asked.

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

Hope it helps :) !

DerSach

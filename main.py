import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pprint import pprint as print


from aiohttp import ClientSession, ClientConnectorError


URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014'


async def request(url: str):
    async with ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.ok:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


async def get_exchange(days):
    resultation = []
    if int(days) > 10:
        print("You can not select more than 10 days")
        return resultation
    
    for i in range(int(days)+1):
        d = datetime.now() - timedelta(days=i)
        count_days = d.strftime("%d.%m.%Y")
        result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={count_days}')
        currency_dict = {}
        final_dict = {}
        for item in result['exchangeRate']:
            rate_dict ={}
            if item['currency'] == 'EUR':
                rate_dict.update({'purchase': item['purchaseRate'], 'sale': item['saleRate']})
                currency_dict.update({'EUR':rate_dict})
            
            if item['currency'] == 'USD':
                rate_dict.update({'purchase': item['purchaseRate'], 'sale': item['saleRate'],})
                currency_dict.update({'USD':rate_dict})
        final_dict.update({count_days:currency_dict})
        resultation.append(final_dict)

    return resultation


if __name__ == '__main__':
    
    days = sys.argv[1]
    result = asyncio.run(get_exchange(days))
    print(result)
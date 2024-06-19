import os
from dotenv import load_dotenv
import requests
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from .models import Transaction, Product
from sina_site.customers.models import Customer
import pandas as pd

load_dotenv()

POSTER_TOKEN = os.getenv('POSTER_TOKEN')
POSTER_URL = os.getenv('POSTER_URL')

class API():

    def __init__(self, token=POSTER_TOKEN, base_url=POSTER_URL) -> None:
        self._token = token
        self._base_url = base_url

    def get_url(self, rpc_method) -> str:
        return f'{self._base_url}{rpc_method}?token={self._token}'
    
    def get_json_request(self, rpc_method: str, quantity='one', **kwargs) -> dict:
            with requests.get(self.get_url(rpc_method), params=kwargs) as response:
                json_response = response.json()
                if json_response['response']:
                    if quantity == 'one':
                        return json_response['response'][0]
                    if quantity == 'many':
                        return json_response['response']

    def get_transactions(self, data_from: str, date_to: str, per_page: int = 1000):
        count = per_page
        page = 1

        while count == per_page:
            params = {
                'date_from': data_from,
                'date_to': date_to,
                'per_page': per_page,
                'page': page
            }
            response = self.get_json_request('transactions.getTransactions', 'many', **params)
            count = response['page']['count']
            page += 1
            yield response['data']


class Pump():
    def __init__(self) -> None:
        self.date_from = '0000-00-00'

    def pull_transaction(self) -> list:
        now = datetime.now().strftime('%Y-%m-%d')
        if Transaction.objects.exists():
            last_date_close = Transaction.objects.latest('date_close').date_close
        else:
            last_date_close = None 
        all_data = []
        api = API()

        if last_date_close:
            self.date_from = last_date_close

        for data in api.get_transactions(self.date_from, now):
            all_data.extend(data)

        return all_data[::-1]

    def synchronization_db(self):
         
         transactions = self.pull_transaction()

         for transaction in transactions:

            products = transaction['products']
            
            transaction_id = transaction['transaction_id']
            client_id = transaction['client_id']
            date_close_naive = datetime.strptime(transaction['date_close'], "%Y-%m-%d %H:%M:%S")
            date_close = timezone.make_aware(date_close_naive, timezone.get_default_timezone())
            if Customer.objects.filter(poster_id=client_id).exists():
                customer_id = Customer.objects.get(poster_id=client_id)
            else:
                customer_id = None
            try:
                transaction = Transaction.objects.create(transaction_id=transaction_id, client_id=client_id, date_close=date_close, customer_id=customer_id)
                for product in products:
                    product_id = product['product_id']
                    type = product['type']
                    product_sum = product['product_sum']
                    payed_sum = product['payed_sum']
                    try:
                        product = Product.objects.create(product_id=product_id, type=type, product_sum=product_sum, payed_sum=payed_sum)
                        transaction.product_id.add(product)
                        transaction.save()
                    except:
                        product = Product.objects.get(product_id=product_id)
                        transaction.product_id.add(product)
                        transaction.save()
            except:
                continue


class Analytics():

    def __init__(self) -> None:
        self.date_from = pd.to_datetime('1677-09-22', utc=True)
        self.date_to = pd.to_datetime(datetime.now(), utc=True)
        self.returning_clients_stats = []
    
    def get_returnability(self, date_from: datetime = None, date_to: datetime = None, **sample_per):

        if date_from:
            self.date_from = pd.to_datetime(date_from, utc=True)
        if date_to:
            self.date_to = pd.to_datetime(date_to, utc=True)

        transactions = Transaction.objects.filter(date_close__range=(self.date_from, self.date_to)).values()
        if transactions:
            df = pd.DataFrame.from_records(transactions)
            df = df.loc[df['client_id'] != 0]

            delta = relativedelta(**sample_per)

            start_date = df['date_close'].min().to_period('W').to_timestamp().replace(hour=7, minute=30)
            if 'months' in sample_per:
                start_date = df['date_close'].min().to_period('M').to_timestamp().replace(hour=7, minute=30)
            if 'years' in sample_per:
                start_date = df['date_close'].min().to_period('Y').to_timestamp().replace(hour=7, minute=30)
            start_date = pd.to_datetime(start_date).tz_localize('UTC')
            common_date = start_date + delta
            end_date = common_date + delta


            while self.date_to > (end_date - delta):
                before_period = df.loc[df['date_close'].between(start_date, common_date)]
                cleane_before_period = before_period.drop_duplicates(subset='client_id')

                period = df.loc[df['date_close'].between(common_date, end_date)]
                clean_period = period.drop_duplicates(subset='client_id')

                returned = len(pd.merge(cleane_before_period, clean_period, on='client_id'))
                one_hundred_percent = len(cleane_before_period)
                if returned == 0:
                    returnability = 0
                else:
                    returnability = round((returned / one_hundred_percent) * 100, 2)

                self.returning_clients_stats.append({
                    'count': returnability,
                    'date_from': common_date.date(),
                    'date_to': end_date.date(),
                })

                start_date += delta
                common_date += delta
                end_date += delta


        return self.returning_clients_stats

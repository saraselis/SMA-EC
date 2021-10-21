import os
import twitter

from dotenv import load_dotenv
from icecream import ic


load_dotenv()

def procura_opniao(nome: str, qtd: int) -> dict:
    api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                        consumer_secret=os.getenv('CONSUMER_SECRET'),
                        access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))

    response = api.GetSearch(term=nome, result_type='recent', count=qtd)
    tweets = {}

    for i in response:
        tweets[i.__getattribute__('id_str')] = {
            'nome_conta' : i.__getattribute__('user').__getattribute__('screen_name'),
            'tweet' : i.__getattribute__('text').replace("\n", ""),
            'data': i.__getattribute__('created_at'),
            'lang': i.__getattribute__('lang'),
        }

    return tweets

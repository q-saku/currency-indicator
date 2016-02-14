#!/usr/bin/env python

import urllib2
import json


def get_query_info(queries):
    queries_dict = {}
    yahoo_finance_api = 'https://query.yahooapis.com/v1/public/yql'
    request_header = {'User-Agent': 'finqwatcher'}
    request_env = urllib2.quote('store://datatables.org/alltableswithkeys')
    request_data = 'q=select+*+from+yahoo.finance.xchange+where+pair+="%s"&format=json&env=%s' % (queries, request_env)
    request = urllib2.Request(url=yahoo_finance_api, data=request_data,
                              headers=request_header)
    try:
        response = urllib2.urlopen(request)

        result = json.load(response)
        query = result.get("query")
        result = query.get("results").get('rate')
        if type(result) is dict:
            result = [result]
        for symbol in result:
            symbol_name = symbol['id']
            symbol_bid = symbol['Bid']
            symbol_ask = symbol['Ask']
            symbol_rate = symbol['Rate']
            symbol_time = symbol['Time']
            symbol_date = symbol['Date']
            queries_dict[symbol_name] = {'name': symbol_name,
                                         'rate': symbol_rate,
                                         'date': symbol_date,
                                         'time': symbol_time,
                                         'bid': symbol_bid,
                                         'ask': symbol_ask}
    except urllib2.HTTPError:
        print 'ERROR: Something went wrong'
    return queries_dict


def main():
    queries = 'EURUSD,EURRUB,USDRUB'
    result = get_query_info(queries)
    for symbol in result:
        print result[symbol]


if __name__ == "__main__":
    main()

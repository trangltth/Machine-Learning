from urllib import request
import constants.twitter as twitter
from datetime import datetime
from math import floor
from urllib.parse import quote_plus
import hmac, hashlib, base64, secrets
import string, re, json, codecs

def check_search_params(search_params):
    if not((search_params == '') | (search_params is None)):
        for param in search_params.split('&'):
            if(len(param.split('=')) < 2):
                raise TypeError('Invalid Search Params.')

def extract_data_from_api(url, _search_params, _method='GET'):  
    response_data = ''
    try:
        _search_params = _search_params.lstrip()
        check_search_params(_search_params)

        _oauth_timestamp = str(floor(datetime.today().timestamp()))
        _oauth_nonce = str(base64.b64encode(secrets.token_bytes(32)), 'utf-8')
        _oauth_nonce = ('').join(_group for _group in re.findall('\w*',_oauth_nonce))
        _signature = get_signature(url, _oauth_timestamp, _oauth_nonce, _search_params, _method)

        _header = {'Authorization':'''OAuth oauth_consumer_key="''' + twitter.api_key + '''", oauth_nonce="'''+ _oauth_nonce  +
            '''", oauth_signature="'''+ quote_plus(_signature) + '''", oauth_signature_method="HMAC-SHA1", oauth_timestamp="'''+ _oauth_timestamp +
            '''", oauth_token="''' + twitter.access_token + '''", oauth_version="1.0"'''}
        
        if((_search_params == '') | (_search_params is None)):
            request_url = url
        else:
            request_url = url + '?' + _search_params

        request_info = request.Request(request_url, headers=_header, method=_method)
        response_data = request.urlopen(request_info).read()
    except Exception as error:
        print('Error: ', error)
    finally:
        return response_data

def get_signature(url, _oauth_timestamp, _oauth_nonce, search_params='', _method='GET'):
    p_signature_dict = {'oauth_token': twitter.access_token, 'oauth_consumer_key': twitter.api_key, 'oauth_nonce': _oauth_nonce, 'oauth_signature_method': 'HMAC-SHA1'
                        , 'oauth_timestamp': _oauth_timestamp, 'oauth_version': '1.0'}
    p_signature = ''
    
    # 
    if not((search_params == '') | (search_params is None)):
        for param in search_params.split('&'):
            name_param = param.split('=')[0]
            value_param = param.split('=')[1]
            p_signature_dict[name_param] = value_param
    
    for key in sorted(p_signature_dict.keys()):
        _value = quote_plus(p_signature_dict[key])

        # if key == 'locations':
        #     _value = p_signature_dict[key]

        if p_signature == '':
            p_signature += quote_plus(key + '=' ) + _value
            continue

        p_signature += quote_plus('&' + key + '=') + _value

    signature_string_base = _method + '&' + quote_plus(url) + '&' + p_signature
    signature_hash = hmac.new(bytes(twitter.signing_key, 'utf-8'), msg=(signature_string_base).encode(encoding='utf-8'), digestmod=hashlib.sha1)
    signature = base64.b64encode(signature_hash.digest())
    print(p_signature)
    return signature


if __name__ == '__main__':
    search_params = 'q=' + quote_plus('list:trangletth/Data') + '&result_type=popular'    
    
    print(twitter.search_url + '?' + search_params)
    search_result = get_tweet_timeline(twitter.search_api, search_params)
    # search_result_encoder = codecs.getencoder(str(search_result))
    print(search_result)
    # print(search_result_encoder)
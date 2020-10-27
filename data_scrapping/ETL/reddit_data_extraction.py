from urllib.request import urlopen
import requests
import requests.auth

def get_authorize(input2, input1):
    # # response_data = urlopen('''https://www.reddit.com/api/v1/authorize?client_id=rzzA33eYjIPosg&response_type=code&redirect_uri=https://www.reddit.com/r/dataisbeautiful/&duration=temporary&scope=identify''')
    # # response_data = urlopen('''https://www.reddit.com/api/v1/authorize?client_id=rzzA33eYjIPosg''')
    # # print(response_data)

    # client_auth = requests.auth.HTTPBasicAuth('33cqD7jSYlirkg', 'ACgTjua26-IiyOe9tiM16hiomyk')
    # _data = {'grant_type':'password', 'code':'P@ssw0rd123', 'redirect_uri':'https://www.reddit.com/r/dataisbeautiful/'}
    # _header = {'User-Agent': 'reddit-clawer'}
    # respone = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, headers=_header, data=_data)
    # # response = requests.post('https://www.reddit.com/api/v1/access_token', headers=_header, data=_data)
    # # respone = requests.post('https://www.reddit.com/api/v1/access_token')
    # print(respone.text)
    num_days_sum = (input2 % 5000) 
    num_days = 0
    s = 0
    for i in range(0,45):
        s += i
        num_days = i
        if (num_days_sum == s):
            break

    label = (input2 - (5000 * num_days) - num_days_sum) / 5000
    return label

if __name__ == '__main__':
    # get_authorize()
    # Write code here
    print(25003 % 5000)
    print(get_authorize(25003,4))
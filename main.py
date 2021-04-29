import requests
from bs4 import BeautifulSoup

URL = 'https://freelancehunt.com/projects?name=бот'
username = 'IATWUkS'
password = 'Phon88ph228'


def request_site(url):
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    session = requests.Session()
    answer = session.post('https://freelancehunt.com/profile/login', headers=headers, data={'_qf__login_form': '',
                                                                           'qf:token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJoYXNoIjoiMTUwOWFiNzBkNmEyZDMxOWVjNDU3ZmI3ZjQ2YTg5MzMiLCJleHAiOjE2MTk3OTk5ODMsImlhdCI6MTYxOTcxMzU4M30.nikkbkfn4Yqj9A9piLRq4MVe-OrvUQc66J3zE2gx_PI',
                                                                           'login': username, 'password': password,
                                                                           'remember_me': '1', 'save': ''})
    answer = session.get(url)
    bs = BeautifulSoup(answer.text, 'html.parser')
    return bs


def get_name_url(bs):
    list_name = []
    list_url = []
    pars_table = bs.find('table', class_='table table-normal project-list')
    for name_url in pars_table.findAll('a', class_='bigger visitable'):
        list_name.append(name_url.text)
        list_url.append(name_url.get('href'))
    return list_name, list_url


def get_time(bs):
    list_time = []
    pars_table = bs.find('table', class_='table table-normal project-list')
    for time in pars_table.findAll('div', class_='with-tooltip'):
        try:
            list_time.append(time.find('h2').text + ' ' + time.find('h5').text)
        except:
            try:
                list_time.append(time.find('h2').text)
            except:
                pass
    return list_time


def get_cout_type(bs):
    cout_worker = []
    type = []
    pars_table = bs.find('table', class_='table table-normal project-list')
    for cout in pars_table.findAll('a', class_='text-orange price'):
        cout_worker.append(cout.text)
    for type_en in pars_table.findAll('td', class_='left'):
        try:
            type.append(type_en.find('small').text)
        except:
            pass
    return cout_worker, type

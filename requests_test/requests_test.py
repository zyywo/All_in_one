import requests

url = 'http://tieba.baidu.com/home/main?id=c95f7a79796d796264aa0a?t=1422943285&fr=userbar&red_tag=z3547255234'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
jar = requests.cookies.RequestsCookieJar()

r = requests.get(url, headers=headers)

print(r.cookies)
print(r.text)

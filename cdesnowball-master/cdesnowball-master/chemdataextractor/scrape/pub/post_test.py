import requests

pload = {'username':'Olivia','password':'123'}
r = requests.post('https://httpbin.org/post',data = pload)
print(r.text)
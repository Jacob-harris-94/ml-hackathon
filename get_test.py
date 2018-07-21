from requests import get

url = 'https://en.wikipedia.org/wiki/Computer_security'

response = get(url)
#print(response.text[:500])

with open ("test.html", 'wb') as f_out:
    f_out.write(response.text.encode('utf-8'))

print("done")

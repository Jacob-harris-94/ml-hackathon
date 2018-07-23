from requests import get
from bs4 import BeautifulSoup

#url = 'https://en.wikipedia.org/wiki/Computer_security'
url = 'https://en.wikipedia.org/wiki/Helmeted_gecko'

response = get(url)
#print(response.text[:500])

with open ("outputs/test.html", 'wb') as f_out:
    f_out.write(response.text.encode('utf-8'))

print("saved off html")

html_soup = BeautifulSoup(response.text, 'html.parser')
print(type(html_soup))

text = html_soup.get_text();
print("===================================================================")
print("text:")
print(text)
print("===================================================================")

print("===================================================================")
print("links:")
links = html_soup.find_all('a')
for link in links:
    print(link.get('href'))
print(f'number of links: {len(links)}')
print("===================================================================")

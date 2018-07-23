from requests import get
from bs4 import BeautifulSoup

def get_text_and_hrefs_from_url(url, print_url=False):
    if print_url:
        print('visiting: ' + url)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    text_only = html_soup.get_text()
    anchors = html_soup.find_all('a')
    urls = []
    for anchor in anchors:
        urls.append(anchor.get('href'))
    return [text_only, urls]

def get_text_and_hrefs_from_url_recursively(url, n=0):

    if n > 0:
        # wrap up results
        # [text_only, urls]
        txt_urls_pair = get_text_and_hrefs_from_url(url, print_url=True)
        url_list = txt_urls_pair[1]
        print('url_list' + str(url_list))
        txt_url_pairs =[]
        for url in url_list:
            if url != None and url[0:5+1] == '/wiki/':
                url = url.replace('/wiki/', 'https://en.wikipedia.org/wiki/')
                txt_url_pairs.append(get_text_and_hrefs_from_url_recursively(url, n-1))
        print(f'recursed {n} times')
        return txt_url_pairs
    else:
        # base case (only 1 url)
        # [text_only, urls]
        return get_text_and_hrefs_from_url(url, print_url=True)


if __name__ == '__main__':
    #url = 'https://en.wikipedia.org/wiki/Computer_security'
    print("===================================================================")
    # one of the shortest pages... only a few links to other pages!
    url = 'https://en.wikipedia.org/wiki/Helmeted_gecko'
    print(f'url: {url}')
    text_and_links = get_text_and_hrefs_from_url_recursively(url, 2)
    print("===================================================================")

    #print(text_and_links)

    #print(f'text_only: {text_and_links[0]}')
    #print("===================================================================")
    #print(f'links: {text_and_links[1]}')
    #print(f'number of links: {len(text_and_links[1])}')
    #print("===================================================================")

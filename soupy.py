from bs4 import BeautifulSoup
import requests
import requests_cache

# requests_cache is a monkey patched update to requests to enable caching
# requested pages so that we can work with a page without hitting the client's
# api or using up bandwidth. use requests as normal after calling .install_cache

requests_cache.install_cache(
    cache_name='nobel_prizes',
    backend='sqlite',
    expire_after=7200)

BASE_URL = 'https://en.wikipedia.org'
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_nobel_soup():
    """ Return a parsed tag tree of our nobel prize page. """

    response = requests.get(
        BASE_URL + '/wiki/List_of_Nobel_laureates',
        headers=HEADERS)
    return BeautifulSoup(response.content, "lxml")


def get_column_titles(table):
    """ Get Nobel categories fom table header """
    cols = []
    for th in table.select_one('tr').select('th')[1:]:
        link = th.select_one('a')
        # store the category name and any Wikipedia link it has
        if link:
            cols.append({
                'name': link.text,
                'href': link.attrs['href']})
        else:
            cols.append({'name': th.text, 'href': None})

    return cols


def get_nobel_winners(table):
    cols = get_column_titles(table)
    winners = []
    for row in table.select('tr')[1:-1]:
        year = int(row.select_one('td').text)
        for i, td in enumerate(row.select('td')[1:]):
            for winner in td.select('a'):
                href = winner.attrs['href']
                if not href.startswith('#endnote'):
                    winners.append({
                        'year': year,
                        'category': cols[i]['name'],
                        'name': winner.text,
                        'link': winner.attrs['href']
                    })
                else:
                    print(href)
    return winners


def get_winner_nationality(winner):
    """ scrape biographic data from the winner's wikipedia page """
    url = BASE_URL + winner['link']
    data = requests.get(url=url, headers=HEADERS)
    print(url)
    soup = BeautifulSoup(data.content, "lxml")
    person_data = {'name': winner['name'],
                   'nationality': None}
    attr_rows = soup.select('table.infobox tr')

    for tr in attr_rows:
        try:
            attribute = tr.select_one('th').text
            if attribute == 'Nationality':
                person_data['nationality'] = tr.select_one('td').text
        except AttributeError:
            print("No nationality for " + winner['name'])

    return person_data


def check_nationalities(winners):
    success = 0
    fail = 0

    for w in winners:
        data = get_winner_nationality(winner=w)
        nationality = data['nationality']
        w['nationality'] = nationality
        if nationality:
            success += 1
        else:
            fail += 1
    print("Found data for: " + str(success) + " winners")
    print("No data for: " + str(fail) + " winners")

    return winners

def frequency_counter(list, attr):
    freqs = dict()

    for item in list:
        attribute = item[attr]
        if attribute in freqs:
            freqs[attribute] += 1
        else :
            freqs[attribute] = 1

    return freqs

soup = get_nobel_soup()

# soup's find method is a bit fragile, ex: 'sortable wikitable' would fail below
# soup.find('table', {'class': 'wikitable sortable'})

# but we can use lxml's select which also allows for css selectors, regex, and
# html tag names plus additional methods.

table = soup.select_one('table.sortable.wikitable')
winners = get_nobel_winners(table=table) # needs to be deduped for folks listed in mutliple places

winners = check_nationalities(winners=winners)



list_xpath = "//*[@id='mw-content-text']/div[1]/table"

from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.parse import quote
from utils.utils import make_request
from utils.config import SEASON_IDS, SCOREBOARD_URL


def get_match_ids(url):
    # Array to store all the match ids
    match_ids = []

    # Get the response from the url
    response = make_request(url)

    if response is None:
        return

    # Set up BeautifulSoup
    soup = BeautifulSoup(response, 'html.parser')

    # All of the matchs ids are in 'tr' tags, so we need to get all of them
    tr_tags = soup.find_all('tr')
    for tag in tr_tags:
        id_val = tag.get('id')
        if id_val and id_val.startswith('contest_'):
            match_id = id_val.replace('contest_', '')
            match_ids.append(match_id)
    
    return set(match_ids)

def get_all_match_ids(season_id):
    years = SEASON_IDS[season_id]
    start_year, end_year = years.split('-')
    
    start_date = date(int(start_year), 2, 1)
    #end_date = date(int(end_year), 1, 15)
    end_date = start_date + timedelta(days=10)

    matches = [] 

    current = start_date
    while current <= end_date:
        date_string = quote(current.strftime('%m/%d/%Y'))
        url = SCOREBOARD_URL.format(season_id=season_id, date=date_string)
        matches.append(get_match_ids(url))
        current += timedelta(days=1)
    
    all_ids = set()
    while current <= end_date:
        result = get_match_ids(url)
        if result:
            all_ids.update(result)
        current += timedelta(days=1)
    return all_ids

if __name__ == "__main__":
    arr = get_all_match_ids(16760)
    print(arr)
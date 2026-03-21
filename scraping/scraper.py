from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.parse import quote
from utils.utils import make_request
from utils.config import SEASON_IDS, SCOREBOARD_URL, SEASON_DIVISIONS, BOXSCORE_URL

# ------------------ MATCH IDS --------------------
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
    start_date = date(int(end_year), 1, 1)
    end_date = date(int(end_year), 4, 30)

    # Iterate through SEASON_DIVISIONS to get divison_id
    division_id = 0
    for div_id, div_years in SEASON_DIVISIONS.items():
        if div_years == years:
            division_id = div_id

    current = start_date
    all_ids = set()
    while current <= end_date:
        date_string = current.strftime('%m%%2f%d%%2f%Y')
        print(date_string)
        url = SCOREBOARD_URL.format(division_id=division_id, date=date_string)
        result = get_match_ids(url)
        if result:
            all_ids.update(result)
        current += timedelta(days=1)
    return all_ids

# ------------------ GAME STATS --------------------
def get_game_stats(match_id):
    game_stats = {
        'team1_name': '', 'team1_id': '', 'team1_sets': '',
        'team2_name': '', 'team2_id': '', 'team2_sets': '',
        'winner_id': '',
        'date': '', 'location': '',
        'team1_stats': {'kills': 0, 'errors': 0, 'attacks': 0, 'hitting_pct': 0.0, 'digs': 0, 'blocks': 0.0, 'aces': 0, 'service_errors': 0},
        'team2_stats': {'kills': 0, 'errors': 0, 'attacks': 0, 'hitting_pct': 0.0, 'digs': 0, 'blocks': 0.0, 'aces': 0, 'service_errors': 0},
    }

    url = BOXSCORE_URL.format(match_id=match_id)
    response = make_request(url)

    if response is None:
        return
    
    soup = BeautifulSoup(response, 'html.parser')

    # Find the team names and IDs, then add them to the game stats dictionary 
    team_dict = {}
    team_tags = soup.find_all('a', class_='skipMask')
    for tag in team_tags:
        href_val = tag.get('href')
        if href_val and href_val.startswith('/teams/'):
            team_id = href_val.split('/teams/')[1]
            if team_id not in team_dict.keys() and tag.text.strip():
                team_dict[team_id] = tag.text.strip()
    teams = list(team_dict.items())
    print(teams)
    game_stats['team1_id'], game_stats['team1_name'] = teams[0]
    game_stats['team2_id'], game_stats['team2_name'] = teams[1]

    return game_stats
    

if __name__ == "__main__":
    print(get_game_stats(6081819))
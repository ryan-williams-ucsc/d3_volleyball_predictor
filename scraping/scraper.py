from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.parse import quote
from utils.utils import make_request
from utils.config import SEASON_IDS, SCOREBOARD_URL, SEASON_DIVISIONS, BOXSCORE_URL
from database.schema import insert_match, insert_team, insert_team_stats

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

    total_days = (end_date - start_date).days + 1
    current = start_date
    all_ids = set()
    day_num = 0
    while current <= end_date:
        day_num += 1
        date_string = current.strftime('%m%%2f%d%%2f%Y')
        print(f'Date {day_num}/{total_days}: {date_string}')
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
    game_stats['team1_id'], game_stats['team1_name'] = teams[0]
    game_stats['team2_id'], game_stats['team2_name'] = teams[1]

    # Get the number of sets each team won + winner
    sets_list = []
    set_tags = soup.find_all('td')
    for tag in set_tags:
        style_val = tag.get('style')
        if style_val and 'font-size:36px' in style_val:
            sets_list.append(tag.text.strip())   
    game_stats['team1_sets'] = sets_list[0]
    game_stats['team2_sets'] = sets_list[1]
    if int(sets_list[0]) > int(sets_list[1]):
        game_stats['winner_id'] = game_stats['team1_id']
    else:
        game_stats['winner_id'] = game_stats['team2_id']

    # Get the location
    date_list = []
    date_tags = soup.find_all('td', class_='grey_text')
    for tag in date_tags:
        if 'colspan' in tag.attrs and tag.text.strip():
            date_list.append(tag.text.strip())
    game_stats['date'] = date_list[0]
    game_stats['location'] = date_list[1]

    # Fill in the stats dictionary for both teams
    stat_map = {
        'Kills': 'kills',
        'Errors': 'errors', 
        'Attacks': 'attacks',
        'Hitting Pct': 'hitting_pct',
        'Digs': 'digs',
        'Total Blocks': 'blocks',
        'Aces': 'aces',
        'Service Errors': 'service_errors'
    }
    stats_table = soup.find('table', id='team_stats_table')
    nested_table = stats_table.find_all('table', class_='display dataTable')
    for table in nested_table:
        stat_name = table.find('th').text.strip()
        stat_vals = table.find_all('td', {'width': '5%'})
        if stat_map.get(stat_name):
            if stat_map.get(stat_name) == 'hitting_pct' or stat_map.get(stat_name) == 'blocks':
                game_stats['team1_stats'][stat_map.get(stat_name)] = float(stat_vals[0].text.strip())
                game_stats['team2_stats'][stat_map.get(stat_name)] = float(stat_vals[1].text.strip())
            else:
                game_stats['team1_stats'][stat_map.get(stat_name)] = int(stat_vals[0].text.strip())
                game_stats['team2_stats'][stat_map.get(stat_name)] = int(stat_vals[1].text.strip())

    return game_stats
    
# ------------------ UPDATE DB ---------------------
def scrape_season(season_id):
    matches = get_all_match_ids(season_id)

    print("total matches found:", len(matches))

    for i, match in enumerate(matches, 1):
        print(f'Match {i}/{len(matches)}:', match)
        game_stats = get_game_stats(match)
        if game_stats is None:
            continue
        # Insert teams from every match
        # Dont need to worry about duplicates, handled inside functions
        insert_team(game_stats['team1_id'], game_stats['team1_name'])
        insert_team(game_stats['team2_id'], game_stats['team2_name'])
        # Insert every match
        insert_match(match, season_id, game_stats)
        # Insert team stats for both teams
        insert_team_stats(match, game_stats['team1_id'], game_stats)
        insert_team_stats(match, game_stats['team2_id'], game_stats)

if __name__ == "__main__":
    print(scrape_season(16760))
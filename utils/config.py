# Base URL for stats.ncaa.org
BASE_URL = 'https://stats.ncaa.org/'
SCOREBOARD_URL = 'https://stats.ncaa.org/season_divisions/{division_id}/livestream_scoreboards?game_date={date}'
# Database path
DB_PATH = 'database/volleyball.db'
# Delay between web requests
REQUEST_DELAY = 1.5
# Dict mapping season ID to years
SEASON_IDS = {
    17001: "2025-2026",
    16760: "2024-2025",
    16560: "2023-2024",
    16380: "2022-2023",
    15920: "2021-2022",
    15562: "2020-2021",
    15020: "2019-2020",
    14383: "2018-2019",
    12825: "2017-2018",
    12582: "2016-2017",
    12382: "2015-2016",
    12100: "2014-2015",
    11600: "2013-2014",
    11360: "2012-2013",
    10800: "2011-2012",
    10540: "2010-2011",
    10481: "2009-2010",
    11000: "2008-2009",
}

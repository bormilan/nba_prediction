# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 10:48:03 2021

@author: milan
"""

from nba_api.stats.static import teams
teams_dict = teams.get_teams()

from nba_api.stats.endpoints import teamgamelog

teamB = "Los Angeles Lakers"
teamA = "Chicago Bulls"

#bulls' object and id
team_obj = [team for team in teams_dict if team["full_name"] == teamA][0]
team_id = team_obj["id"]

 #test section
#-------------------
suns_obj = [team for team in teams_dict if team["full_name"] == "Phoenix Suns"][0]
suns_id = suns_obj["id"]
suns_log = teamgamelog.TeamGameLog(team_id=suns_id).get_data_frames()[0]
suns_percentage = suns_log["W_PCT"][0]

#imports for the players and player stats
from nba_api.stats.static import players
players_dict = players.get_active_players()
from nba_api.stats.endpoints import playercareerstats

#devin's stats and its a way to find a players stat dynamically
devin_id = players.find_players_by_full_name("Devin Booker")[0]["id"]
devin_stat = playercareerstats.PlayerCareerStats(player_id=devin_id).get_normalized_dict()["SeasonTotalsRegularSeason"]
#devin_temp_stat = devin_stat["SeasonTotalsRegularSeason"]
devin_2021_stat = [stat for stat in devin_stat if stat["SEASON_ID"] == "2020-21"][0]
devin_pts = devin_2021_stat["PTS"]
#-------------------

#bulls' game log
team_log = teamgamelog.TeamGameLog(team_id=team_id).get_data_frames()[0]
teamA_percentage = team_log["W_PCT"][0]
aaaaaa = team_log["GAME_DATE"][0]

#a team's starting lineup for every game
from nba_api.stats.endpoints import teamdashlineups
lineup = teamdashlineups.TeamDashLineups(team_id=team_id).get_data_frames()[1]

import datetime
#zach's data
zach = [player for player in players_dict if player["full_name"] == "Zach LaVine"][0]
zach_id = zach["id"]
from nba_api.stats.endpoints import playergamelog
zach_log = playergamelog.PlayerGameLog(zach_id).get_normalized_dict()["PlayerGameLog"]
date_time = datetime.datetime.strptime("MAR 10, 2021", "%b %d, %Y") 
zach_log_2 = [stat for stat in zach_log if datetime.datetime.strptime(stat["GAME_DATE"], "%b %d, %Y") < date_time]
zach_ast = sum([stat["AST"] for stat in zach_log_2])
zach_stat = playercareerstats.PlayerCareerStats(player_id=zach_id).get_normalized_dict()
zach_2021_stat = zach_stat["SeasonTotalsRegularSeason"][6]
zach_pts = zach_2021_stat["PTS"]

#how many points a player gives a team
def pts_of_player(name):
    pts = 0
    player_id = players.find_players_by_full_name(name)[0]["id"]
    player_stat = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict()["SeasonTotalsRegularSeason"]
    player_2021_stat = [stat for stat in player_stat if stat["SEASON_ID"] == "2020-21"][0]
    pts += player_2021_stat["AST"]
    pts += player_2021_stat["REB"]
    pts += player_2021_stat["PTS"]
    pts += player_2021_stat["BLK"]
    pts += player_2021_stat["STL"]
    pts += player_2021_stat["PTS"] / player_2021_stat["MIN"]
    
    return pts / 100

def pts_of_team(team):
    pts = 0
    team_id = teams.find_teams_by_full_name(team)[0]["id"]
    team_log = teamgamelog.TeamGameLog(team_id=team_id).get_data_frames()[0]
    
    return team_id
    
stephen_id = pts_of_player("Giannis Antetokounmpo")
pts_of_team = pts_of_team("Chicago Bulls")

from nba_api.stats.endpoints import leaguegamelog
gr = leaguegamelog.LeagueGameLog(season="2020").get_data_frames()

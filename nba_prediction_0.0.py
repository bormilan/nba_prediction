# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:45:17 2021

@author: milan
"""
import datetime
import numpy as np

from nba_api.stats.static import teams
teams_dict = teams.get_teams()
from nba_api.stats.static import players
players_dict = players.get_active_players()


from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import teamdashlineups
from nba_api.stats.endpoints import playergamelog

#how many points a player gives a team
def pts_of_player(player_id):
    pts = 0
    player_log = playergamelog.PlayerGameLog(player_id).get_normalized_dict()["PlayerGameLog"]
    player_log_by_date = [stat for stat in player_log if datetime.datetime.strptime(stat["GAME_DATE"], "%b %d, %Y") < date_time]
    pts += np.sum([stat["AST"] for stat in player_log_by_date])
    pts += np.sum([stat["REB"] for stat in player_log_by_date])
    pts += np.sum([stat["PTS"] for stat in player_log_by_date])
    pts += np.sum([stat["BLK"] for stat in player_log_by_date])
    pts += np.sum([stat["STL"] for stat in player_log_by_date])
    pts += np.sum([stat["PTS"] for stat in player_log_by_date]) / np.sum([stat["MIN"] for stat in player_log_by_date])
    
    return pts / 100

#how many points the win percentage gives a team
def pts_of_team(team):
    team_games = teamgamelog.TeamGameLog(team_id=team["id"]).get_normalized_dict()["TeamGameLog"]
    team_pct = [game["W_PCT"] for game in team_games if datetime.datetime.strptime(game["GAME_DATE"], "%b %d, %Y") <= date_time][0]
    return team_pct*10
   
#how many points the matchup gives a team 
def pts_of_matchup(team1,team2):
    team_id = teams.find_teams_by_full_name(team1)[0]["id"]
    team_games = teamgamelog.TeamGameLog(team_id=team_id).get_normalized_dict()["TeamGameLog"] 
    
    opponent_abb =teams.find_teams_by_full_name(team2)[0]["abbreviation"]
    games_by_opponent = [game for game in team_games if game["MATCHUP"].split(" ")[2] == opponent_abb and datetime.datetime.strptime(game["GAME_DATE"], "%b %d, %Y") <= date_time]
    wins_by_opponent = [game for game in games_by_opponent if game["WL"] == "W"]
    if games_by_opponent == []:
        return 0
    return (len(wins_by_opponent) / len(games_by_opponent))*10

def who_win(team1,team2):
    lineup1 = teamdashlineups.TeamDashLineups(team_id=team1["id"]).get_normalized_dict()["Lineups"][0]["GROUP_ID"].strip("-").split("-")
    lineup2 = teamdashlineups.TeamDashLineups(team_id=team2["id"]).get_normalized_dict()["Lineups"][0]["GROUP_ID"].strip("-").split("-")
    # print(teamdashlineups.TeamDashLineups(team_id=team1["id"]).get_normalized_dict()["Lineups"][0]["GROUP_NAME"])
    # print(teamdashlineups.TeamDashLineups(team_id=team2["id"]).get_normalized_dict()["Lineups"][0]["GROUP_NAME"])
    #1
    pts_team1 = 0
    pts_team2 = 0
    pts_team1 = pts_of_matchup(team1["full_name"],team2["full_name"])
    pts_team2 = pts_of_matchup(team2["full_name"],team1["full_name"])
    #2
    pts_team1 += pts_of_team(team1)
    pts_team2 += pts_of_team(team2)
    #3
    pts_team1 += np.sum([pts_of_player(player_id) for player_id in lineup1])
    pts_team2 += np.sum([pts_of_player(player_id) for player_id in lineup2])
    
    print(pts_team1," - ",pts_team2)
    print(team1["full_name"]," - ",team2["full_name"])
    
team1 = [team for team in teams_dict if team["full_name"] == "Miami Heat"][0]
team2 = [team for team in teams_dict if team["full_name"] == "Chicago Bulls"][0]
date_time = datetime.datetime.strptime("MAR 12, 2021", "%b %d, %Y")
who_win(team1,team2)
# The purpose of this program is to determine tiebreakers for division winners
# in the International League of the MILB (minor league baseball).
# The first tiebreaker is head to head win percentage among all teams tied.
# If teams are still tied after that, whichever team has a better win pct in
# its last 20 games is the winner.
# If there's still a tie, then it goes to 21 games, 22 and so on until someone
# emerges as the winner. Each team in the International League plays 150 games per season.
# In my simulated dataset, each team plays 28 games, so I set the tiebreaker number of games to 4.

# I - Module import and initalization of constants
import pandas as pd
import random
import numpy as np
teams = ["WAS","BOS","NY","SD","MIA","CHI","DEN","SEA"] # not the actual teams in the International League
full_names = {"WAS":"Washington", "BOS":"Boston", "NY":"New York",
              "SD":"San Diego","MIA":"Miami","CHI":"Chicago",
              "DEN":"Denver","SEA":"Seattle"} # used for nice printing of information
scores = list(range(11)) # scores of games; used to determine winners
games_played_list = [] # used to set correct number of home-away combos for all pairs
NUM_GAMES = 28
FULL_SEASON = 112
# add rows to this empty one to get all games in season
games_df = {
    'home_team': [],
    'away_team': [],
    'home_score': [],
    'away_score': [],
}
games_df = pd.DataFrame(games_df)

# II - Create data frame of games played for whole season
while len(games_played_list) < FULL_SEASON:
    one_game = random.sample(teams,2) + random.sample(scores,2)
    if games_played_list.count(one_game[0]+"-"+one_game[1]) < 2: # each team plays 2 home and 2 away games against each opponent
        games_played_list.append(one_game[0]+"-"+one_game[1])
        pd_dict = {'home_team':[one_game[0]], # value needs to be list to be converted into data frame
               'away_team':[one_game[1]],
               'home_score':[one_game[2]],
               'away_score':[one_game[3]],
              }
        added_df = pd.DataFrame(pd_dict)
        games_df = pd.concat([games_df,added_df])
    else: continue # don't add game if team has played other team home or away twice. Come up with new combo

games_df = games_df.astype(dtype={'home_score': int, 'away_score': int}) # baseball scores can only be integers

# III - Determine win percentage for all teams
win_pct_dict = {}
def determine_win_pct(team,reference_df): # function determines winning pct for a team from a df of games
    """DETERMINES WINNING PERCENTAGE FOR A TEAM. INPUT AS A DATA FRAME OF GAMES"""
    wp_dict = {}
    temp_games = reference_df[(reference_df['home_team'] == team) | (reference_df['away_team'] == team)]
    temp_wins = temp_games[(((temp_games['home_team'] == team) & (temp_games['home_score'] > temp_games['away_score'])) | \
                ((temp_games['away_team'] == team) & (temp_games['away_score'] > temp_games['home_score'])))]
    wp_dict[team] = round((temp_wins.shape[0] / temp_games.shape[0]),3)
    return wp_dict

for team in teams:
    win_pct_dict[team] = determine_win_pct(team,games_df)[team] # dictionary keys are team abbreviations; vals are winning percentages

# for nice output - used throughout:
formatted_season_dict = {full_names[key]:val for key,val in win_pct_dict.items()}
ordered_season_dict = dict(sorted(formatted_season_dict.items(), key = lambda x: x[1], reverse=True)) # sort by descending value of win pct
print("Season win percentages:\n",ordered_season_dict)

# IV - Determine if there's a tie for first place
def make_winners_df(dict_of_win_pcts):
    """CREATES DATA FRAME OF ALL TEAMS WITH HIGHEST WINNING PERCENTAGE"""
    win_pct_list = []
    team_indexes = []
    for i,j in dict_of_win_pcts.items(): # turn team abbreviations into row index lables; turn win % into values of win % column
        win_pct_list.append(j)
        team_indexes.append(i)
    win_pct_df = pd.DataFrame({"Win_Pct" : win_pct_list}, index=team_indexes)
    win_pct_df = win_pct_df.sort_values(by="Win_Pct", ascending = False)

# see if there's a tie for highest win %
    highest_win_pct = win_pct_df['Win_Pct'].max()
    winners_df = win_pct_df["Win_Pct"] == highest_win_pct
    winners_df = win_pct_df[winners_df]
    return winners_df, win_pct_df

winners_df, win_pct_df = make_winners_df(win_pct_dict)

if winners_df.shape[0] == 1: # if no tie, winner is declared
    winner = win_pct_df['Win_Pct'].idxmax()
    print(full_names[winner],"wins the division")

# V - Tiebreak based on head to head of all tied teams
else:
    tied_teams = [winners_df.index[i] for i in range(winners_df.shape[0])] # get list of all tied teams
    print("The following teams are tied for first:")
    for team in tied_teams: print(full_names[team])
    tiebreaker_df = {
    'home_team': [],
    'away_team': [],
    'home_score': [],
    'away_score': [],
    }
    tiebreaker_df = pd.DataFrame(tiebreaker_df) # can add indexes if printing this df; just zeroes for now - same throughout
    h2h_win_pct_dict = {}
    # get all games each team played against the other tied teams. Don't need to do last team b/c their games are covered by the other teams
    tied_teams_2, tied_teams_3 = tied_teams.copy(), tied_teams.copy()
    while len(tied_teams) > 1:
        tied_teams_2.remove(tied_teams_2[0])
        for j in range(len(tied_teams_2)):
            temp_games = (((games_df['home_team'] == tied_teams[0]) & (games_df['away_team'] == tied_teams_2[j])) | \
                     ((games_df['away_team'] == tied_teams[0]) & (games_df['home_team'] == tied_teams_2[j])))
            temp_games = games_df[temp_games]
            tiebreaker_df = pd.concat([tiebreaker_df,temp_games])

        #get team's win pct in head to head against other tied teams
        h2h_win_pct_dict_add = determine_win_pct(tied_teams[0],tiebreaker_df)
        h2h_win_pct_dict = {**h2h_win_pct_dict, **h2h_win_pct_dict_add}
        tied_teams.remove(tied_teams[0])

    # now need to get last team's win pct. Only one team left in list, so can use [0]
    last_team_dict = determine_win_pct(tied_teams[0],tiebreaker_df)
    h2h_win_pct_dict = {**h2h_win_pct_dict, **last_team_dict}
    tiebreaker_df = tiebreaker_df.astype(dtype={'home_score': int, 'away_score': int}) # if printing
    formatted_h2h_dict = {full_names[key]:val for key,val in h2h_win_pct_dict.items()}
    ordered_h2h_dict = dict(sorted(formatted_h2h_dict.items(), key = lambda x: x[1], reverse=True)) # sort by descending value of win pct
    print("Winning percentages in games among tied teams:\n",ordered_h2h_dict)

    # Get highest win percentage. Declare winner if only one team has that value
    win_pct_list = [val for val in h2h_win_pct_dict.values()]
    if win_pct_list.count(max(win_pct_list)) == 1:
        tiebreak_winner = [key for key in h2h_win_pct_dict if h2h_win_pct_dict[key] == max(win_pct_list)]
        print(full_names[tiebreak_winner[0]],"wins based on head to head among all tied teams")

# VI - proceed to tiebreaker based on last 4 (or more) games
    else:
        def last_n_tiebreaker(teams_in_tie): # recursive function. If tie not broken after 4 games, add 1 and try again until tie is broken
            """RECURSIVE FUNCTION WHICH CHECKS WINNING PERCENTAGE OF ALL TIED TEAMS IN LAST 4 GAMES.
            IF STILL TIED, ADDS ONE GAME AND CHECKS AGAIN. CONTINUES UNTIL TIE IS BROKEN."""
            TIEBREAKER_GAMES = 4
            last_n_win_pct_dict = {}
            # get last n games (based on value of TIEBREAKER_GAMES) for each team
            for team in teams_in_tie:
                last_n_temp_games = games_df[(games_df['home_team'] == team) | (games_df['away_team'] == team)]
                last_n_games = last_n_temp_games[(TIEBREAKER_GAMES)*-1:]
                last_n_games = last_n_games.astype(dtype={'home_score': int, 'away_score': int})
                # get win pct in last n games
                last_n_win_pct_dict[team] = determine_win_pct(team,last_n_games)[team]
            formatted_last_n_dict = {full_names[key]:val for key,val in last_n_win_pct_dict.items()}
            ordered_last_n_dict = dict(sorted(formatted_last_n_dict.items(), key = lambda x: x[1], reverse=True)) # sort by descending value of win pct
            print("Winning percentages in last",TIEBREAKER_GAMES,"games:\n",ordered_last_n_dict)
            # make df for win pct of last n games for all teams involved
            last_n_winners_df, last_n_win_pct_df = make_winners_df(last_n_win_pct_dict)

            if last_n_winners_df.shape[0] == 1: # if no tie, winner is declared
                last_n_winner = last_n_winners_df['Win_Pct'].idxmax()
                print("Winner is",full_names[last_n_winner],"by virtue of win percentage" \
                " in last",TIEBREAKER_GAMES,"games")
            else:
                TIEBREAKER_GAMES += 1
                last_n_tiebreaker(teams_in_tie)

        last_n_tiebreaker(tied_teams_3) # will proceed until winner is determined!

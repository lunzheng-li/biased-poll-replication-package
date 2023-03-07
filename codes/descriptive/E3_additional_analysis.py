import pandas as pd              # 'Pandas' is Python's main library for data analysis
import numpy as np
from scipy import stats
# This module allows to specify the path to chosen files
import tkinter.filedialog as tk
import matplotlib.pyplot as plt  # Used for plotting and visualising
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import os
import math

# The tinker module is not working Mac very well. Let's read the data using the following way.
os.chdir('../../E3_data')

York_TREAT = pd.read_excel('E3_Treatment.xlsx')

York_CONTROL = pd.read_excel('E3_Control.xlsx')

# Save data from different sessions in dictionary
York_2019_PollsData = {}

TR_SESSIONS = ['E3_T1', 'E3_T2', 'E3_T3', 'E3_T4',
               'E3_T5']  # We name the 8 sessions we conducted
CT_SESSIONS = ['E3_C1', 'E3_C2', 'E3_C3', 'E3_C4']
Sessions = TR_SESSIONS + CT_SESSIONS

i = 0
for s in TR_SESSIONS:
    York_2019_PollsData[s] = York_TREAT.iloc[i:i + 270]
    i = i + 270


i = 0
for s in CT_SESSIONS:
    York_2019_PollsData[s] = York_CONTROL.iloc[i:i + 270]
    i = i + 270
# For tractability let us choose the variables that we are interested in:

relevant_var_tr = ['player.id_position', 'participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
                   'group.practice_round_number', 'group.quality_J', 'group.k_inelection', 'group.j_inelection', 'group.winner', 'group.quality_K',
                   'group.companyA_k_inpolls', 'group.companyB_k_inpolls', 'group.companyC_k_inpolls', 'group.companyD_k_inpolls', 'group.companyE_k_inpolls',
                   'group.companyA_j_inpolls', 'group.companyB_j_inpolls', 'group.companyC_j_inpolls', 'group.companyD_j_inpolls', 'group.companyE_j_inpolls',
                   'group.biased1_company', 'group.biased2_company', 'group.biased1_j_inpolls', 'group.biased1_k_inpolls', 'group.biased2_j_inpolls', 'group.biased2_k_inpolls']

relevant_var_ct = ['player.id_position', 'participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
                   'group.practice_round_number', 'group.quality_J', 'group.k_inelection', 'group.j_inelection', 'group.winner', 'group.quality_K',
                   'group.companyA_k_inpolls', 'group.companyB_k_inpolls', 'group.companyC_k_inpolls', 'group.companyD_k_inpolls', 'group.companyE_k_inpolls',
                   'group.companyA_j_inpolls', 'group.companyB_j_inpolls', 'group.companyC_j_inpolls', 'group.companyD_j_inpolls', 'group.companyE_j_inpolls']

for i in CT_SESSIONS:
    York_2019_PollsData[i] = York_2019_PollsData[i][[*relevant_var_ct]]

for i in TR_SESSIONS:
    York_2019_PollsData[i] = York_2019_PollsData[i][[*relevant_var_tr]]

# Now let us drop the practice rounds. This will leave us with 225 observations per session:

for i in Sessions:
    York_2019_PollsData[i] = York_2019_PollsData[i][(
        York_2019_PollsData[i]['group.practice_round_number'] >= 1)]

# Now let us rename a few variables to make the data easier to work with:
for i in Sessions:
    York_2019_PollsData[i].columns = ['subject' if x == 'participant.id_in_session' else 'round_number' if x == 'group.practice_round_number'
                                      else 'poll_vote' if x == 'player.poll' else 'election_vote' if x == 'player.vote' else 'belief_k' if x == 'player.belief_k'
                                      else 'belief_j' if x == 'player.belief_j'else 'gender' if x == 'player.gender'else 'nationality' if x == 'player.nationality'
                                      else 'major' if x == 'player.major' else 'income' if x == 'player.income'else 'total_earnings' if x == 'player.total_payoffs'
                                      else x for x in York_2019_PollsData[i].columns]
# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # #
# 23/06/2020 the problem of fisher's exact test with clustered data
K_winner = []
J_winner = []
K_vote = []
J_vote = []
for i in Sessions:
    print(str(i), York_2019_PollsData[i]
          ['group.winner'].describe()['freq'] / 15)
    K_win_times = York_2019_PollsData[i]['group.winner'].describe()[
        'freq'] / 15
    J_win_times = 15 - K_win_times
    K_winner.append(K_win_times)
    J_winner.append(J_win_times)

    K_vote_times = York_2019_PollsData[i]['election_vote'].value_counts()['K']
    J_vote_times = York_2019_PollsData[i]['election_vote'].value_counts()['J']
    K_vote.append(K_vote_times)
    J_vote.append(J_vote_times)
df = pd.DataFrame({'session': Sessions, 'K': K_winner, 'J': J_winner})
df1 = pd.DataFrame({'session': Sessions, 'K': K_vote, 'J': J_vote})
print(df)
print(df1)

K_Ct = []
K_Tr = []
K_Ct_count = []
K_Tr_count = []
for i in CT_SESSIONS:
    K_Ct.append(York_2019_PollsData[i]['group.winner'].describe()['freq'] / 15)
    K_Ct_count.append(
        York_2019_PollsData[i]['election_vote'].value_counts()['K'])
for i in TR_SESSIONS:
    K_Tr.append(York_2019_PollsData[i]['group.winner'].describe()['freq'] / 15)
    K_Tr_count.append(
        York_2019_PollsData[i]['election_vote'].value_counts()['K'])
print(K_Ct)
print(K_Ct_count)
print(stats.mannwhitneyu(K_Ct, K_Tr, alternative='less'))
print(stats.mannwhitneyu(K_Ct_count, K_Tr_count, alternative='less'))
# MannwhitneyuResult(statistic=5.0, pvalue=0.12043699518148421)

#   session     K    J
# 0   E3_T1   9.0  6.0
# 1   E3_T2   8.0  7.0
# 2   E3_T3   9.0  6.0
# 3   E3_T4  12.0  3.0
# 4   E3_T5  10.0  5.0
# 5   E3_C1   9.0  6.0
# 6   E3_C2   8.0  7.0
# 7   E3_C3   8.0  7.0
# 8   E3_C4   9.0  6.0

# # # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # #

# # J = 6 K = 10
# # U = 100 - 5(d) + Q

frames = []  # this is for df concat
frames_Ct = []
frames_Tr = []

# adding the is_treatment and average_k_inpolls

for i in TR_SESSIONS:
    York_2019_PollsData[i]['is_treatment'] = 1
    York_2019_PollsData[i]['average_k_inpolls'] = York_2019_PollsData[i][[
        'group.biased1_k_inpolls', 'group.biased2_k_inpolls']].mean(axis=1)

for i in CT_SESSIONS:
    York_2019_PollsData[i]['is_treatment'] = 0
    York_2019_PollsData[i]['average_k_inpolls'] = York_2019_PollsData[i][['group.companyA_k_inpolls', 'group.companyB_k_inpolls',
                                                                          'group.companyC_k_inpolls', 'group.companyD_k_inpolls', 'group.companyE_k_inpolls']].mean(axis=1)

# Let's create a few function which might be useful when modifing the dataset


def informed(x):
    if x in [1, 2, 3, 5, 7, 9, 11]:
        y = 1
    else:
        y = 0
    return y


def predict(x):
    if x > 0:
        y = 1
    else:
        y = 0
    return y


def id_cat(x):
    '''
    id_cat stands for id position category 
    we have 4 categories: informed, uninformed_close to J, uninformed_close to K, uninformed_median 
    '''
    if x in [1, 2, 3, 5, 7, 9, 11]:
        y = 0
    elif x in [4, 6]:
        y = 1
    elif x in [10, 12, 13, 14, 15]:
        y = 2
    else:
        y = 3
    return y


# # Lets only keep the necessary columns

York_2019_PollsData_reg = {}
for i in Sessions:
    York_2019_PollsData_reg[i] = York_2019_PollsData[i][['subject', 'round_number', 'group.quality_K', 'group.quality_J', 'is_treatment',
                                                         'belief_k', 'average_k_inpolls', 'group.k_inelection', 'player.id_position', 'poll_vote', 'election_vote', 'group.winner']]
    York_2019_PollsData_reg[i].columns = ['subject', 'round_number', 'quality_K', 'quality_J', 'is_treatment',
                                          'belief_k', 'average_k_inpolls', 'k_inelection', 'id_position', 'poll_vote', 'election_vote', 'winner']
    York_2019_PollsData_reg[i]['session'] = i
    # Ok now, let's mapping the id_position into an informed dummy
    York_2019_PollsData_reg[i]['informed'] = York_2019_PollsData_reg[i]['id_position'].apply(
        informed)
    # utility if one of the candidates wins
    York_2019_PollsData_reg[i]['U_J'] = 100 - 5 * (
        York_2019_PollsData_reg[i]['id_position'] - 6).abs() + York_2019_PollsData_reg[i]['quality_J']
    York_2019_PollsData_reg[i]['U_K'] = 100 - 5 * (
        York_2019_PollsData_reg[i]['id_position'] - 10).abs() + York_2019_PollsData_reg[i]['quality_K']
    York_2019_PollsData_reg[i]['K_J'] = York_2019_PollsData_reg[i]['U_K'] - \
        York_2019_PollsData_reg[i]['U_J']
    # who will they vote for if all are rational and uninformed gets the real information of valence
    York_2019_PollsData_reg[i]['predict'] = York_2019_PollsData_reg[i]['K_J'].apply(
        predict)
    # who they really voted for in the experiment
    York_2019_PollsData_reg[i]['election_vote'] = York_2019_PollsData_reg[i]['election_vote'].map({
                                                                                                  'K': 1, 'J': 0})
    # # compare could be 1, 0, -1 or nan.
    # 1 means they voted for K however, the rational choice should be J
    # -1 means they voted for J howver, the rational choice should be K
    # 0 means they voted for the prefer candidate
    # nan means abstetion
    York_2019_PollsData_reg[i]['compare'] = York_2019_PollsData_reg[i]['election_vote'] - \
        York_2019_PollsData_reg[i]['predict']
    York_2019_PollsData_reg[i]['add'] = York_2019_PollsData_reg[i]['election_vote'] + \
        York_2019_PollsData_reg[i]['predict']

    York_2019_PollsData_reg[i]['compare1'] = np.where(
        York_2019_PollsData_reg[i]['compare'] != 0, York_2019_PollsData_reg[i]['compare'], np.where(York_2019_PollsData_reg[i]['add'] == 0, 0, 2))

    York_2019_PollsData_reg[i]['winner'] = York_2019_PollsData_reg[i]['winner'].map({
                                                                                    'K': 1, 'J': 0})
    # highV is a boolean variable which is one if K is better than J in terms of quality
    York_2019_PollsData_reg[i]['highV'] = York_2019_PollsData_reg[i]['quality_K'] > York_2019_PollsData_reg[i]['quality_J']
    # highV_loses could be 1, 0, -1, however in the data we only have 1, 0, when it's True, highV is J, and winner is K
    # which means in our experiment if K has a higher valence, it is always elected
    # data shows that in control group , candidates with higher valence are always elected
    York_2019_PollsData_reg[i]['highV_loses'] = York_2019_PollsData_reg[i]['winner'] - \
        York_2019_PollsData_reg[i]['highV']

    # welfare effect
    # what if no poll, and informed voter vote for rationally and uniformed votes for candidate who has a close id_position, median voters flip a coin.
    York_2019_PollsData_reg[i]['id_cat'] = York_2019_PollsData_reg[i]['id_position'].apply(
        id_cat)
    York_2019_PollsData_reg[i].loc[York_2019_PollsData_reg[i]['id_cat']
                                   == 0, 'vote_nopoll'] = York_2019_PollsData_reg[i]['predict']
    York_2019_PollsData_reg[i].loc[York_2019_PollsData_reg[i]
                                   ['id_cat'] == 1, 'vote_nopoll'] = 0
    York_2019_PollsData_reg[i].loc[York_2019_PollsData_reg[i]
                                   ['id_cat'] == 2, 'vote_nopoll'] = 1
    # then set the it to 0, run the program again. the real value should always between two.
    York_2019_PollsData_reg[i].loc[York_2019_PollsData_reg[i]
                                   ['id_cat'] == 3, 'vote_nopoll'] = 1
    # count how many supporters for K in one round, if it's larger then 7, K is elected.
    York_2019_PollsData_reg[i]['K_supporters'] = York_2019_PollsData_reg[i].groupby(
        ['session', 'round_number'])['vote_nopoll'].transform('sum')
    York_2019_PollsData_reg[i]['U_nopoll'] = np.where(
        York_2019_PollsData_reg[i]['K_supporters'] > 7, York_2019_PollsData_reg[i]['U_K'], York_2019_PollsData_reg[i]['U_J'])
    # 'U_winner' is the realise utility
    York_2019_PollsData_reg[i]['U_winner'] = np.where(
        York_2019_PollsData_reg[i]['winner'] == 1, York_2019_PollsData_reg[i]['U_K'], York_2019_PollsData_reg[i]['U_J'])
    frames.append(York_2019_PollsData_reg[i])  # for data concat
    print(i)  # print it out just to show that the program runs soomthly
    # print (York_2019_PollsData_reg[i][['U_winner','U_nopoll']].describe())
    # print (York_2019_PollsData_reg[i].groupby(['informed','compare'])['average_k_inpolls'].describe())
    # # York_2019_PollsData_reg[i].groupby(['informed','compare'])['average_k_inpolls'].describe().to_excel(i + 'informed.xlsx')
    # print (York_2019_PollsData_reg[i]['highV_wins'].describe())

# # Let's check the whole data, treatment and control respectively, or just use All is enough
All = pd.concat(frames)
# # print (All.columns)
# # # the following is not useful since we have is_treatment column in the data
All_Tr = pd.concat([York_2019_PollsData_reg[i] for i in TR_SESSIONS])
All_Ct = pd.concat([York_2019_PollsData_reg[i] for i in CT_SESSIONS])

# os.chdir('/Users/lunzhengli/Desktop/biased_poll_data/E3_results')

# # # - fraction of voters vote for the least preferred candidate
# # # - session wise - across treatment
print(All.groupby(['session', 'informed', 'compare'])
      ['average_k_inpolls'].describe())
print(All.groupby(['is_treatment', 'informed', 'compare'])
      ['average_k_inpolls'].describe())
print(All.groupby(['is_treatment', 'informed', 'compare1'])
      ['average_k_inpolls'].describe())

All.groupby(['session', 'informed', 'compare'])[
    'average_k_inpolls'].describe().to_excel('E3_sessions.xlsx')
All.groupby(['is_treatment', 'informed', 'compare'])[
    'average_k_inpolls'].describe().to_excel('E3_treatments.xlsx')
All.groupby(['is_treatment', 'informed', 'compare1'])[
    'average_k_inpolls'].describe().to_excel('E3_compare1.xlsx')


# # - welfare effect
# - if all the median voters vote for 0 namely J
All.groupby(['session', 'informed'])[['U_winner', 'U_nopoll']
                                     ].describe().to_excel('E3_median_0.xlsx')
All.groupby(['is_treatment', 'informed'])[['U_winner', 'U_nopoll']
                                          ].describe().to_excel('E3_median_0_T.xlsx')


All.groupby(['session'])[['U_winner', 'U_nopoll']
                         ].describe().to_excel('E3_median_0_noinform.xlsx')
All.groupby(['is_treatment'])[['U_winner', 'U_nopoll']
                              ].describe().to_excel('E3_median_0_T_noinform.xlsx')


# - if all the median voters vote for 1 namely K

All.groupby(['session', 'informed'])[['U_winner', 'U_nopoll']
                                     ].describe().to_excel('E3_median_1.xlsx')
All.groupby(['is_treatment', 'informed'])[['U_winner', 'U_nopoll']
                                          ].describe().to_excel('E3_median_1_T.xlsx')


All.groupby(['session'])[['U_winner', 'U_nopoll']
                         ].describe().to_excel('E3_median_1_noinform.xlsx')
All.groupby(['is_treatment'])[['U_winner', 'U_nopoll']
                              ].describe().to_excel('E3_median_1_T_noinform.xlsx')

print(All.groupby(['session', 'informed'])[
      ['U_winner', 'U_nopoll']].describe())
print(All.groupby(['is_treatment', 'informed'])
      [['U_winner', 'U_nopoll']].describe())
All.groupby(['is_treatment', 'informed', 'compare1'])[
    'U_winner'].describe().to_excel('E3_prefered_voted.xlsx')


# fraction of rounds won by high valence candidate
print(All['highV_loses'].unique())
print(All.groupby(['session', 'informed'])['highV_loses'].describe())
print(All.groupby(['session', 'informed'])['highV_loses'].sum())
print(All.groupby(['is_treatment', 'informed'])['highV_loses'].describe())

All.groupby(['session', 'informed'])[
    'highV_loses'].describe().to_excel('E3_highV.xlsx')
All.groupby(['session', 'informed'])[
    'highV_loses'].sum().to_excel('E3_highV1.xlsx')
# All.groupby(['is_treatment','informed'])['highV_loses'].describe().to_excel('E3_highV2.xlsx')

All.groupby(['session', 'informed', 'highV_loses'])[
    'highV_loses'].describe().to_excel('E3_highV.xlsx')
All.groupby(['is_treatment', 'informed', 'highV_loses'])[
    'highV_loses'].describe().to_excel('E3_highV1.xlsx')

All.groupby(['session', 'highV_loses'])[
    'highV_loses'].describe().to_excel('E3_highV2.xlsx')


# '''
# -treatment derease welfare in terms of money.
# control > nopoll > treatment

# -this result do not contain the information when compare == nan, we lost the information of. it seems it doesn't matter, because abstetion is very low especially for
# informed.
# '''

# # print (All.groupby(['is_treatment','election_vote'])['election_vote'].describe())

# ###############################################################################################################################
# # poll vote describe
# ###############################################################################################################################

# # # print (All['poll_vote'].unique())
# def convert_poll(x):
#     if x == 'J':
#         y = 0
#     elif x == 'K':
#         y = 1
#     elif x == 'Prefer not to participate in the Poll':
#         y = 2
#     else:
#         y = 3
#     return y
# All['poll_vote_converted'] = All['poll_vote'].apply(convert_poll)
# All[['election_vote']]= All[['election_vote']].fillna(value = 'abstention')
# # # print (All['poll_vote_converted'].unique())
# # # print (All.groupby(['session','informed','poll_vote_converted'])['poll_vote_converted'].describe())
# # All.groupby(['session','informed','poll_vote_converted'])['poll_vote_converted'].describe().to_excel('E3_poll.xlsx')
# All.groupby(['is_treatment','poll_vote_converted', 'election_vote']).count().to_excel('E3_poll_election.xlsx')

# # we then consider that do they turthfully reveal their preference.

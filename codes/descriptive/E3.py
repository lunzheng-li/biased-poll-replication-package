import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

# The tinker module is not working Mac very well. Let's read the data using the following way.
os.chdir('../../original data/E3_data')

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

relevant_var_tr = ['participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
                   'group.practice_round_number', 'group.quality_J', 'group.k_inelection', 'group.j_inelection', 'group.winner', 'group.quality_K',
                   'group.companyA_k_inpolls', 'group.companyB_k_inpolls', 'group.companyC_k_inpolls', 'group.companyD_k_inpolls', 'group.companyE_k_inpolls',
                   'group.companyA_j_inpolls', 'group.companyB_j_inpolls', 'group.companyC_j_inpolls', 'group.companyD_j_inpolls', 'group.companyE_j_inpolls',
                   'group.biased1_company', 'group.biased2_company', 'group.biased1_j_inpolls', 'group.biased1_k_inpolls', 'group.biased2_j_inpolls', 'group.biased2_k_inpolls']

relevant_var_ct = ['participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
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

# I now want to save the data in a form that does not have the subject as an index. But I have to be very careful:
# disctionaries are mutable, so simply storing the dictionary in another variable will generate an alias. I want to avoid that

York2019_PollDt = York_2019_PollsData.copy()

# And now let us put the subject id as an index, to help us with feeling the data
for i in Sessions:
    York_2019_PollsData[i] = York_2019_PollsData[i].set_index(['subject'])

# Alternatively, we could make a composite index for each observation according to both subject id and number of round (1-15)
# for i in Sessions:
#    York_2019_PollsData[i]=York_2019_PollsData[i].set_index(['participant.id_in_session', 'group.practice_round_number'])
# I need to be careful. Any variable that belongs to a composite index cannot be treated as a normal column.


# # Now let us see how to examine the data:
# # York_2019_PollsData['Sessions_T3'].loc[[1,2,3]]  # This gives us all the data in the given session for subject 1,2,3 etc.
# # York_2019_PollsData['E3_T3'][York_2019_PollsData['E3_T3']['round_number']==2]
# # This allows us to get the data for round 2, etc.


# ######################################################################################
# # DESCRIPTIVE STATISTICS AND BASIC GRAPHICAL ANALYSIS
# ######################################################################################
# # Rememeber that K is the favoured candidate in the polls.


# # -Percentage of times K wins in Tr vs Ct
# # a) overall
# # b) across sessions

K_Winning_Percentage = {}  # This will store K's winn percentage across sessions
overall_wins_forK = 0

for i in Sessions:
    # The 'winner' variable is common across subjects. So, it suffices to
    k = York_2019_PollsData[i].loc[[1]][['group.winner', 'round_number']]
    h = pd.value_counts(k['group.winner'])
    K_Winning_Percentage[i] = h[0] / 15
    overall_wins_forK = overall_wins_forK + h[0]

Overall_Win_Per_forK = overall_wins_forK / 120

##### Overall winning percentage for K is 0.7. In the treatment conditions this is 0.8 and in the control this is 0.6 ########
############                                                                                       ###########################

# Now, let us plot this:

K_Win_Per = pd.DataFrame.from_dict(
    K_Winning_Percentage, orient='index')  # Covert dict to DataFrame
K_Win_Per.columns = ["K's Win Percentage by Session"]
K_Win_Per = K_Win_Per.sort_values(
    by="K's Win Percentage by Session", ascending=False)
K_Win_Per.plot(kind='bar')
K_Win_Per.to_csv(r'E3_win.csv')
plt.show()

# # (See graph 1). We see that all Tr have higher winning for K. Interestingly, all  Ct sessions have a 60% winning percentage for K


#             ####       Graph the Percentage of election votes for K in Tr vs Ct:          #####
# # a) Aggregated in each session

K_Vote_Fraction = {}  # This will store K's winn percentage across sessions

for i in Sessions:
    k = York_2019_PollsData[i][['election_vote', 'round_number']]
    h = pd.value_counts(k['election_vote'])
    if 'Abstain' in k['election_vote'].values:
        # h['Abstain'] is the frequency of 'abstain'
        K_Vote_Fraction[i] = h['K'] / (225 - h['Abstain'])
    else:
        K_Vote_Fraction[i] = h['K'] / (225)

# Now, let us plot this:
K_V_Fr = pd.DataFrame.from_dict(
    K_Vote_Fraction, orient='index', )  # Covert dict to DataFrame
K_V_Fr.columns = ["K's Vote Share"]
K_V_Fr = K_V_Fr.sort_values(by="K's Vote Share", ascending=False)
K_V_Fr.plot(kind='bar')
K_V_Fr.to_csv(r'E3_vote.csv')
plt.show()

# #######  From the Graph 3 it seems that K's vote shares are much higher in treatment conditions ########################
# ############################################################################################################################

# # b) Round-per round and over individual sessions

# # # Our objective is to calculate for each session the vote share of K across the 15 rounds.
K_voteFr_per_round_and_session = {}  # The overarching dictionary

for i in Sessions:
    K_vote_Fr_Per_Round = {}
    ROUND = 1
    while ROUND <= 15:
        k = York_2019_PollsData[i]
        # This is the data for round 'ROUND' alone
        k = k[k['round_number'] == ROUND]
        h = pd.value_counts(k['election_vote'])
        if ('Abstain' in k['election_vote'].values) and ('K' in k['election_vote'].values):
            K_vote_Fr_Per_Round[ROUND] = h['K'] / (15 - h['Abstain'])
        elif ('Abstain'not in k['election_vote'].values) and ('K' in k['election_vote'].values):
            K_vote_Fr_Per_Round[ROUND] = h['K'] / 15
        else:
            K_vote_Fr_Per_Round[ROUND] = 0
        ROUND = ROUND + 1

    K_voteFr_per_round_and_session[i] = K_vote_Fr_Per_Round


D = pd.DataFrame.from_dict(K_voteFr_per_round_and_session, orient='index')
DF = D.transpose()    # To graph, we need to transpose the dataframe
# DF.to_csv(r'E3_vote_per_round.csv')
# # print (DF)
# print(DF.index[::1])
# print(DF.index)

# # # # %matplotlib inline

# # This will allow us to view the plots in the Notebook

# # p=DF.plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');  # Unfortunately this is not detailed enough

# p=DF['E3_C1'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='--'); # xticks adjusts the grid spacing.
# p=DF['E3_C2'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='--');
# p=DF['E3_C3'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='--');
# p=DF['E3_C4'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='--');
# p=DF['E3_T1'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
# p=DF['E3_T2'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
# p=DF['E3_T3'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
# p=DF['E3_T4'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
# p=DF['E3_T5'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
# # I was forced to plot it like this because I wanted to choose individual markers per line

# p.legend(['Ct1','Ct2','Ct3','Ct4', 'Tr1','Tr2','Tr3','Tr4','Tr5'])
# # It means that you are using every n'th index value as a tick mark on the x-axis.
# p.set_title('K\'s Voteshare in each session and round', fontsize=25);
# p.set_xlabel('Round Number', fontsize=16);
# p.set_ylabel('K\'s Voteshare', fontsize=16);
# p.grid()
# plt.show()
# # Graph 4 shows the results. Of course there are common tendencies in all sessions, since share of K is driven by the differences in valence.


# # -Let us now illustrate 'how biased' the polls are in the treatment sessions. For each round,
# # graph the pecentage of K vote in the polls of all 5 companies.

# for i in TR_SESSIONS:

#     f=York_2019_PollsData[i].loc[[1]][['round_number', 'group.companyA_k_inpolls', 'group.companyB_k_inpolls',\
#                                         'group.companyC_k_inpolls', 'group.companyD_k_inpolls','group.companyE_k_inpolls']]
#     f=f.set_index('round_number')
#     # p=f.plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     p=f['group.companyA_k_inpolls'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     p=f['group.companyB_k_inpolls'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='v', linestyle='--');
#     p=f['group.companyC_k_inpolls'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='s', linestyle='--');
#     p=f['group.companyD_k_inpolls'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='d', linestyle='--');
#     p=f['group.companyE_k_inpolls'].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='X', linestyle='--');

#     # p.set_title('Poll Results in Session '+str(i), fontsize=20);
#     p.set_xlabel('Round Number', fontsize=16);
#     p.set_ylabel('K\'s Share in Poll of Each Company', fontsize=16);
#     p.legend(['Comp. A','Comp. B','Comp. C', 'Comp. D','Comp. E'],loc=4, prop={'size':12});
#     #p.grid()

#     plt.show()
# # Graph 5 indicates that in the treatment sessions, there were reasonably large differences
# # in the poll results among different companies. This means that the selection treatment is meaningful


# # Calculating average payoffs per subject
# Total_payoffs=0

# for i in Sessions:
#     D=York_2019_PollsData[i]
#     G=D[D['round_number']==15]['total_earnings'] # The earnings data from the last round
#     Total_payoffs=Total_payoffs+sum(G)

# Average_payoffs_per_subject=Total_payoffs/120

# # -Compare demographics across the two conditions to see whether they are balanced.
# # I better compile this table manually, seems easier.

# # -Graph the polls that agents see together with their AVERAGE stated beliefs, to get a flavour of the relationship.


# #####################################################################################
# #                                    BASIC STATISTICAL TESTS
# #####################################################################################

# ################################
# #           Statistical Tests for differences in proportions
# ################################

# # A) The hypothsis H0 is that the proportion of rounds where K wins is similar across treatments.
# # The aternative is that the treatment tends to increase the win share of K.

# #                       A.I) Fisher exact test

# # First, we form the 2x2 contingency table. We have two treatments and two outcomes (K wins, J wins)

# Election_winner={'Treatment':{'K':0, 'J':0}, 'Control':{'K':0, 'J':0}}

# for i in TR_SESSIONS:
#     k=York_2019_PollsData[i].loc[[1]][['group.winner', 'round_number']]
#     h=pd.value_counts(k['group.winner'])
#     if 'K' in h:
#         Election_winner['Treatment']['K']=Election_winner['Treatment']['K']+h['K']
#     if 'J' in h:
#         Election_winner['Treatment']['J']=Election_winner['Treatment']['J']+h['J']

# for i in CT_SESSIONS:
#     k=York_2019_PollsData[i].loc[[1]][['group.winner', 'round_number']]
#     h=pd.value_counts(k['group.winner'])
#     if 'K' in h:
#         Election_winner['Control']['K']=Election_winner['Control']['K']+h['K']
#     if 'J' in h:
#         Election_winner['Control']['J']=Election_winner['Control']['J']+h['J']

# Election_winner = pd.DataFrame.from_dict(Election_winner, orient='index')  # Now we have our 2x2 contigency table
# Election_Winner=Election_winner.transpose()
# print (Election_Winner)
# print (stats.fisher_exact(Election_Winner, alternative='less'))


# # ##############################
# # p-val of the test:  0.2450565877437343
# # ##############################

# # But even if we were agnostic to the effect of treatment and had a two-sided test,
# # we would find p-val=0.027692
# # So, even if we did not have an alternative that 'Treatment' tends to increase K (two-sided)
# # we would get a significant difference.

# # Of course, one shoud fear that rounds in each given session are not independent.
# # However, all sessions point in the same direction, which is reassuring.

# #              A.II) Chi-square test.

# print (stats.chi2_contingency(Election_Winner, correction=True, lambda_=None))
# ####################################
# # The p-val of this test is 0.49039800094287656. Again, differences appear significant
# #####################################


# Now, let us do the same for the voting behaviour of individuals. We need to cluster errors at the subject level
# or to consider individual rounds alone. It is an interesting question whether treatment seems to affect voting behaviour
# in early or later rounds. If subjects can learn, this means that the potential effect should dimish in later rounds.

######        Differences in Round-by-round voting behaviour across  the two treatments   ############

# For each session, make a dictionary with rounds as the key, and a dictionary {'K': , 'J':  ,'Abstain': } as the value.
# Then, pool the data in a given treatment together.

Vote_Counts_per_round_Ct = {}

for i in range(1, 16):
    Vote_Counts_per_round_Ct[i] = {'K': 0, 'J': 0,
                                   'Abstain': 0}  # Initialising the dictionary

for i in CT_SESSIONS:
    ROUND = 1
    while ROUND <= 15:
        k = York_2019_PollsData[i]
        # This is the data for round 'ROUND' alone
        k = k[k['round_number'] == ROUND]
        h = pd.value_counts(k['election_vote'])
        if ('Abstain' in k['election_vote'].values):
            Vote_Counts_per_round_Ct[ROUND]['Abstain'] = Vote_Counts_per_round_Ct[ROUND]['Abstain'] + h['Abstain']
        if ('K' in k['election_vote'].values):
            Vote_Counts_per_round_Ct[ROUND]['K'] = Vote_Counts_per_round_Ct[ROUND]['K'] + h['K']
        if ('J' in k['election_vote'].values):
            Vote_Counts_per_round_Ct[ROUND]['J'] = Vote_Counts_per_round_Ct[ROUND]['J'] + h['J']
        ROUND = ROUND + 1

# Now Vote_Counts_per_round_Ct contains the counts of votes for each period, with the 4 control treatments pooled

Vote_Counts_per_round_Tr = {}

for i in range(1, 16):
    Vote_Counts_per_round_Tr[i] = {'K': 0, 'J': 0,
                                   'Abstain': 0}  # Initialising the dictionary

for i in TR_SESSIONS:
    ROUND = 1
    while ROUND <= 15:
        k = York_2019_PollsData[i]
        # This is the data for round 'ROUND' alone
        k = k[k['round_number'] == ROUND]
        h = pd.value_counts(k['election_vote'])
        if ('Abstain' in k['election_vote'].values):
            Vote_Counts_per_round_Tr[ROUND]['Abstain'] = Vote_Counts_per_round_Tr[ROUND]['Abstain'] + h['Abstain']
        if ('K' in k['election_vote'].values):
            Vote_Counts_per_round_Tr[ROUND]['K'] = Vote_Counts_per_round_Tr[ROUND]['K'] + h['K']
        if ('J' in k['election_vote'].values):
            Vote_Counts_per_round_Tr[ROUND]['J'] = Vote_Counts_per_round_Tr[ROUND]['J'] + h['J']
        ROUND = ROUND + 1

# Now, let us make K's vote fraction per round in each treatment and let us graph it

K_fract_per_round_Ct = {}
for i in range(1, 16):
    K_fract_per_round_Ct[i] = Vote_Counts_per_round_Ct[i]['K'] / \
        (60 - Vote_Counts_per_round_Ct[i]['Abstain'])
print(sum([Vote_Counts_per_round_Ct[i]['Abstain'] for i in range(1, 16)]) / 15)
# 1.4


K_fract_per_round_Tr = {}
for i in range(1, 16):
    K_fract_per_round_Tr[i] = Vote_Counts_per_round_Tr[i]['K'] / \
        (75 - Vote_Counts_per_round_Tr[i]['Abstain'])
print(sum([Vote_Counts_per_round_Tr[i]['Abstain'] for i in range(1, 16)]) / 15)
# 1.6666666666666667


pd.DataFrame.from_dict(K_fract_per_round_Ct, orient='index').to_csv(
    r'E3_vote_l5_ct.csv')
pd.DataFrame.from_dict(K_fract_per_round_Tr, orient='index').to_csv(
    r'E3_vote_l5_tr.csv')


# # Now, let us graph this:

FR_Ct = pd.DataFrame.from_dict(K_fract_per_round_Ct, orient='index')
FR_Tr = pd.DataFrame.from_dict(K_fract_per_round_Tr, orient='index')

p = FR_Ct[0].plot(figsize=[20, 5], xticks=DF.index[::1],
                  grid=True, marker='o', linestyle='--');
p = FR_Tr[0].plot(figsize=[20, 5], xticks=DF.index[::1],
                  grid=True, marker='o', linestyle='-');
print(FR_Ct)
print(FR_Tr)
# p = FR_Ct['K'].plot(figsize=[20, 5], xticks=DF.index[::1],
#                     grid=True, marker='o', linestyle='--');
# p = FR_Tr['K'].plot(figsize=[20, 5], xticks=DF.index[::1],
#                     grid=True, marker='o', linestyle='-');

# p.set_title('K\'s Vote Share per Round and Treatment', fontsize=20);
p.set_xlabel('Round Number', fontsize=16)
p.set_ylabel('K\'s Vote Share', fontsize=16)
p.legend(['Control', 'Treatment'], loc=4, prop={'size': 12});
# p.grid()
plt.show()

# # Graph 6 nicely shows that in each round, the fraction of votes for K is higher in the treatment rather than the control.

#     #########################################

# # Let is split the data into only two categories ('vote for K', 'not vote for K'), in order to perform Fisher's exact tests

# for i in range(1,16):
#     Vote_Counts_per_round_Ct[i]['Not K']= Vote_Counts_per_round_Ct[i]['J']+ Vote_Counts_per_round_Ct[i]['Abstain']

# for i in range(1,16):
#     Vote_Counts_per_round_Tr[i]['Not K']= Vote_Counts_per_round_Tr[i]['J']+ Vote_Counts_per_round_Tr[i]['Abstain']

# # Now calculate the p-value of the fisher exact test across rounds

# Fisher_p_vals_per_round={}

# for i in range(1,16):
#     d={1:[Vote_Counts_per_round_Ct[i]['K'], Vote_Counts_per_round_Ct[i]['Not K']], 2:[Vote_Counts_per_round_Tr[i]['K'], Vote_Counts_per_round_Tr[i]['Not K']]}
#     g=pd.DataFrame.from_dict(d)
#     Fisher_p_vals_per_round[i]=stats.fisher_exact(g , alternative='less')[1]

# # Ok. It seems that for most rounds the direction is in the expected side, and that only in rounds 1,3 and 13 the tendency to
# # vote for K is relatively similar across treatments.

# # Now, let us graph this:

# F=pd.DataFrame.from_dict(Fisher_p_vals_per_round, orient='index')
# p=F.plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');

# p.set_title('P-Values of Test of Difference in K\'s Share (Alternative: Treatment Increases this Share)', fontsize=20);
# p.set_xlabel('Round Number', fontsize=16);
# p.set_ylabel('P value of Fisher Test', fontsize=16);
# p.legend(['p-val.']);
# #p.grid()
# plt.show()

# # Graph 7 illustrates the p-values of these tests.


# #########################             ANALYSIS OF BELIEFS    #######################################################
# ####################################################################################################################


# # Subjects do not know the overlap among polls. So it is natural to assume that they may use the average of the polls they
# # see revealed as a summary of poll info. So, let us calculate this for every round, and then let us get a scatterplot of their
# # stated beliefs in every round together with these summaries.

# # Our first graph juxtaposes individual beliefs to the average poll info that people are exposed to

# # First, consider the control treatments.

# Average_Polls_Ct={}

# for i in CT_SESSIONS:
#     Total_Poll_info=York_2019_PollsData[i].loc[[1]][['round_number','group.companyA_k_inpolls', 'group.companyB_k_inpolls',\
#                                            'group.companyC_k_inpolls','group.companyD_k_inpolls' , 'group.companyE_k_inpolls']]
#     Total_Poll_info=Total_Poll_info.set_index('round_number')
#     Av_Poll_info=Total_Poll_info.mean(axis=1)
#     Average_Polls_Ct[i]=Av_Poll_info

# # Then, for the biased info 'treatments':

# Average_Polls_Tr={}

# for i in TR_SESSIONS:
#     Total_Poll_info=York_2019_PollsData[i].loc[[1]][['round_number', 'group.biased1_k_inpolls', 'group.biased2_k_inpolls']]
#     Total_Poll_info=Total_Poll_info.set_index('round_number')
#     Av_Poll_info=Total_Poll_info.mean(axis=1)
#     Average_Polls_Tr[i]=Av_Poll_info

# # Ok. Now let us save this into Dataframes for graphing purposes:

# Ks_AvFraction_Polls_Ct=pd.DataFrame.from_dict(Average_Polls_Ct, orient='index').transpose()
# Ks_AvFraction_Polls_Tr=pd.DataFrame.from_dict(Average_Polls_Tr, orient='index').transpose()

# # Now let us graph this for the control sessions. We need a dataframe for the beliefs, but with each subject having
# # different beliefs in each round.
# for i in CT_SESSIONS:
#     data=York_2019_PollsData[i].set_index('round_number')
#     belief_data=data['belief_k']
#     p=belief_data.plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     # Notice that the plot is made according to the index of the DataFrame. So the horizontal axis runs from 1 to 15
#     p=Ks_AvFraction_Polls_Ct[i].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='-');
#     # The index in this DF also runs from 1 to 15, so I can graph the two together!
#     p.legend(['Individual beliefs','Average Polls']);
#     p.set_title('Comparing Invidividual beliefs to poll information in each round, session '+ str(i), fontsize=20);
#     p.set_xlabel('Round Number', fontsize=16);
#     p.set_ylabel('K\'s Winning Chances', fontsize=16);
#     plt.show()  # If I did not add this, the graphs would all show in the same axes


# for i in TR_SESSIONS:
#     data=York_2019_PollsData[i].set_index('round_number')
#     belief_data=data['belief_k']
#     p=belief_data.plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     p=Ks_AvFraction_Polls_Tr[i].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='-');
#     p.legend(['Individual beliefs','Average Polls']);
#     p.set_title('Comparing Invidividual beliefs to poll information in each round, session '+ str(i), fontsize=20);
#     p.set_xlabel('Round Number', fontsize=16);
#     p.set_ylabel('K\'s Winning Chances', fontsize=16);
#     plt.show() # If I did not add this, the graphs would all show in the same axes


#     ############ GRAPH 8 shows the results. No clear pattern is shown. For most sessions, the average beliefs seem
#     #######                   to follow closely the average poll info            ##################################

# # Each subject's correlation coefficient between average poll info and beliefs. Does the average (spearman) correlation
# #,coefficient between beliefs and average poll info changes across treatment?
# # So, we shall calculate the correlation for each subject and then take its average.


beliefs_per_round_Ct = {}
for i in CT_SESSIONS:                                     # First, saving the data on beliefs
    data = York2019_PollDt[i].set_index('round_number')
    belief_data = data[['subject', 'belief_k']]
    beliefs_per_round_Ct[i] = belief_data


beliefs_per_round_Tr = {}
for i in TR_SESSIONS:
    data = York2019_PollDt[i].set_index('round_number')
    belief_data = data[['subject', 'belief_k']]
    beliefs_per_round_Tr[i] = belief_data

# ########   So, now  beliefs_per_round_Tr, beliefs_per_round_Tr    are dictionaries of dataframes. For instance,
# ########   beliefs_per_round_Tr['E3_T3']  contains the beliefs per round and subject in the particular session (225 obs.)


# # Now we need to solve the average poll fraction in the right format. This has to be the same for all subjects in a given round

Av_Polls_Ct = {}

for i in CT_SESSIONS:
    Dt = York2019_PollDt[i].set_index('round_number')
    Total_Poll_info = Dt[['group.companyA_k_inpolls', 'group.companyB_k_inpolls',
                          'group.companyC_k_inpolls', 'group.companyD_k_inpolls', 'group.companyE_k_inpolls']]
    Av_Poll_info = Total_Poll_info.mean(axis=1)
    Av_Polls_Ct[i] = Av_Poll_info


Av_Polls_Tr = {}

for i in TR_SESSIONS:
    Dt = York2019_PollDt[i].set_index('round_number')
    Total_Poll_info = Dt[[
        'group.biased1_k_inpolls', 'group.biased2_k_inpolls']]
    Av_Poll_info = Total_Poll_info.mean(axis=1)
    Av_Polls_Tr[i] = Av_Poll_info

# ##############              CORRELATION COEFFICIENT ANALYSIS             #############################
# # Good. Now Av_Polls_Tr, Av_Polls_Ct  are dictionaries having as their values series.

# # Notice that if subjects merely compare Av_Polls with the election results, then they are likely to continue believing them,
# # since although they falsely represent the preferences as expressed in polls, they also push in favour of K and they may become
# # self-confirming profecies in the actual elections.

# # Let me first merge the two data sets and then get some illustration of the relationship between average poll info and
# # average beliefs.

# for i in TR_SESSIONS:
#     A=beliefs_per_round_Tr[i]
#     B=Av_Polls_Tr[i]
#     H=pd.concat([A,B], axis=1)
#     # p= H[['belief_k', 0]].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     #=Ks_AvFraction_Polls_Tr[i].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='-');
#     p= H[['belief_k']].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     p= H.iloc[:,2].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');

#     p.legend(['Average Beliefs for K\'s Vote Share','Average Poll Info for K\'s Vote share'],loc=4, prop={'size':12});
#     # p.set_title('Comparing Av. Beliefs to Av. Poll Info, session '+str(i), fontsize=20);p.set_xlabel('Round Number', fontsize=16);
#     p.set_xlabel('Round Number',fontsize=16)
#     p.set_ylabel('K\'s Vote Share', fontsize=16);
#     plt.show()

# for i in CT_SESSIONS:
#     A=beliefs_per_round_Ct[i]
#     B=Av_Polls_Ct[i]
#     H=pd.concat([A,B], axis=1)
#     # p= H[['belief_k', 0]].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');

#     p= H[['belief_k']].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='--');
#     p= H.iloc[:,2].groupby(['round_number']).mean().plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='o', linestyle='-');
#     #=Ks_AvFraction_Polls_Tr[i].plot(figsize=[20,5], xticks=DF.index[::1], grid=True, marker='x', linestyle='-');
#     p.legend(['Average Beliefs for K\'s Vote Share','Average Poll Info for K\'s Vote share'],loc=4, prop={'size':12});
#     # p.set_title('Comparing Av. Beliefs to Av. Poll Info, session '+str(i), fontsize=20);p.set_xlabel('Round Number', fontsize=16);
#     p.set_xlabel('Round Number',fontsize=16)
#     p.set_ylabel('K\'s Vote Share', fontsize=16);
#     plt.show()

# # ############### GRAPH 9 presents this information for each session. This gave me the average beliefs ###################
# # ############### as compared to average polls revealed. I see no particular pattern that would indicate #################
# # ################ that subjects' beliefs systematically deviate from the revealed average poll info. ####################

CC_Beliefs_PollInfo = {}

for i in TR_SESSIONS:
    A = beliefs_per_round_Tr[i]
    B = Av_Polls_Tr[i]
    H = pd.concat([A, B], axis=1)
    CC_Beliefs_PollInfo[i] = stats.pearsonr(H['belief_k'], H[0])

for i in CT_SESSIONS:
    A = beliefs_per_round_Ct[i]
    B = Av_Polls_Ct[i]
    H = pd.concat([A, B], axis=1)
    CC_Beliefs_PollInfo[i] = stats.pearsonr(H['belief_k'], H[0])

d = pd.DataFrame.from_dict(CC_Beliefs_PollInfo,  orient='index')
d.columns = ['Pearson Correlation', 'p-value']
d = d.sort_values(by='Pearson Correlation', ascending=False)
p = d.iloc[:, 0].plot(kind='bar', figsize=[10, 6])
# p.set_title('Correlation of Beliefs to Av. Poll Info in Each Session', fontsize=16);
# p.set_xlabel('Session', fontsize=10);
p.set_ylabel('Pearson Correlation', fontsize=10)
d.to_csv(r'E3_pearson.csv')
plt.show()

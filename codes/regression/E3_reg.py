#######################################################
# distributions of differences between poll and election
########################################################

import pandas as pd              # 'Pandas' is Python's main library for data analysis
import numpy as np
from scipy import stats
import tkinter.filedialog as tk  #  This module allows to specify the path to chosen files
import matplotlib.pyplot as plt  # Used for plotting and visualising
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import os
import seaborn as sns
from scipy.stats import skew

# The tinker module is not working Mac very well. Let's read the data using the following way.
os.chdir('/Users/lunzhengli/Desktop/biased_poll_data/E3_data')

York_TREAT=pd.read_excel('E3_Treatment.xlsx') 

York_CONTROL=pd.read_excel('E3_Control.xlsx')

York_2019_PollsData={}              # Save data from different sessions in dictionary

TR_SESSIONS=['E3_T1','E3_T2','E3_T3','E3_T4','E3_T5']  # We name the 8 sessions we conducted
CT_SESSIONS=['E3_C1','E3_C2','E3_C3','E3_C4']
Sessions=TR_SESSIONS+CT_SESSIONS

i=0
for s in TR_SESSIONS:
    York_2019_PollsData[s]=York_TREAT.iloc[i:i+270]
    i=i+270

    
i=0
for s in CT_SESSIONS:
    York_2019_PollsData[s]=York_CONTROL.iloc[i:i+270]
    i=i+270
# For tractability let us choose the variables that we are interested in:

relevant_var_tr=['participant.id_in_session','player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
              'group.practice_round_number', 'group.quality_J','group.k_inelection','group.j_inelection','group.winner', 'group.quality_K',
             'group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls',
             'group.companyA_j_inpolls','group.companyB_j_inpolls','group.companyC_j_inpolls','group.companyD_j_inpolls', 'group.companyE_j_inpolls',
             'group.biased1_company', 'group.biased2_company','group.biased1_j_inpolls','group.biased1_k_inpolls', 'group.biased2_j_inpolls','group.biased2_k_inpolls']
    
relevant_var_ct=['participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
              'group.practice_round_number', 'group.quality_J','group.k_inelection','group.j_inelection','group.winner', 'group.quality_K',
             'group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls',
             'group.companyA_j_inpolls','group.companyB_j_inpolls','group.companyC_j_inpolls','group.companyD_j_inpolls', 'group.companyE_j_inpolls']

for i in CT_SESSIONS:
    York_2019_PollsData[i]=York_2019_PollsData[i][[*relevant_var_ct]]
                      
for i in TR_SESSIONS:
    York_2019_PollsData[i]=York_2019_PollsData[i][[*relevant_var_tr]]
    
# Now let us drop the practice rounds. This will leave us with 225 observations per session:

for i in Sessions:
    York_2019_PollsData[i]=York_2019_PollsData[i][(York_2019_PollsData[i]['group.practice_round_number']>=1)]
    
# Now let us rename a few variables to make the data easier to work with:
for i in Sessions:
    York_2019_PollsData[i].columns = ['subject' if x=='participant.id_in_session' else 'round_number' if x== 'group.practice_round_number'\
    else 'poll_vote' if x== 'player.poll' else 'election_vote' if x=='player.vote' else 'belief_k' if x== 'player.belief_k'\
    else 'belief_j' if x== 'player.belief_j'else 'gender' if x== 'player.gender'else 'nationality' if x== 'player.nationality'\
    else 'major' if x== 'player.major' else 'income' if x== 'player.income'else 'total_earnings' if x== 'player.total_payoffs'\
    else x for x in York_2019_PollsData[i].columns]

# I now want to save the data in a form that does not have the subject as an index. But I have to be very careful:
# disctionaries are mutable, so simply storing the dictionary in another variable will generate an alias. I want to avoid that

York2019_PollDt=York_2019_PollsData.copy()         

# And now let us put the subject id as an index, to help us with feeling the data
for i in Sessions:
    York_2019_PollsData[i]=York_2019_PollsData[i].set_index(['subject'])


frames = [] # this is for df concat   
frames_Ct = []
frames_Tr = []
for i in TR_SESSIONS:
    York_2019_PollsData[i]['is_treatment'] = 1
    York_2019_PollsData[i]['average_k_inpolls'] = York_2019_PollsData[i][['group.biased1_k_inpolls','group.biased2_k_inpolls']].mean(axis=1)
#     frames_Tr.append(York_2019_PollsData[i])
for i in CT_SESSIONS:
    York_2019_PollsData[i]['is_treatment'] = 0
    York_2019_PollsData[i]['average_k_inpolls'] = York_2019_PollsData[i][['group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls']].mean(axis=1)
#     frames_Ct.append(York_2019_PollsData[i])
# print (York_2019_PollsData['Ct_29_05_1400'])
# print (York_2019_PollsData['Tr_29_05_1600'])

# Let's just simply keep the columns which are necessary
York_2019_PollsData_reg = {}
for i in Sessions:
    York_2019_PollsData_reg[i] = York_2019_PollsData[i][['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'group.k_inelection']]
    York_2019_PollsData_reg[i].columns = ['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'k_inelection']
    York_2019_PollsData_reg[i]['session'] = i     
    York_2019_PollsData_reg[i] = York_2019_PollsData_reg[i].groupby(['round_number']).mean()
    
    York_2019_PollsData_reg[i]['diff_BP'] = York_2019_PollsData_reg[i]['belief_k'] -  York_2019_PollsData_reg[i]['average_k_inpolls']
    York_2019_PollsData_reg[i]['diff_PV'] = York_2019_PollsData_reg[i]['average_k_inpolls'] - York_2019_PollsData_reg[i]['k_inelection']
    York_2019_PollsData_reg[i]['diff_BV'] = York_2019_PollsData_reg[i]['belief_k'] - York_2019_PollsData_reg[i]['k_inelection']
    
    
# dealing with lags
    York_2019_PollsData_reg[i]['diff_PV_lag'] = York_2019_PollsData_reg[i]['diff_PV'].shift(periods = 1)
    
    York_2019_PollsData_reg[i]['diff_BP_lag'] = York_2019_PollsData_reg[i]['diff_BP'].shift(periods = 1)
#     York_2019_PollsData_reg[i]['diff_BP_lagg'] = York_2019_PollsData_reg[i]['diff_BP'].shift(periods = 2)
#     York_2019_PollsData_reg[i]['diff_BP_laggg'] = York_2019_PollsData_reg[i]['diff_BP'].shift(periods = 3)
    
    York_2019_PollsData_reg[i]['diff_BV_lag'] = York_2019_PollsData_reg[i]['diff_BV'].shift(periods = 1)
    frames.append(York_2019_PollsData_reg[i])
# print (York_2019_PollsData_reg['Ct_29_05_1400'])

# lets just simply pool all the data together
All = pd.concat(frames).reset_index()      
# # # Let's also check for each treament
All_Tr = pd.concat([York_2019_PollsData_reg[i] for i in TR_SESSIONS]).reset_index()  
All_Ct = pd.concat([York_2019_PollsData_reg[i] for i in CT_SESSIONS]).reset_index()  

# All.to_csv('All_E3.csv')
# # 
sns.distplot(All_Tr['diff_PV'], label = "Treatment")
sns.distplot(All_Ct['diff_PV'], label = "Control")
plt.legend()
# plt.title('Distribution of differences between poll and election (E3)')
plt.xlabel('Differences between poll results and vote share of elections')
# plt.savefig('E3_diff_PV')
plt.show()
# # 
print (skew(All_Tr['diff_PV'].values))
print (np.mean(All_Tr['diff_PV'].values))
print (skew(All_Ct['diff_PV'].values))
print (np.mean(All_Ct['diff_PV'].values))

#############
# regressions
#############

# # # # we get all the data we needed, let try to work on it
####################################################################################################################
# result1 = smf.ols(formula="belief_k ~ round_number*is_treatment*average_k_inpolls", data= All).fit()
# result2 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls ", data= All_Tr).fit()
# result3 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls", data= All_Ct).fit()

# dfoutput1 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput1)


# ######################################################################################################################
# result1 = smf.ols(formula= " k_inelection ~  average_k_inpolls + is_treatment + is_treatment*average_k_inpolls", data= All).fit()                                               
# result2 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Tr).fit()
# result3 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Ct).fit()

# dfoutput2 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput2)


# #####################################################################################################################

# result1 = smf.ols(formula= " diff_BP~  diff_PV_lag + is_treatment + is_treatment*diff_PV_lag", data= All).fit()                                               
# result2 = smf.ols(formula= " diff_BP~  diff_PV_lag", data= All_Tr).fit()
# result3 = smf.ols(formula= " diff_BP~  diff_PV_lag", data= All_Ct).fit()

# dfoutput3 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput3)

#####################################################################################################################

# result1 = smf.ols(formula= " belief_k~  diff_BV_lag + is_treatment + is_treatment*diff_BV_lag", data= All).fit()                                               
# result2 = smf.ols(formula= " belief_k~  diff_BV_lag", data= All_Tr).fit()
# result3 = smf.ols(formula= " belief_k~  diff_BV_lag", data= All_Ct).fit()

# dfoutput4 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput4)



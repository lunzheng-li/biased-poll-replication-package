import pandas as pd  
import numpy as np           
from scipy import stats
import matplotlib.pyplot as plt
import os 
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col 
import seaborn as sns 
from scipy.stats import skew

# The tinker module is not working Mac very well. Let's read the data using the following way.
os.chdir('/Users/lunzhengli/Desktop/biased_poll_data/E2_data')

NOV_TREAT=pd.read_excel('E2_Treatment.xlsx') 

NOV_CONTROL=pd.read_excel('E2_Control.xlsx')

NOV_2018_PollsData={}              # Save data from different sessions in dictionary

TR_SESSIONS=['E2_T1','E2_T2','E2_T3','E2_T4']  # We name the 8 sessions we conducted
CT_SESSIONS=['E2_C1','E2_C2','E2_C3','E2_C4']
NOV_SESSIONS=TR_SESSIONS+CT_SESSIONS

i=0
for s in TR_SESSIONS:
    NOV_2018_PollsData[s]=NOV_TREAT.iloc[i:i+270]
    i=i+270

    
i=0
for s in CT_SESSIONS:
    NOV_2018_PollsData[s]=NOV_CONTROL.iloc[i:i+270]
    i=i+270
    
# Our main data structure is ready.

# For tractability let us choose the variables that we are interested in:

relevant_var_tr=['participant.id_in_session','player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
              'group.practice_round_number', 'group.quality_J','group.k_inelection','group.j_inelection','group.winner', 'group.quality_K',
             'group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls',
             'group.companyA_j_inpolls','group.companyB_j_inpolls','group.companyC_j_inpolls','group.companyD_j_inpolls', 'group.companyE_j_inpolls',
             'group.biased1_company', 'group.biased2_company','group.biased1_j_inpolls','group.biased1_k_inpolls', 'group.biased2_j_inpolls','group.biased2_k_inpolls']
    
relevant_var_ct=['participant.id_in_session', 'player.poll', 'player.vote', 'player.belief_k', 'player.belief_j', 'player.gender', 'player.nationality', 'player.major', 'player.income', 'player.total_payoffs',
              'group.practice_round_number', 'group.quality_J','group.k_inelection','group.j_inelection','group.winner', 'group.quality_K',
             'group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls',
             'group.companyA_j_inpolls','group.random1_company','group.random2_company','group.random1_j_inpolls', 'group.random2_j_inpolls','group.random1_k_inpolls', 'group.random2_k_inpolls','group.companyB_j_inpolls','group.companyC_j_inpolls','group.companyD_j_inpolls', 'group.companyE_j_inpolls']

# The variables ,'group.random1_company', ,'group.random2_company', 'group.random1_k_inpolls', 'group.random2_k_inpolls'
# 'group.random1_j_inpolls', 'group.random2_j_inpolls'  are new to the analysis and they describe the randomly chosen companies
# in the new control treatment and their results

for i in  CT_SESSIONS:
    NOV_2018_PollsData[i]=NOV_2018_PollsData[i][[*relevant_var_ct]]
                      
for i in TR_SESSIONS:
    NOV_2018_PollsData[i]=NOV_2018_PollsData[i][[*relevant_var_tr]]
    
# Now let us drop the practice rounds. This will leave us with 225 observations per session:

for i in NOV_SESSIONS:
    NOV_2018_PollsData[i]=NOV_2018_PollsData[i][(NOV_2018_PollsData[i]['group.practice_round_number']>=1)]
    # Keep the observations for which the logical relation in the parenthesis holds
    
# Now let us rename a few variables to make the data easier to work with:
for i in NOV_SESSIONS:
    NOV_2018_PollsData[i].columns = ['subject' if x=='participant.id_in_session' else 'round_number' if x== 'group.practice_round_number'    else 'poll_vote' if x== 'player.poll' else 'election_vote' if x=='player.vote' else 'belief_k' if x== 'player.belief_k'    else 'belief_j' if x== 'player.belief_j'else 'gender' if x== 'player.gender'else 'nationality' if x== 'player.nationality'    else 'major' if x== 'player.major' else 'income' if x== 'player.income'else 'total_earnings' if x== 'player.total_payoffs'    else x for x in NOV_2018_PollsData[i].columns]

NOV_2018_PollsDt=NOV_2018_PollsData.copy()  # Making a copy of the dictionary, not an alias        

# And now let us put the subject id as an index, to help us with feeling the data
for i in NOV_SESSIONS:
    NOV_2018_PollsData[i]=NOV_2018_PollsData[i].set_index(['subject'])


# In[2]:


# let's get the data for the econometrics part
frames = [] # this is for df concat   
frames_Ct = []
frames_Tr = []
for i in TR_SESSIONS:
    NOV_2018_PollsData[i]['is_treatment'] = 1
    NOV_2018_PollsData[i]['average_k_inpolls'] = NOV_2018_PollsData[i][['group.biased1_k_inpolls','group.biased2_k_inpolls']].mean(axis=1)

for i in CT_SESSIONS:
    NOV_2018_PollsData[i]['is_treatment'] = 0
    NOV_2018_PollsData[i]['average_k_inpolls'] = NOV_2018_PollsData[i][['group.random1_k_inpolls','group.random2_k_inpolls']].mean(axis=1)


# Let's just simply keep the columns which are necessary
NOV_2018_PollsData_reg = {}
for i in NOV_SESSIONS:
    NOV_2018_PollsData_reg[i] = NOV_2018_PollsData[i][['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'group.k_inelection']]
    NOV_2018_PollsData_reg[i].columns = ['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'k_inelection']
    NOV_2018_PollsData_reg[i]['session'] = i     
    NOV_2018_PollsData_reg[i] = NOV_2018_PollsData_reg[i].groupby(['round_number']).mean()
    
    NOV_2018_PollsData_reg[i]['diff_BP'] = NOV_2018_PollsData_reg[i]['belief_k'] -  NOV_2018_PollsData_reg[i]['average_k_inpolls']
    NOV_2018_PollsData_reg[i]['diff_PV'] = NOV_2018_PollsData_reg[i]['average_k_inpolls'] - NOV_2018_PollsData_reg[i]['k_inelection']
    NOV_2018_PollsData_reg[i]['diff_BV'] = NOV_2018_PollsData_reg[i]['belief_k'] - NOV_2018_PollsData_reg[i]['k_inelection']
    
    
# dealing with lags
    NOV_2018_PollsData_reg[i]['diff_PV_lag'] = NOV_2018_PollsData_reg[i]['diff_PV'].shift(periods = 1)
    
    NOV_2018_PollsData_reg[i]['diff_BP_lag'] = NOV_2018_PollsData_reg[i]['diff_BP'].shift(periods = 1)
    NOV_2018_PollsData_reg[i]['diff_BP_lagg'] = NOV_2018_PollsData_reg[i]['diff_BP'].shift(periods = 2)
    NOV_2018_PollsData_reg[i]['diff_BP_laggg'] = NOV_2018_PollsData_reg[i]['diff_BP'].shift(periods = 3)
    
    NOV_2018_PollsData_reg[i]['diff_BV_lag'] = NOV_2018_PollsData_reg[i]['diff_BV'].shift(periods = 1)
    frames.append(NOV_2018_PollsData_reg[i])


# lets just simply pool all the data together
All = pd.concat(frames).reset_index()      
# # # Let's also check for each treament
All_Tr = pd.concat([NOV_2018_PollsData_reg[i] for i in TR_SESSIONS]).reset_index()  
All_Ct = pd.concat([NOV_2018_PollsData_reg[i] for i in CT_SESSIONS]).reset_index()  

print (All)


# All.to_csv('All_E2.csv')


# # # # we get all the data we needed, let try to work on it
###################################################################################################################
# result1 = smf.ols(formula="belief_k ~ round_number*is_treatment*average_k_inpolls", data= All).fit()
# result2 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls ", data= All_Tr).fit()
# result3 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls", data= All_Ct).fit()

# dfoutput1 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput1)


# #####################################################################################################################
# result1 = smf.ols(formula= " k_inelection ~  average_k_inpolls + is_treatment + is_treatment*average_k_inpolls", data= All).fit()                                               
# result2 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Tr).fit()
# result3 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Ct).fit()

# dfoutput2 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput2)


# ####################################################################################################################

# result1 = smf.ols(formula= " diff_BP~  diff_PV_lag + is_treatment + is_treatment*diff_PV_lag", data= All).fit()                                               
# result2 = smf.ols(formula= " diff_BP~  diff_PV_lag", data= All_Tr).fit()
# result3 = smf.ols(formula= " diff_BP~  diff_PV_lag", data= All_Ct).fit()

# dfoutput3 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput3)

# ####################################################################################################################

# result1 = smf.ols(formula= " belief_k~  diff_BV_lag + is_treatment + is_treatment*diff_BV_lag", data= All).fit()                                               
# result2 = smf.ols(formula= " belief_k~  diff_BV_lag", data= All_Tr).fit()
# result3 = smf.ols(formula= " belief_k~  diff_BV_lag", data= All_Ct).fit()

# dfoutput4 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput4)


# In[7]:


# # let's graphcailly illustrate diff_PV and diff_BP

# # All_Tr.hist(column='diff_PV',  bins=10)

# # All_Ct.hist(column='diff_PV',  bins=10)

# # All_Tr.hist(column='diff_BP',  bins=10)

# # All_Ct.hist(column='diff_BP',  bins=10)

sns.distplot(All_Tr['diff_PV'], label = "Treatment")
sns.distplot(All_Ct['diff_PV'], label = "Control")
plt.legend()
# plt.title('Distribution of differences between poll and election (E2)')
plt.xlabel('Differences between poll results and vote share of elections')
# plt.savefig('E2_diff_PV')
plt.show()

print (skew(All_Tr['diff_PV'].values))
print (np.mean(All_Tr['diff_PV'].values))
print (skew(All_Ct['diff_PV'].values))
print (np.mean(All_Ct['diff_PV'].values))


# sns.distplot(All_Tr['diff_BP'], label = "Treatment")
# sns.distplot(All_Ct['diff_BP'], label = "Control")
# # plt.title('Distribution of differences between belief and poll (E2)')
# plt.legend()

# # plt.savefig('E2_diff_BP')
# plt.show()


# In[6]:


# # in E2, how close reaveled polls between treatment and control

# sns.distplot(All_Tr['average_k_inpolls'], label = "Treatment")
# sns.distplot(All_Ct['average_k_inpolls'], label = "Control")
# plt.title('Distribution of average poll information in E2')


# plt.legend()
# plt.savefig('E2_average_k_inpolls')
# plt.show()


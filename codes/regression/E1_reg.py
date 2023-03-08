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

MAY_2018_PollsData={}

os.chdir('/Users/lunzhengli/Desktop/biased_poll_data/E1_data')

MAY_2018_PollsData['E1_C1']=pd.read_excel('E1_C1.xlsx') # Made the dataframe corresponding to the session

MAY_2018_PollsData['E1_C2']=pd.read_excel('E1_C2.xlsx')

MAY_2018_PollsData['E1_C3']=pd.read_excel('E1_C3.xlsx')

MAY_2018_PollsData['E1_C4']=pd.read_excel('E1_C4.xlsx')

MAY_2018_PollsData['E1_T1']=pd.read_excel('E1_T1.xlsx')

MAY_2018_PollsData['E1_T2']=pd.read_excel('E1_T2.xlsx')

MAY_2018_PollsData['E1_T3']=pd.read_excel('E1_T3.xlsx')

MAY_2018_PollsData['E1_T4']=pd.read_excel('E1_T4.xlsx')    


Sessions= ['E1_C1','E1_C2','E1_C3','E1_C4','E1_T1','E1_T2','E1_T3','E1_T4']
Sessions_Tr= ['E1_T1','E1_T2','E1_T3','E1_T4']
Sessions_Ct= ['E1_C1','E1_C2','E1_C3','E1_C4']

Initial_rows={}
Initial_rows['E1_C1']=810
Initial_rows['E1_C2']=1080
Initial_rows['E1_C3']=0
Initial_rows['E1_C4']=270
Initial_rows['E1_T1']=810
Initial_rows['E1_T2']=0
Initial_rows['E1_T3']=0
Initial_rows['E1_T4']=810


#  I use the same seqence of sessions as above. In particular, session Ct_29_05_1400 is the first one, etc.
# Now it is time to collect the useful data only:
May2018_PollData={}

for i in Sessions:
    May2018_PollData[i]=MAY_2018_PollsData[i][Initial_rows[i]:Initial_rows[i]+270]
    
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

for i in Sessions_Ct:
    May2018_PollData[i]=May2018_PollData[i][[*relevant_var_ct]]
                      
for i in Sessions_Tr:
    May2018_PollData[i]=May2018_PollData[i][[*relevant_var_tr]]
    
# Now let us drop the practice rounds. This will leave us with 225 observations per session:

for i in Sessions:
    May2018_PollData[i]=May2018_PollData[i][(May2018_PollData[i]['group.practice_round_number']>=1)]
    
# Now let us rename a few variables to make the data easier to work with:
for i in Sessions:
    May2018_PollData[i].columns = ['subject' if x=='participant.id_in_session' else 'round_number' if x== 'group.practice_round_number'    else 'poll_vote' if x== 'player.poll' else 'election_vote' if x=='player.vote' else 'belief_k' if x== 'player.belief_k'    else 'belief_j' if x== 'player.belief_j'else 'gender' if x== 'player.gender'else 'nationality' if x== 'player.nationality'    else 'major' if x== 'player.major' else 'income' if x== 'player.income'else 'total_earnings' if x== 'player.total_payoffs'    else x for x in May2018_PollData[i].columns]

# I now want to save the data in a form that does not have the subject as an index. But I have to be very careful:
# disctionaries are mutable, so simply storing the dictionary in another variable will generate an alias. I want to avoid that

May2018_PollDt=May2018_PollData.copy()         

# # And now let us put the subject id as an index, to help us with feeling the data
for i in Sessions:
    May2018_PollData[i]=May2018_PollData[i].set_index(['subject'])

# in the regression analysis, it seems that we do not need the index, if we need we just do it later, let comment these lines of codes    


# In[2]:


# let's get the data just for the econometrics part
frames = [] # this is for df concat   
frames_Ct = []
frames_Tr = []
for i in Sessions_Tr:
    May2018_PollData[i]['is_treatment'] = 1
    May2018_PollData[i]['average_k_inpolls'] = May2018_PollData[i][['group.biased1_k_inpolls','group.biased2_k_inpolls']].mean(axis=1)
#     frames_Tr.append(May2018_PollData[i])
for i in Sessions_Ct:
    May2018_PollData[i]['is_treatment'] = 0
    May2018_PollData[i]['average_k_inpolls'] = May2018_PollData[i][['group.companyA_k_inpolls','group.companyB_k_inpolls','group.companyC_k_inpolls','group.companyD_k_inpolls','group.companyE_k_inpolls']].mean(axis=1)
#     frames_Ct.append(May2018_PollData[i])
# print (May2018_PollData['Ct_29_05_1400'])
# print (May2018_PollData['Tr_29_05_1600'])

# Let's just simply keep the columns which are necessary
May2018_PollData_reg = {}
for i in Sessions:
    May2018_PollData_reg[i] = May2018_PollData[i][['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'group.k_inelection']]
    May2018_PollData_reg[i].columns = ['round_number', 'is_treatment', 'belief_k', 'average_k_inpolls', 'k_inelection']
    May2018_PollData_reg[i]['session'] = i     
    May2018_PollData_reg[i] = May2018_PollData_reg[i].groupby(['round_number']).mean()
    
    May2018_PollData_reg[i]['diff_BP'] = May2018_PollData_reg[i]['belief_k'] -  May2018_PollData_reg[i]['average_k_inpolls']
    May2018_PollData_reg[i]['diff_PV'] = May2018_PollData_reg[i]['average_k_inpolls'] - May2018_PollData_reg[i]['k_inelection']
    May2018_PollData_reg[i]['diff_BV'] = May2018_PollData_reg[i]['belief_k'] - May2018_PollData_reg[i]['k_inelection']
    
    
# dealing with lags
    May2018_PollData_reg[i]['diff_PV_lag'] = May2018_PollData_reg[i]['diff_PV'].shift(periods = 1)
    
    May2018_PollData_reg[i]['diff_BP_lag'] = May2018_PollData_reg[i]['diff_BP'].shift(periods = 1)
#     May2018_PollData_reg[i]['diff_BP_lagg'] = May2018_PollData_reg[i]['diff_BP'].shift(periods = 2)
#     May2018_PollData_reg[i]['diff_BP_laggg'] = May2018_PollData_reg[i]['diff_BP'].shift(periods = 3)
    
    May2018_PollData_reg[i]['diff_BV_lag'] = May2018_PollData_reg[i]['diff_BV'].shift(periods = 1)
    frames.append(May2018_PollData_reg[i])
# print (May2018_PollData_reg['Ct_29_05_1400'])

# lets just simply pool all the data together
All = pd.concat(frames).reset_index()      
# # # Let's also check for each treament
All_Tr = pd.concat([May2018_PollData_reg[i] for i in Sessions_Tr]).reset_index()  
All_Ct = pd.concat([May2018_PollData_reg[i] for i in Sessions_Ct]).reset_index()  

print (All)

# All.to_csv('All_E1.csv')
# In[7]:


# # # # we get all the data we needed, let try to work on it
####################################################################################################################
# result1 = smf.ols(formula="belief_k ~ round_number*is_treatment*average_k_inpolls", data= All).fit()
# result2 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls ", data= All_Tr).fit()
# result3 = smf.ols(formula="belief_k ~ round_number*average_k_inpolls", data= All_Ct).fit()

# dfoutput1 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput1)


######################################################################################################################
# result1 = smf.ols(formula= " k_inelection ~  average_k_inpolls + is_treatment + is_treatment*average_k_inpolls", data= All).fit()                                               
# result2 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Tr).fit()
# result3 = smf.ols(formula= " k_inelection ~  average_k_inpolls", data= All_Ct).fit()

# dfoutput2 = summary_col([result1,result2,result3],stars=True)
# print (dfoutput2)


#####################################################################################################################

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



# In[3]:


# # let's graphcailly illustrate diff_PV and diff_BP

# All_Tr.hist(column='diff_PV',  bins=10)

# All_Ct.hist(column='diff_PV',  bins=10)

# # All_Tr.hist(column='diff_BP',  bins=10)

# # All_Ct.hist(column='diff_BP',  bins=10)

sns.distplot(All_Tr['diff_PV'], label = "Treatment")
sns.distplot(All_Ct['diff_PV'], label = "Control")
plt.legend()
# plt.title('Distribution of differences between poll and election (E1)')
plt.xlabel('Differences between poll results and vote share of elections')
# plt.savefig('E1_diff_PV')

plt.show()
print (skew(All_Tr['diff_PV'].values))
print (np.mean(All_Tr['diff_PV'].values))
print (skew(All_Ct['diff_PV'].values))
print (np.mean(All_Ct['diff_PV'].values))


# sns.distplot(All_Tr['diff_BP'], label = "Treatment")
# sns.distplot(All_Ct['diff_BP'], label = "Control")
# plt.title('Distribution of differences between belief and poll (E1)')


# plt.legend()
# plt.savefig('E1_diff_BP')
# plt.show()


# In[3]:


# # in E2, how close reaveled polls between treatment and control

# sns.distplot(All_Tr['average_k_inpolls'], label = "Treatment")
# sns.distplot(All_Ct['average_k_inpolls'], label = "Control")
# plt.title('Distribution of average poll information in E1')


# plt.legend()
# plt.savefig('E1_average_k_inpolls')
# plt.show()


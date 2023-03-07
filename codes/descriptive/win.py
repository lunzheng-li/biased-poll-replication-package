import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

# os.chdir('/Users/lunzhengli/Desktop/new_figures')
os.chdir('/Users/lunzhengli/Library/CloudStorage/OneDrive-Personal/Biased_poll/new_figures')

Win_per = pd.read_excel('win.xlsx')
print(Win_per)

fig, ax = plt.subplots()

ax.plot(Win_per['Session'], Win_per['E1'],
        marker='v', linestyle="dotted", label='E1')
ax.plot(Win_per['Session'], Win_per['E2'], color='red',
        marker='s', linestyle="dotted", label='E2')
ax.plot(Win_per['Session'], Win_per['E3'], color='blue',
        marker='o', linestyle="dotted", label='E3')
ax.axvline(x=3.5, linestyle="-", color='gray')
# ax.axvspan(-0.2, 3.2, alpha=0.1, color='gray')
# ax.axvspan(3.8, 8.2, alpha=0.2, color='grey')
ax.legend()
ax.set_ylabel('K\'s Win Percentage by Session')
plt.show()

Vote = pd.read_excel('vote.xlsx')

fig, ax = plt.subplots()

ax.plot(Vote['Session'], Vote['E1'], marker='v',
        linestyle='dotted', label='E1')
ax.plot(Vote['Session'], Vote['E2'], color='red',
        marker='s', linestyle='dotted', label='E2')
ax.plot(Vote['Session'], Vote['E3'], color='blue',
        marker='o', linestyle='dotted', label='E3')
ax.legend()
ax.set_ylabel('K\'s Vote Share by Session')
plt.show()

Pearson = pd.read_excel('pearson.xlsx')

fig, ax = plt.subplots()

ax.plot(Pearson['Session'], Pearson['E1'],
        marker='v', linestyle='dotted', label='E1')
ax.plot(Pearson['Session'], Pearson['E2'], color='red',
        marker='s', linestyle='dotted', label='E2')
ax.plot(Pearson['Session'], Pearson['E3'], color='blue',
        marker='o', linestyle='dotted', label='E3')
ax.legend()
ax.set_ylabel('Pearson Correlation')
plt.show()

# Vote_diff=pd.read_excel('vote_diff.xlsx')

# fig, ax = plt.subplots()

# ax.plot(Vote_diff['round'], Vote_diff['E1'], marker='v', linestyle = 'dotted', label = 'E1')
# ax.plot(Vote_diff['round'], Vote_diff['E2'], color='red', marker='s', linestyle = 'dotted', label = 'E2')
# ax.plot(Vote_diff['round'], Vote_diff['E3'], color='blue', marker='o', linestyle = 'dotted', label = 'E3')
# ax.legend()
# ax.set_xlabel('Round Number')
# ax.set_ylabel('Treatment Effect by K\'s Vote Share')
# ax.axvspan(1.8, 4.2, alpha=0.2, color='yellow')
# ax.axvspan(5.8, 8.2, alpha=0.2, color='yellow')
# plt.xticks(Vote_diff['round'])
# plt.show()


########################################################################
# # work out the significance level of vote share diff by experiments.##
########################################################################

# Vote_diff_E1 = pd.read_csv('E1_vote_diff.csv')
# Vote_diff_E2 = pd.read_csv('E2_vote_diff.csv')
# Vote_diff_E3 = pd.read_csv('E3_vote_diff.csv')

# # print (stats.mannwhitneyu(Vote_diff_E1['control'], Vote_diff_E1['treatment'], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E2['control'], Vote_diff_E2['treatment'], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E3['control'], Vote_diff_E3['treatment'], alternative='less'))

# # MannwhitneyuResult(statistic=67.5, pvalue=0.03241777967534192)
# # MannwhitneyuResult(statistic=86.5, pvalue=0.14507140117701744)
# # MannwhitneyuResult(statistic=81.0, pvalue=0.09895308947498033)

# # print (stats.mannwhitneyu(Vote_diff_E1['control'][-5:], Vote_diff_E1['treatment'][-5:], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E2['control'][-5:], Vote_diff_E2['treatment'][-5:], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E3['control'][-5:], Vote_diff_E3['treatment'][-5:], alternative='less'))
# # MannwhitneyuResult(statistic=7.0, pvalue=0.1481349357421432)
# # MannwhitneyuResult(statistic=3.0, pvalue=0.030051402969433157)
# # MannwhitneyuResult(statistic=10.0, pvalue=0.33805165701157347)

# print(stats.mannwhitneyu(Vote_diff_E1['control'][Vote_diff_E1['diff'] > 0],
#                          Vote_diff_E1['treatment'][Vote_diff_E1['diff'] > 0], alternative='less'))
# print(stats.mannwhitneyu(Vote_diff_E2['control'][Vote_diff_E2['diff'] > 0],
#                          Vote_diff_E2['treatment'][Vote_diff_E2['diff'] > 0], alternative='less'))
# print(stats.mannwhitneyu(Vote_diff_E3['control'][Vote_diff_E3['diff'] > 0],
#                          Vote_diff_E3['treatment'][Vote_diff_E3['diff'] > 0], alternative='less'))
# MannwhitneyuResult(statistic=13.5, pvalue=0.00954835067432986)
# MannwhitneyuResult(statistic=32.5, pvalue=0.25379076818920454)
# MannwhitneyuResult(statistic=25.0, pvalue=0.09129695607674204)

# # print (stats.mannwhitneyu(Vote_diff_E1['control'][Vote_diff_E1['diff']<0], Vote_diff_E1['treatment'][Vote_diff_E1['diff']<0], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E2['control'][Vote_diff_E2['diff']<0], Vote_diff_E2['treatment'][Vote_diff_E2['diff']<0], alternative='less'))
# # print (stats.mannwhitneyu(Vote_diff_E3['control'][Vote_diff_E3['diff']<0], Vote_diff_E3['treatment'][Vote_diff_E3['diff']<0], alternative='less'))
# # MannwhitneyuResult(statistic=0.0, pvalue=0.0025374340489701264)
# # MannwhitneyuResult(statistic=0.0, pvalue=0.0025374340489701264)
# # MannwhitneyuResult(statistic=2.0, pvalue=0.0065326133822129805)

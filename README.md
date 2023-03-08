# biased-poll-replication-package

This repo contains the original data and the codes that reproduce the figures and results in the following paper:

**A. Boukouras, W. Jennings, L. Li, Z. Maniadis,"Can Biased Polls Distort Electoral Results? Evidence from the Lab." _European Journal of Political Economy_, forthcoming.**

- To make sense of the following explanations, you may want to have a quick look at the working paper  [here](https://github.com/lunzheng-li/MyWebsite/blob/main/pdf/BJLM2022_Biased%20polls.pdf).

- You can also find the oTree source code for the experiment [here](https://github.com/lunzheng-li/biased-poll-otree).

## `original data`

This folder contains all data from experiments E1, E2 and E3.

- `E1_data` and `E2_data` were collected at the Unversity of Southampton and Newcastle Business School between May and November 2018;
- `E3_data` was collected at the University of York in June 2019.

## `codes`

The `codes` folder consists of two parts:
- `descriptive`: codes that produce the descriptive results, such as **Figure 4**, **Figure 5** and results in the **Welfare Effects and Individual Behaviour** section. All codes are `python`.
- `regression`: codes that produce the regression results in **Appendix B**. `python` is used to clean the data, and `stata` is for regressions.

#### `descriptive`
1. running `E1.py`, `E2.py`, and `E3.py` gives you all the results in **Results** section. However, more work needs to be done to reproduce the exact figures.
    - For instance, running `E1.py` creates the following figure different from **Figure 4** in the paper.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223376891-d4f4c1c1-d4d1-4869-a612-cf4ea56dd50f.png" width="50%" height="50%"/>
        </p>
      
    - Also, after running  `E1.py`, `E2.py` and `E3.py`, you will see the following `.csv` files in your working directory.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223382582-d9b44189-e6cd-4418-86ff-a8b208bc2460.png" width="50%" height="50%"/>
        </p>
      
    - The `csv` files store the numbers in the figures. For instance, the following `E1_win.csv` is consistent with the bar graph above.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223389061-7dff6934-95d8-4a07-b4e4-546503158067.png" width="20%" height="20%"/>
        </p>
        
2. combine `E1_win.csv`,  `E2_win.csv` and `E3_win.csv`, so you have a `win.xlsx` file looks like following: 
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223532299-7cf1e94b-c49c-469b-a292-af28727160cb.png" width="50%" height="50%"/>
        </p>
        
        
    - combine all the  `*_vote.csv` files, and impelement the same process for all `*_pearon.csv` files, and you will have a `win.xlsx`, a `vote.xlsx` and a `pearson.xlsx` that contain the results of all three experiments.
    - put all the these combined `csv` files in the same directory with `win.py`

3. run `win.py`, and it gives you the figures in **Figure 4**.

4. `E1_additional_analysis.py`,`E2_additional_analysis.py` and `E3_additional_analysis.py` produce results in **Welfare Effects and Individual Behaviour** section and the tables in **Appendix D**.
    - Note that code does not output the tables directly, and some straightforward calculations and copy&paste work are still needed.

##### `regression`

1. running `E1_reg.py`, `E2_reg.py` and `E3_reg.py` gives you `All_E1.csv`, `All_E2.csv` and `All_E3.csv`, and these are cleaned-up data for regressions.
     - Note that there is code for regressions at the end of the `python` scripts. However, I wasn't familiar with `statsmodels` package at the time, I switched to `stata` instead.

        
2. run `cluster.do` to generate the results in **Appendix B Additonal Econometric Analysis**。
     - The `.do` file tests six models and only _"model 1"_ and _"model 3"_ in the script are presented in the online appendix of the final version.

Notes: I apologise that the `E1.py`, `E2.py` and `E3.py` scripts are a bit messy. They are code drafts that also produce figures and results that, in the end, do not present in the final version of the paper. For the purpose of replicating the result of the final version, we commented out unnecessary code blocks. Should you have any questions, please email me at lunz3706@outlook.com.


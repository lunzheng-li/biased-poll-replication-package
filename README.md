# biased-poll-replication-package

This repo contains the original data and the code that reproduces the figures and results in the following paper:

**A. Boukouras, W. Jennings, L. Li, Z. Maniadis,"Can Biased Polls Distort Electoral Results? Evidence from the Lab." _European Journal of Political Economy_, forthcoming.**

- To make sense of the following explainations, you may want to have a quick look at the working paper  [here](https://github.com/lunzheng-li/MyWebsite/blob/main/pdf/BJLM2022_Biased%20polls.pdf).

- You can also find the oTree source code for the experiment [here](https://github.com/lunzheng-li/biased-poll-otree).

## `original data`

This folder contains all data from experiment E1, E2 and E3.

- `E1_data` and `E2_data` were collected at the Unversity of Southampton and Newcastle Business School between May and November 2018;
- `E3_data` was collected at the University of York in June 2019.

## `codes`

The `codes` folder consists of two parts:
- `descriptive`: codes that produce the descriptive results, such as **Figure 4**, **Figure 5** and results in the **Welfare Effects and Individual Behaviour** section. All codes are `python`.
- `regression`: codes that produce the regression results in **Appendix B**. `python` is used to clean the data and `stata` is for regressions.

#### descriptive
1. running `E1.py`, `E2.py` and `E3.py` gives you all the results in **Results** section. However, more work need to be done to reproduce the same figures.
    - For instance, running `E1.py` creates following figure which is different from Figure 4 in the paper.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223376891-d4f4c1c1-d4d1-4869-a612-cf4ea56dd50f.png" width="50%" height="50%"/>
        </p>
      
    - Also, after running  `E1.py`, `E2.py` and `E3.py`, you will see the following `.csv` files in your working directory.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223382582-d9b44189-e6cd-4418-86ff-a8b208bc2460.png" width="50%" height="50%"/>
        </p>
      
    - The `csv` files just store the numbers in the figures. For instance, the following `E1_win.csv` is consistent with the bar graph above.
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223389061-7dff6934-95d8-4a07-b4e4-546503158067.png" width="20%" height="20%"/>
        </p>
        
2. combine `E1_win.csv`,  `E2_win.csv` and `E3_win.csv`, so you a `win.xlsx` file looks like following: 
        <p align="center">
            <img src="https://user-images.githubusercontent.com/68153897/223532299-7cf1e94b-c49c-469b-a292-af28727160cb.png" width="50%" height="50%"/>
        </p>
        
        
    - combine all the  `*_vote.csv` files, and the same process for all `*_pearon.csv`, and you have `win.xlsx`, `vote.xlsx` and `pearson` that contain the results of all three expriments.
    - put all the these combine `csv` files in the same directory with `win.py`

3. run the `win.py`, and it gives you the figures in **Figure 4**.

4. The `E1` produce that result in **Welfare Effects and Individual Behaviour** section and the tables in **Appendix D**
    - Note that code would produce the tables directly, some strightforward calculations and copy&paste work are still needed.

##### regression
        





Notes: I apologise that the `E1.py`, `E2.py` and `E3.py` scripts are a bit messy. They are code drafts that also produce figures and results that, in the end, do not presented in the final version of the paper. For purpose of replicating the result of final version, we commented out unnecessay code blocks. Should you have any questions, please email me at lunz3706@outlook.com.


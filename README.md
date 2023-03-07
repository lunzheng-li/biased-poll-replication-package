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
- `descriptive`: codes that produce the descriptive results, such as _Figure 4_, _Figure 5_ and results in the _"Welfare Effects and Individual Behaviour"_ section. All codes are `python`.
- `regression`: codes that produce the regression results in _"Appendix B"_. `python` is used to clean the data and `stata` is for regressions.

#### descriptive
1. running `E1.py`, `E2.py` and `E3.py` gives all the results in _"3 Results"_. However, more work need to be done to reproduce the same figures.
    - for instance, running `E1.py` creates following figure which is different from Figure 4 in the paper.
    
      ![Figure_1](https://user-images.githubusercontent.com/68153897/223376891-d4f4c1c1-d4d1-4869-a612-cf4ea56dd50f.png)
      
    - Also, after running  `E1.py`, `E2.py` and `E3.py`, you will see the following `.csv` files in your working directory.
        ![SCR-20230307-g4d](https://user-images.githubusercontent.com/68153897/223382582-d9b44189-e6cd-4418-86ff-a8b208bc2460.png)
      
      They are just the numbers in the figures. For instance, the follwing `E1_win.csv` that is consistent with the bar graph above.
      
        ![image](https://user-images.githubusercontent.com/68153897/223389061-7dff6934-95d8-4a07-b4e4-546503158067.png)




Notes: Sorry that the `python` scripts are all a bit messy. They are code drafts that also produce figures and results that, in the end, do not presented in the final version of the paper. For purpose of replicating the result of final version, we commented out unnecessay code blocks. Should you have any questions, please email me at lunz3706@outlook.com.


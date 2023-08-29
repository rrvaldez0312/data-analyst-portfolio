# transforming dataset using python

import pandas as pd

powerball = pd.read_csv("Lottery_Powerball_Winning_Numbers__Beginning_2010.csv")

# splitting powerball numbers into multiple columns

powerball[["p1", "p2", "p3", "p4", "p5", "m"]] = powerball["Winning Numbers"].str.extract("(\d+) (\d+) (\d+) (\d+) (\d+) (\d+)", expand=True).astype(int)

winning_numbers = powerball[["p1", "p2", "p3", "p4", "p5"]].copy()
cols = ['p2', 'p3', 'p4', 'p5']

winning_numbers['p1'] = winning_numbers[cols].sum(1)
winning_numbers = winning_numbers.drop(cols, 1)
winning_numbers

import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
#from linearmodels import PanelOLS

df = pd.read_csv('paneldata.csv')
'''
df = df.pivot_table(values=['diffrepo','difffo','diffco'] , index = 'uid', columns = 'timestamp')
regression = PanelOLS(y=df['difffo'], x=df[['diffrepo', 'diffco']])
'''
model = sm.OLS(formula = "difffo ~ diffrepo + diffco + difflike", data = df, time_effects=True).fit()
#model = pd.ols(y='difffo', x=['diffpo', 'diffco', 'difflike'], time_effects=True, entity_effects=True)
print(model.summary())
#res = sm.ols(formula = "follower ~ likes + comment + repost + gender + picindex + lenindex", data = df).fit()

#print(res.summary())
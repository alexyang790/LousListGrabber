import pandas as pd 

data = pd.read_csv('data.csv')

print(data.head().to_dict(orient='records'))

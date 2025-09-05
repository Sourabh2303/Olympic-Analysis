import pandas as pd

def preprocess(df,region_df):

    #filtering for summer olympics
    df=df[df['Season']=='Summer']
    #merge with region_df
    df = df.merge(region_df[['NOC', 'region', 'notes']], how='left', on='NOC')

    #dropping Duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medals
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)


    return df
import pandas as pd


def preprocess(df, region_df):
    # Filter only Summer Olympics directly with .loc for speed
    df = df.loc[df['Season'] == 'Summer'].copy()

    # Merge with region_df (only required columns)
    df = df.merge(region_df[['NOC', 'region']], how='left', on='NOC')

    # Drop duplicates (in-place, faster)
    df.drop_duplicates(inplace=True, ignore_index=True)

    # One-hot encode medals (Gold, Silver, Bronze) - avoids unnecessary dtypes
    medal_dummies = pd.get_dummies(df['Medal'], dtype='int8')
    df = pd.concat([df, medal_dummies], axis=1)

    return df

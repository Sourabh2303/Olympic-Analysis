import numpy as np
import pandas as pd


# -------------------------
# Medal Tally
# -------------------------
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = (temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']]
             .sum().sort_index().reset_index())
    else:
        x = (temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']]
             .sum().sort_values('Gold', ascending=False).reset_index())

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


# -------------------------
# Country & Year List
# -------------------------
def country_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


# -------------------------
# Data Over Time
# -------------------------
def data_over_time(df, col):
    nations_over_time = (df.drop_duplicates(['Year', col])
                           .groupby('Year')
                           .count()[col]
                           .reset_index())
    nations_over_time.rename(columns={col: col}, inplace=True)
    nations_over_time.rename(columns={'Year': 'Editions'}, inplace=True)
    return nations_over_time


# -------------------------
# Most Successful Athletes
# -------------------------
def most_success(df, sport, top_n=15):
    temp_df = df.dropna(subset=['Medal'])

    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = (temp_df['Name'].value_counts()
         .reset_index()
         .head(top_n)
         .merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']]
         .drop_duplicates('index'))
    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)

    return x


# -------------------------
# Country Yearwise Medal Tally
# -------------------------
def country_yearwise_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    final_df = (temp_df.groupby('Year').count()['Medal']
                .reset_index())
    return final_df


# -------------------------
# Country Event Heatmap
# -------------------------
def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    pt = (temp_df.drop_duplicates(['Year', 'Sport', 'Event'])
                  .pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
                  .fillna(0))
    return pt


# -------------------------
# Most Successful Athletes (Countrywise)
# -------------------------
def most_successfull_countrywise(df, country, top_n=10):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = (temp_df['Name'].value_counts()
         .reset_index()
         .head(top_n)
         .merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport']]
         .drop_duplicates('index'))
    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)

    return x


# -------------------------
# Weight vs Height
# -------------------------
def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Ensure "No Medal" exists in categories before filling
    if pd.api.types.is_categorical_dtype(athlete_df['Medal']):
        if "No Medal" not in athlete_df['Medal'].cat.categories:
            athlete_df['Medal'] = athlete_df['Medal'].cat.add_categories(["No Medal"])
    athlete_df['Medal'] = athlete_df['Medal'].fillna("No Medal")

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    return temp_df


# -------------------------
# Men vs Women Participation
# -------------------------
def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = (athlete_df[athlete_df['Sex'] == 'M']
           .groupby('Year')
           .count()['Name']
           .reset_index())
    women = (athlete_df[athlete_df['Sex'] == 'F']
             .groupby('Year')
             .count()['Name']
             .reset_index())

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

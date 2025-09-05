import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    # Work on only necessary columns
    medal_df = df.drop_duplicates(
        subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'],
        keep='first'
    )

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df.loc[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df.loc[medal_df['Year'] == year]
    else:
        temp_df = medal_df.loc[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = (
            temp_df.groupby('Year', as_index=False)[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Year')
        )
    else:
        x = (
            temp_df.groupby('region', as_index=False)[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Gold', ascending=False)
        )

    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    return x


def data_over_time(df, col):
    nations_over_time = (
        df.drop_duplicates(['Year', col])
        .groupby('Year')[col]
        .count()
        .reset_index()
        .rename(columns={'Year': 'Editions', col: col})
    )
    return nations_over_time


def medal_tally(df):
    medal_tally1 = (
        df.drop_duplicates(subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal'])
        .groupby('region', as_index=False)[['Gold', 'Silver', 'Bronze']]
        .sum()
        .sort_values('Gold', ascending=False)
    )
    medal_tally1['total'] = medal_tally1[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    return medal_tally1


def country_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    country = sorted(df['region'].dropna().unique().tolist())
    country.insert(0, 'Overall')

    return years, country


def most_success(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(15)
        .merge(df[['Name', 'Sport', 'region']], on='Name', how='left')
        .drop_duplicates('Name')
    )
    x.rename(columns={'count': 'medals'}, inplace=True)
    return x


def country_yearwise_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', "City", 'Sport', "Event", 'Medal']
    )
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year', as_index=False)['Medal'].count()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', "City", 'Sport', "Event", 'Medal']
    )
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(
        index='Sport', columns='Year', values='Medal', aggfunc='count', fill_value=0
    )
    return pt


def most_successfull_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(10)
        .merge(df[['Name', 'Sport']], on='Name', how='left')
        .drop_duplicates('Name')
    )
    x.rename(columns={'count': 'medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'region']).copy()
    athelete_df['Medal'] = athelete_df['Medal'].fillna('No Medal')

    if sport != 'Overall':
        return athelete_df[athelete_df['Sport'] == sport]
    return athelete_df


def men_v_women(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year', as_index=False)['Name'].count()
    women = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year', as_index=False)['Name'].count()

    final = men.merge(women, on='Year', how='outer').fillna(0)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    return final

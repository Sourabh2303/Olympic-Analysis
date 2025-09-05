import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=['Team', 'Games', 'NOC', 'City', 'Sport', 'Event', 'Medal']
    )

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
        x = (
            temp_df.groupby('region')
            .sum()[['Gold', 'Silver', 'Bronze']]
            .sort_values('Gold', ascending=False)
            .reset_index()
        )
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        x = (
            temp_df.groupby('Year')
            .sum()[['Gold', 'Silver', 'Bronze']]
            .sort_values('Year')
            .reset_index()
        )
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
        x = (
            temp_df.groupby('region')
            .sum()[['Gold', 'Silver', 'Bronze']]
            .sort_values('Gold', ascending=False)
            .reset_index()
        )
    else:  # both year and country selected
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
        x = (
            temp_df.groupby('region')
            .sum()[['Gold', 'Silver', 'Bronze']]
            .reset_index()
        )

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def data_over_time(df, col):
    df = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    df.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    df = df.sort_values('Edition')
    return df


def most_successful(df, sport, top_n=15):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(top_n)
        .merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']]
        .drop_duplicates('index')
    )

    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(['Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = (
        new_df.groupby('Year')
        .count()['Medal']
        .reset_index()
    )
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    new_df = temp_df[temp_df['region'] == country]

    if new_df.empty:
        return pd.DataFrame()  # return empty safely

    pt = new_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count',
        fill_value=0,
        observed=False  # avoid pandas FutureWarning
    )

    return pt


def most_successful_countrywise(df, country, top_n=10):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(top_n)
        .merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport']]
        .drop_duplicates('index')
    )

    x.rename(columns={'index': 'Athlete', 'Name_x': 'Medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    return temp_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = (
        athlete_df[athlete_df['Sex'] == 'M']
        .groupby('Year')
        .count()['Name']
        .reset_index()
    )
    women = (
        athlete_df[athlete_df['Sex'] == 'F']
        .groupby('Year')
        .count()['Name']
        .reset_index()
    )

    final = men.merge(women, on='Year', how='left').fillna(0)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final

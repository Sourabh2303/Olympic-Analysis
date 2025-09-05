import streamlit as st
import pandas as pd
import preprocess, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


# -------------------------
# Cache Data Loading
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    df = preprocess.preprocess(df, region_df)

    # Optimize memory
    cat_cols = ['Sex', 'Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal', 'region']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    return df


df = load_data()

# -------------------------
# Sidebar Menu
# -------------------------
st.sidebar.title('🏅 Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athelete-wise Analysis')
)


# -------------------------
# Medal Tally
# -------------------------
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")
    else:
        st.title(f"{selected_country}'s Performance in {selected_year} Olympics")

    st.dataframe(medal_tally, use_container_width=True)


# -------------------------
# Overall Analysis
# -------------------------
elif user_menu == 'Overall Analysis':
    st.title('📊 Overall Statistics')

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    atheletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Host Cities", cities)
    col3.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Nations", nations)
    col3.metric("Athletes", atheletes)

    # Nations over time
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Editions', y='region', markers=True)
    st.subheader('Participating Nations Over the Years')
    st.plotly_chart(fig, use_container_width=True)

    # Events over time
    event_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(event_over_time, x='Editions', y='Event', markers=True)
    st.subheader('Events Over the Years')
    st.plotly_chart(fig, use_container_width=True)

    # Athletes over time
    athelete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athelete_over_time, x='Editions', y='Name', markers=True)
    st.subheader('Athletes Over the Years')
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap (with annot=True kept!)
    st.subheader("Number of Events over Time (per Sport)")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
    st.pyplot(fig)

    # Most successful athletes
    st.subheader('Most Successful Athletes')
    sport_list = sorted(df['Sport'].unique().tolist())
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_success(df, selected_sport)
    st.dataframe(x, use_container_width=True)


# -------------------------
# Country-wise Analysis
# -------------------------
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df = helper.country_yearwise_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal', markers=True)
    st.subheader(f"{selected_country} Medal Tally over the Years")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"{selected_country} Excels in These Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if pt.empty:
        st.warning(f"No medal records available for {selected_country}.")
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(pt, annot=True, fmt="g", cmap="YlGnBu")
        st.pyplot(fig)

    st.subheader(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successfull_countrywise(df, selected_country)
    st.dataframe(top10_df, use_container_width=True)


# -------------------------
# Athlete-wise Analysis
# -------------------------
elif user_menu == "Athelete-wise Analysis":
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Distribution of Age
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold', 'Silver', 'Bronze'],
                             show_hist=False, show_rug=False)
    st.subheader('Distribution of Age')
    st.plotly_chart(fig, use_container_width=True)

    # Distribution wrt Sports (full list kept)
    x, name = [], []
    famous_sports = [
        'Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming',
        'Badminton','Sailing','Gymnastics','Art Competitions',
        'Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing',
        'Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball','Archery','Volleyball','Synchronized Swimming','Table Tennis',
        'Baseball','Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon',
        'Rugby','Polo','Ice Hockey'
    ]
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_rug=False, show_hist=False)
    st.subheader('Distribution of Age wrt Sports (Gold Medalists)')
    st.plotly_chart(fig, use_container_width=True)

    # Height vs Weight
    sport_list = sorted(df['Sport'].unique().tolist())
    sport_list.insert(0, 'Overall')
    st.subheader('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],
                    hue=temp_df['Medal'], style=temp_df['Sex'], s=50, ax=ax)
    st.pyplot(fig)

    # Men vs Women participation
    st.subheader("Men vs Women Participation over the Years")
    final = helper.men_v_women(df)
    fig = px.line(final, x='Year', y=['Male', "Female"], markers=True)
    st.plotly_chart(fig, use_container_width=True)

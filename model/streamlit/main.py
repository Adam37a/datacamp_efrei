import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from st_on_hover_tabs import on_hover_tabs
import plotly.express as px

csv_path = os.path.join(os.path.dirname(__file__), 'sentiments_mappes_output_final.csv')
df = pd.read_csv(csv_path, delimiter=';')

st.set_page_config(layout="wide")
style_path = os.path.join(os.path.dirname(__file__), 'style.css')

df['Date de publication'] = pd.to_datetime(df['Date de publication'], format='ISO8601')
df['Year'] = df['Date de publication'].dt.year

sentiment_options = df['Sentiment Description'].unique()

min_year, max_year = df['Year'].min(), int(df['Year'].max())
selected_year = st.slider('Filtre par année', min_value=min_year, max_value=max_year, value=(min_year, max_year))
selected_sentiments = st.multiselect('Filtre par Sentiment', options=sentiment_options, default=sentiment_options)

filtered_df = df[(df['Sentiment Description'].isin(selected_sentiments)) &
                 (df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1])]


total_reviews = len(filtered_df)
average_note = filtered_df['Predicted Sentiment'].mean()
latest_review_date = filtered_df['Date de publication'].max()

st.markdown('<style>' + open(style_path).read() + '</style>', unsafe_allow_html=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Tableau de bord', 'Nuage de mots', 'Carte'],
                         iconName=['dashboard', 'Nuage de mots', 'Carte'], default_choice=0)

if tabs == 'Tableau de bord':
    st.title('Avis Luggage Superstore')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total des avis", value=total_reviews)
    with col2:
        st.metric(label="Note moyenne prédict", value=round(average_note, 2))
    with col3:
        average_sentiment_description = filtered_df['Sentiment Description'].mode()[0]
        st.metric(label="Sentiment moyen prédict", value=average_sentiment_description)

    st.title('Note moyenne par année et par sentiment')
    yearly_avg_note = filtered_df.groupby(['Year', 'Sentiment Description'])['Predicted Sentiment'].mean().unstack(
        fill_value=0)
    st.bar_chart(yearly_avg_note)
    st.title('Distribution des notes par année')
    note_distribution = filtered_df.groupby(['Year', 'Sentiment Description']).size().unstack(fill_value=0)
    st.bar_chart(note_distribution)

elif tabs == 'Nuage de mots':
    text = " ".join(str(review) for review in filtered_df["Contenu de l'avis"])
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    st.title(
        f'Nuage de mots des avis pour les années {selected_year[0]}-{selected_year[1]} et les sentiments sélectionnés')
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

elif tabs == 'Carte':
    st.title("Carte")
    review_counts = filtered_df['Pays'].value_counts().reset_index()
    review_counts.columns = ['Pays', 'Review Count']
    fig = px.choropleth(
        review_counts,
        locations="Pays",
        locationmode="country names",
        color="Review Count",
        hover_name="Pays",
        color_continuous_scale=px.colors.sequential.Reds,
        title="Nombre d'avis par pays"
    )
    fig.update_layout(margin=dict(l=23, r=23, t=23, b=23))

    st.plotly_chart(fig, use_container_width=True)
    fig = px.pie(
        review_counts,
        names='Pays',
        values='Review Count',
        title="Nombre d'avis par pays",
    )
    fig.update_layout(margin=dict(l=23, r=23, t=23, b=23))
    st.plotly_chart(fig, use_container_width=True)
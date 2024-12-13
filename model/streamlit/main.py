import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from st_on_hover_tabs import on_hover_tabs
import plotly.express as px

csv_path = os.path.join(os.path.dirname(__file__), 'sentiments_mappés.csv')
df = pd.read_csv(csv_path, delimiter=';')

st.set_page_config(layout="wide")
style_path = os.path.join(os.path.dirname(__file__), 'style.css')

df['Date de publication'] = pd.to_datetime(df['Date de publication'], format='ISO8601')
df['Year'] = df['Date de publication'].dt.year

sentiment_options = df['Sentiment Description'].unique()
selected_sentiments = st.multiselect('Filtre par Sentiment', options=sentiment_options, default=sentiment_options)

min_year, max_year = df['Year'].min(), int(df['Year'].max())
selected_year = st.slider('Filtre par année', min_value=min_year, max_value=max_year, value=(min_year, max_year))

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
    st.write("""Tableau de bord
    
   Total des avis et note moyenne prédite :
   Le total des avis permet d'évaluer l'ampleur des retours clients sur une période donnée. Un nombre élevé indique une forte participation des clients.
   La note moyenne prédite reflète le sentiment général des clients. Une note élevée indique une satisfaction majoritairement positive, tandis qu'une note faible signale des points à améliorer dans les services ou produits.
   
   Sentiment moyen prédit :
   Le sentiment dominant permet d'identifier le ressenti majoritaire des clients (positif, neutre ou négatif). Cela aide les équipes métier à prioriser les actions correctives ou à renforcer les aspects appréciés.
   
   Note moyenne par année et par sentiment :
   Ce graphique met en évidence l'évolution des sentiments clients au fil des années. Une amélioration constante peut refléter un effet positif des actions entreprises par l’entreprise.
   Il aide également à identifier les années où des sentiments négatifs prédominent, permettant ainsi d’analyser les causes spécifiques et de les corriger.
   
   Distribution des notes par année :
   La répartition des notes par année et sentiment fournit une vue plus granulaire sur l’engagement des clients et la diversité des sentiments exprimés.
   Elle peut révéler des tendances saisonnières ou des pics d’avis positifs/négatifs liés à des événements spécifiques (nouveaux produits, campagnes marketing, etc.).
   """)

elif tabs == 'Nuage de mots':
    text = " ".join(str(review) for review in filtered_df["Contenu de l'avis"])
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    st.title(
        f'Nuage de mots des avis pour les années {selected_year[0]}-{selected_year[1]} et les sentiments sélectionnés')
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    st.write("""
    Le nuage de mots extrait les mots-clés les plus fréquents des avis, mettant en lumière les sujets récurrents. Par exemple, des termes positifs comme &quot;excellent&quot; ou &quot;rapide&quot; indiquent des points forts, tandis que des mots comme &quot;problème&quot; ou &quot;retard&quot; signalent des axes d’amélioration.
    Cela peut guider les priorités métier pour répondre rapidement aux préoccupations des clients et optimiser l’expérience utilisateur.
    
    Pertinence pour les solutions métier :
    Les mots les plus fréquents peuvent indiquer les attentes principales des clients. 
    Les équipes peuvent aligner les stratégies sur ces attentes pour améliorer la satisfaction.
    """)

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

    st.write(""" Carte des avis par pays :
    
    Le choroplèthe montre la répartition géographique des avis, ce qui aide à identifier les marchés les plus engageants ou ceux nécessitant davantage d'attention.
    Les zones avec un faible volume d'avis peuvent signaler un manque de visibilité ou d'engagement dans ces régions, offrant des opportunités de croissance.
    
    Graphique circulaire :
    Ce graphique permet de visualiser rapidement les contributions relatives des pays en termes d’avis. Cela peut aider les équipes métier à adapter leurs stratégies marketing ou de service selon la répartition régionale. """)


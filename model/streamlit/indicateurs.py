import streamlit as st
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

def show_page () :
        # Load the data
        csv_path = os.path.join(os.path.dirname(__file__), 'luggage_superstore_reviews.csv')
        df = pd.read_csv(csv_path)

        # Extract the first digit from the 'Note' column
        df['Note'] = df['Note'].str.extract(r'(\d)').astype(int)

        # Convert the 'Date de publication' column to datetime
        df['Date de publication'] = pd.to_datetime(df['Date de publication'])

        # Extract the year from the 'Date de publication' column
        df['Year'] = df['Date de publication'].dt.year

        # Calculate indicators
        total_reviews = len(df)
        average_note = df['Note'].mean()
        latest_review_date = df['Date de publication'].max()

        # Display indicators
        st.title('Luggage Superstore Reviews')
        st.metric(label="Total ", value=total_reviews)
        st.metric(label="Moyenne Note", value=round(average_note, 2))
        st.metric(label="Dernière Note Date", value=latest_review_date.strftime('%Y-%m-%d'))

        # Display the first chart: Average Note by Year
        st.title('Average Note by Year')
        yearly_avg_note = df.groupby('Year')['Note'].mean().reset_index()
        chart = st.empty()
        for year in yearly_avg_note['Year']:
                data = yearly_avg_note[yearly_avg_note['Year'] <= year]
                chart.bar_chart(data.set_index('Year'))
                time.sleep(0.5)

        # Display the second chart: Note Distribution by Year
        st.title('Note Distribution by Year')
        note_distribution = df.groupby(['Year', 'Note']).size().unstack(fill_value=0)
        st.bar_chart(note_distribution)
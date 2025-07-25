# utils/visualizer.py

import matplotlib.pyplot as plt
import streamlit as st

def create_ats_pie_chart(score):
    """Creates and displays a pie chart for the ATS score."""
    score = max(0, min(100, score)) # Ensure score is between 0 and 100
    
    # Data for the pie chart
    labels = ['ATS Match Score', 'Missing']
    sizes = [score, 100 - score]
    colors = ['#4CAF50', '#FF9999']
    explode = (0.1, 0)  # Explode the 'ATS Match Score' slice

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140, textprops={'color':"w", 'weight':'bold'})
    
    # Set background to transparent to match Streamlit theme
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)
import matplotlib.pyplot as plt
import streamlit as st

def plot_bias_meter(bias_score):
    """
    Plot a pie chart that visualizes political bias.
    
    Args:
        bias_score (float): Bias score between -1 (left) to 1 (right).
    """
    labels = ['Left', 'Center', 'Right']
    sizes = [abs(bias_score), 1 - abs(bias_score), abs(-bias_score)]
    colors = ['lightcoral', 'gold', 'lightskyblue']
    explode = (0.1 if bias_score < 0 else 0, 0, 0.1 if bias_score > 0 else 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  
    
    st.pyplot(fig1)

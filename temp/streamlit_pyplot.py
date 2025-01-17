import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate data
arr = np.random.normal(1, 1, size=100)
chart_data = pd.DataFrame(
    {
        "col1": list(range(20)) * 3,  # 60 values in total (0-19 repeated 3 times)
        "col2": np.random.randn(60),  # 60 random values
        "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,  # Categories A, B, C
    }
)

# Create plots
fig, ax = plt.subplots(1, 2, figsize=(14, 6))  # Create 1 row, 2 columns of plots

# Left plot: Histogram
ax[0].hist(arr, bins=80, color='blue', alpha=0.7)
ax[0].set_title('Histogram of Random Data')

# Right plot: Bar chart
colors = {'A': 'blue', 'B': 'orange', 'C': 'green'}  # Mapping categories to colors
ax[1].bar(chart_data['col1'], chart_data['col2'], color=[colors[c] for c in chart_data['col3']])
ax[1].set_title('Bar Chart with Categories')
ax[1].set_xlabel('X-axis (col1)')
ax[1].set_ylabel('Y-axis (col2)')

# Add a main title
fig.suptitle("Main Title for Both Plots")

# Display the plot in Streamlit
st.pyplot(fig)

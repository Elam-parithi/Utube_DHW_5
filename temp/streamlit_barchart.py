import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    {
        "col1": list(range(20)) * 3, # total 60 values 20 per color
        "col2": np.random.randn(60),    # random 60 chars
        "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,  # a,b,c 20 per color per char total 60
    }
)

st.bar_chart(chart_data, x="col1", y="col2", color="col3")
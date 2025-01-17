import streamlit as st

st.html("""
<style>
.custom-button {
   background-color: #4CAF50;
   color: white;
   padding: 14px 20px;
   margin: 8px 0;
   border: none;
   cursor: pointer;
   width: 100%;
}
.custom-button:hover {
   opacity: 0.8;
}
</style>
<button class="custom-button">Custom Button</button>
""")

if st.button('Click Me', key='my_button',
             help='Click this button to perform an action'):
    st.write('You clicked the button!')

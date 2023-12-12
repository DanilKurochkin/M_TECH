import streamlit as st
import pandas as pd
from utils import create_dataframe
import matplotlib.pyplot as plt
import seaborn as sns

file = None
df : pd.DataFrame = None

st.header('Загрузите файл для анализа')
file = st.file_uploader("Выберите файл")
if file is not None:
    lines = file.readlines()
    lines = list(map(lambda x: x.decode('cp1251'), lines))
    df = create_dataframe(lines)
    st.header('Результаты анализа')
    st.text('-------')
    figure = plt.figure()
    sns.countplot(data=df, x='Количество больничных дней')
    st.pyplot(figure)
import streamlit as st
import numpy as np
import pandas as pd
from classes.utils import create_dataframe
from classes.statistics import uelch_statistic_check
import matplotlib.pyplot as plt
import seaborn as sns

def statistics_report(X1 : pd.Series, X2:pd.Series,
                      work_days : int, alpha : float):
    
    result, test_statistics, test_critical_statistics=uelch_statistic_check(X1, X2, work_days, alpha)                             
        
    st.text(f'Посчитаем статистику: {test_statistics:.3f}')
    st.text(f'Посчитаем критическую статистику: {test_critical_statistics:.3f}')
    
    if result:
        st.text('Нулевая гипотеза принимается')
        st.text(f'Так как:{test_statistics:.3f} > {test_critical_statistics:.3f}')
    else:
        st.text('Нулевая гипотеза отколняется в пользу альтернативной')
        st.text(f'Так как:{test_statistics:.3f} < {test_critical_statistics:.3f}')
        
    st.text(f'При статистической значимости: {alpha}')


def draw_graphs(df : pd.DataFrame, hue : str):
    sns.countplot(data=df, x='Количество больничных дней', hue=hue)
    plt.ylabel('Количество сотрудников')
    st.pyplot(figure)
    figure.clear()
    
    sns.boxplot(data=df, x='Количество больничных дней', hue=hue)
    st.pyplot(figure)
    figure.clear()

#функция для нахождения сотрудников страше данного возраста
def elder_than(x, age):
    if x > age:
        return 'Да'
    
    return 'Нет'

#стартовая страница, анализ начнётся только после загрузки файла с данными
st.header('Загрузить файл для анализа')
file = st.file_uploader("Выберите файл")

#после загрузки файла
if file is not None:
    #обработка входнго файла
    lines = file.readlines()
    lines = list(map(lambda x: x.decode('cp1251'), lines))
    df = create_dataframe(lines)
    
    
    st.header('Результаты анализа')
    
    st.text('Распределение больничных во всей выборке')
    figure = plt.figure()
    sns.countplot(data=df, x='Количество больничных дней')
    plt.ylabel('Количество дней на больничном')
    st.pyplot(figure)
    figure.clear()
    
    #поля ввода для входных данных
    age = st.slider(label='Выберите возраст',
                    min_value=df['Возраст'].min(),
                    max_value=df['Возраст'].max())
    
    work_days = st.slider(label='Количество пропущенных рабочих дней',
                          min_value=df['Количество больничных дней'].min(),
                          max_value=df['Количество больничных дней'].max())
    
    alpha = st.number_input(label='Статистическая значимость',
                            max_value=1.0,
                            min_value=0.0,
                            value=0.05)
    
    #после ввода данных можно приступить к расчёту и построению графиков
    start_calculation_button = st.button(label='Начать расчёт')
    
    if start_calculation_button:
        #постановка гипотез и доводы в пользу данного критерия проверки
        st.header('Выдвенем следующие гипотезы:')
        st.text(f'''
                H₀ : M₁ - M₂ >= {work_days}
                H₁ : M₁ - M₂ < {work_days}
                Левосторонний тест
                ''')
        
        st.header('Используем t-тест Уэлча')
        st.text('''
                Выбираем его, так как нет оснований полагать о равенстве дисперсий
                И более того, даже если дисперсии равны, t-тест Уэлча корректен
                ''')
        st.text('''
                На больших выборках, даже при ненормальном распределении, t-тесты работают.
                t-критерий предполагает, что средние значения различных выборок, взятых из
                генеральной совокупности, нормально распределены.
                Это не предполагает, что вся генеральная совокупность распределена нормально.
                ''')
        
        #обработка данных для выборок по полу
        st.header('Связь пола и колечества дней на больничном')
        
        #построение графиков
        draw_graphs(df, 'Пол')
        
        #разбиение данных на две выборки
        X1_sex = df[df['Пол'] == 'М']['Количество больничных дней']
        X2_sex = df[df['Пол'] == 'Ж']['Количество больничных дней']
        
        #проведение теста по критерию
        statistics_report(X1_sex, X2_sex, work_days, alpha)
        

        #обработка данных для выборок по возрасту
        st.header('Связь возраста и колечества дней на больничном')
        #создание дополнительной колонки в данных, для удобной фильтрации
        df[f'Cтарше {age}'] = np.vectorize(elder_than)(df['Возраст'], age)
        
        #построение графиков
        draw_graphs(df, f'Cтарше {age}')
        
        #разбиение данных на две выборки
        X1_age = df[df[f'Cтарше {age}'] == 'Да']['Количество больничных дней']
        X2_age = df[df[f'Cтарше {age}'] == 'Нет']['Количество больничных дней']
        #проведение теста по критерию
        statistics_report(X1_age, X2_age, work_days, alpha)
import scipy.stats as stats
import numpy as np
import pandas as pd

#реализуем метод Уэлча
def uelch_statistic_check(X1 : pd.Series, X2 : pd.Series,
                          work_days, alpha : float) -> bool:
    #среднее в двух выборках
    X1_average = np.average(X1)
    X2_average = np.average(X2)
    #несмещенная дисперсия
    s1 = np.var(X1, ddof=1)
    s2 = np.var(X2, ddof=1)
    #размеры выборок
    n1 = len(X1)
    n2 = len(X2)

    #количество степеней свободы
    degrees_of_freedom = (s1/n1+s2/n2)**2/((s1/n1)**2/(n1-1) + (s2/n2)**2/(n2-1))

    #критическое значение для левостроннего теста
    test_statistics_critical = stats.t.ppf(q=alpha, df=degrees_of_freedom)
    
    #значения критерия для нашей выборки
    test_statistics = ((X1_average - X2_average) - work_days)/np.sqrt(s1/n1 + s2/n2)
    
    #из условий формулироваки гипотезы, понимаем что у нас левосторонний критерий
    return test_statistics > test_statistics_critical
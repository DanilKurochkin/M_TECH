import pandas as pd

#функция преобразует считанный с csv файла текст в dataframe
def create_dataframe(lines : list[str]) -> pd.DataFrame:
    #почистим данные от лишних ковычек
    lines = list(map(lambda x: x.rstrip().replace('"', '').rsplit(','), lines))
    columns = lines[0]
    data = lines[1:]
    #создадим DataFrame с данными
    df = pd.DataFrame(data=data, columns=columns)
    #вручную установим типы данных для колонок
    df = df.astype({'Количество больничных дней' : int, 'Возраст' : int, 'Пол' : str})
    
    return df
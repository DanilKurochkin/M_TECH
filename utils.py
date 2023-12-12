import pandas as pd

def create_dataframe(lines : list[str]) -> pd.DataFrame:
    lines = list(map(lambda x: x.rstrip().replace('"', '').rsplit(','), lines))
    columns = lines[0]
    data = lines[1:]
    df = pd.DataFrame(data=data, columns=columns)
    df = df.astype({'Количество больничных дней' : int, 'Возраст' : int, 'Пол' : str})
    
    return df
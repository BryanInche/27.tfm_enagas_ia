import pandas as pd

class DataIngestion:
    def __init__(self):
        pass

    def load_erm_400(self, full_path):
        """Lee el Excel de sensores usando la ruta completa que le pasemos"""
        df = pd.read_excel(full_path, skiprows=5, engine='openpyxl')
        
        df.columns = [
            'datetime', 'presion_in_A', 'presion_in_B', 
            'temperatura_in_A', 'temperatura_in_B', 
            'caudal_bruto_A', 'caudal_bruto_B', 
            'caudal_nominal_A', 'caudal_nominal_B', 
            'caudal_min_diario_A', 'caudal_min_diario_B', 
            'caudal_max_diario_A', 'caudal_max_diario_B'
        ]
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df

    def load_avisos(self, full_path):
        """Lee el Excel de avisos usando la ruta completa que le pasemos"""
        df = pd.read_excel(full_path, sheet_name='Avisos', engine='openpyxl')
        df['Inicio avería'] = pd.to_datetime(df['Inicio avería'])
        return df[df['UT'] == 'ERM_400'].copy() # Se hace un filtro del ERM a analizar
        
import sys
import os
import pandas as pd

# 1. Asegurar que Python vea la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from old.ingestion import DataIngestion

def main():
    # 2. Definir las rutas manualmente (Ruta absoluta a la raíz)
    # Cambia esta ruta si tu carpeta se llama distinto, pero esta es la que sale en tus logs
    base_path = r"C:\Users\braya\Documents\TFM_UCM_Enagas\tfm_enagas"
    
    ruta_sensores = os.path.join(base_path, "data", "raw", "BBDD_ERM_400_CON_A_B_20220101_000000_20230101_000000.xlsx")
    ruta_avisos = os.path.join(base_path, "data", "raw", "Avisos_ERM_Madrid_202210601_20260101_Anonimizado.xlsx")

    print(f"Verificando sensor_file en: {ruta_sensores}")
    
    # Comprobación simple antes de llamar a la función
    if not os.path.exists(ruta_sensores):
        print("ERROR: No encuentro el archivo de sensores. Revisa el nombre o la carpeta.")
        return

    # 3. Llamar a la función con la ruta ya masticada
    ingester = DataIngestion()
    
    print("--- Cargando datos... ---")
    df_sensores = ingester.load_erm_400(ruta_sensores)
    df_avisos = ingester.load_avisos(ruta_avisos)

    print("\n--- ¡LOGRADO!---")
    print(f"Registros: {len(df_sensores)}")
    print(df_sensores[['presion_in_A', 'caudal_nominal_A']].describe())

if __name__ == "__main__":
    main()
import pandas as pd
import glob
import os
import re

path_bbdd = r"C:\Users\braya\Documents\TFM_UCM_Enagas\tfm_enagas\00. Datos aportados por Enagás\BBDD\BBDD"
archivos = glob.glob(os.path.join(path_bbdd, "BBDD*.xlsx"))
print(f"Se han encontrado {len(archivos)} archivos de sensores.")
analisis_final = []

print("--- Iniciando Análisis de Integridad Temporal ---")

for f in archivos:
    nombre = os.path.basename(f)
    match = re.search(r"ERM_(\d+)", nombre)
    erm_id = f"ERM_{match.group(1)}" if match else "Desconocido"

    try:
        # Leemos especificando que la primera col es la fecha
        df_temp = pd.read_excel(f, skiprows=5, engine='openpyxl')
        
        # Identificamos la columna de fecha (usualmente es la primera)
        col_fecha = df_temp.columns[0]
        
        total_filas = len(df_temp)
        # NUEVA LÓGICA: Duplicados basados SOLO en la fecha
        duplicados_fecha = df_temp[col_fecha].duplicated().sum()
        
        # Nulos totales
        nulos_totales = df_temp.isnull().sum().sum()
        
        analisis_final.append({
            'ERM': erm_id,
            'Archivo': nombre,
            'Registros': total_filas,
            'Duplicados_Fecha': duplicados_fecha,
            'Pct_Nulos': round((nulos_totales / (total_filas * df_temp.shape[1])) * 100, 3)
        })
        print(f"OK: {nombre} | Dups Fecha: {duplicados_fecha}")
        
    except Exception as e:
        print(f"Error en {nombre}: {e}")

df_resumen = pd.DataFrame(analisis_final).sort_values(by=['ERM', 'Duplicados_Fecha'], ascending=[True, False])

print("\n" + "="*85)
print("REPORTE DE CALIDAD BASADO EN INTEGRIDAD DE TIEMPO (TIMESTAMP)")
print("="*85)
print(df_resumen.to_string(index=False))
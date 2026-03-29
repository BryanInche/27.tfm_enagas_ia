import pandas as pd
import os
import glob
import re

# 1. Configuración de rutas
path_bbdd = r"C:\Users\braya\Documents\TFM_UCM_Enagas\tfm_enagas\00. Datos aportados por Enagás\BBDD\BBDD"
ruta_avisos = r"C:\Users\braya\Documents\TFM_UCM_Enagas\tfm_enagas\00. Datos aportados por Enagás\BBDD\BBDD\Avisos_ERM_Madrid_202210601_20260101_Anonimizado.xlsx"

# 2. Carga y limpieza de Avisos SAP
df_sap = pd.read_excel(ruta_avisos, sheet_name='Avisos')
# Usamos 'Inicio deseado' por ser el más completo
df_sap['fecha_evento'] = pd.to_datetime(df_sap['Inicio deseado'])

# 3. Listar archivos de sensores
archivos = glob.glob(os.path.join(path_bbdd, "BBDD*.xlsx"))
print(f"Se han encontrado {len(archivos)} archivos de sensores.")
analisis_realismo = []

print("--- Cruzando Sensores con Avisos SAP ---")

for f in archivos:
    nombre = os.path.basename(f)
    match = re.search(r"ERM_(\d+)", nombre)
    erm_id = f"ERM_{match.group(1)}" if match else "Desconocido"
    
    try:
        # Leemos solo la primera columna para obtener el rango de fechas rápido
        df_temp = pd.read_excel(f, skiprows=5, usecols=[0], engine='openpyxl')
        fecha_min = df_temp.iloc[:, 0].min()
        fecha_max = df_temp.iloc[:, 0].max()
        
        # Filtrar avisos que pertenezcan a esta ERM y estén en este rango de fechas
        avisos_en_rango = df_sap[
            (df_sap['UT'] == erm_id) & 
            (df_sap['fecha_evento'] >= fecha_min) & 
            (df_sap['fecha_evento'] <= fecha_max)
        ]
        
        num_avisos = len(avisos_en_rango)
        # Extraer tipos de fallo (ej. Regulación, Mecánico) para la justificación
        tipos_fallo = ", ".join(avisos_en_rango['Denominación'].unique().tolist()) if num_avisos > 0 else "N/A"

        analisis_realismo.append({
            'ERM': erm_id,
            'Archivo': nombre,
            'Inicio_Datos': fecha_min.date(),
            'Fin_Datos': fecha_max.date(),
            'Cant_Avisos_SAP': num_avisos,
            'Tipos_de_Fallo': tipos_fallo
        })
        print(f"Procesado: {erm_id} | Avisos encontrados: {num_avisos}")
        
    except Exception as e:
        print(f"Error procesando {nombre}: {e}")

# 4. Mostrar resultados finales
df_realismo = pd.DataFrame(analisis_realismo).sort_values(by='Cant_Avisos_SAP', ascending=False)
print("\n" + "="*95)
print("ANÁLISIS DE REALISMO: ARCHIVOS CON FALLOS DOCUMENTADOS")
print("="*95)
print(df_realismo[['ERM', 'Cant_Avisos_SAP', 'Tipos_de_Fallo', 'Inicio_Datos']].to_string(index=False))
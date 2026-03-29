import pandas as pd
import glob
import os
import re

path_bbdd = r"C:\Users\braya\Documents\TFM_UCM_Enagas\tfm_enagas\00. Datos aportados por Enagás\BBDD\BBDD"
archivos = glob.glob(os.path.join(path_bbdd, "BBDD*.xlsx"))
analisis_lineas = []

print("--- Iniciando Análisis de Disponibilidad Real por Periodo ---")

for f in archivos:
    nombre = os.path.basename(f)
    
    # 1. Extraer el ID de la ERM
    match_erm = re.search(r"ERM_(\d+)", nombre)
    erm_id = f"ERM_{match_erm.group(1)}" if match_erm else "Desconocido"
    
    # 2. Extraer el Periodo (buscamos las fechas tipo 20210601_000000)
    # Buscamos los grupos de 8 dígitos que suelen ser las fechas YYYYMMDD
    fechas = re.findall(r"(\d{8})", nombre)
    periodo = f"{fechas[0]}-{fechas[1]}" if len(fechas) >= 2 else "Sin Fecha"

    try:
        df_temp = pd.read_excel(f, skiprows=5, engine='openpyxl')
        total_filas = len(df_temp)
        
        for col in df_temp.columns:
            if 'fecha' in col.lower() or 'time' in col.lower() or 'unnamed' in col.lower():
                continue
                
            nulos = df_temp[col].isnull().sum()
            ceros = 0
            if pd.api.types.is_numeric_dtype(df_temp[col]):
                ceros = (df_temp[col] == 0).sum()
            
            pct_nulos = (nulos / total_filas) * 100
            pct_ceros = (ceros / total_filas) * 100
            disponibilidad_real = 100 - (pct_nulos + pct_ceros)

            analisis_lineas.append({
                'ERM': erm_id,
                'Periodo': periodo,  # <--- Nueva columna
                'Variable': col,
                'Pct_Nulos': round(pct_nulos, 2),
                'Pct_Ceros': round(pct_ceros, 2),
                'Disp_Real_%': round(disponibilidad_real, 2)
            })
            
    except Exception as e:
        print(f"Error en {nombre}: {e}")

df_resumen = pd.DataFrame(analisis_lineas)

# Ordenamos por ERM, luego por Periodo y finalmente por la mejor disponibilidad
df_resumen = df_resumen.sort_values(by=['ERM', 'Periodo', 'Disp_Real_%'], ascending=[True, True, False])

print("\n" + "="*110)
print(f"{'ERM':<10} | {'Periodo':<20} | {'Variable':<25} | {'Nulos%':<8} | {'Ceros%':<8} | {'Disp_Real%'}")
print("="*110)

# Mostramos el resultado (puedes ajustar el head si quieres ver más filas)
print(df_resumen.to_string(index=False))

# Opcional: Guardar este reporte a Excel para analizarlo con calma
# df_resumen.to_excel("reporte_disponibilidad_tfm.xlsx", index=False)
import pandas as pd
import os
from pathlib import Path
import re

def NormalizarObjetivo(description):
       if re.search('BRAND', description.upper()):
              return 'Brand'
       elif re.search('PERFORM', description.upper()):
              return 'Performance'
       elif re.search('FUNNE', description.upper()):
              return 'Mid Funnel'
       else:
              return 'SIN_OBJETIVO'

def NormalizarDisciplina(description):
       if re.search('SOC', description.upper()):
              return 'Social Media'
       elif re.search('VIDEO', description.upper()):
              return 'Video Online'
       elif re.search('AUD', description.upper()):
              return 'Audio'
       elif re.search('DISPLAY', description.upper()):
              return 'Display'
       else:
              return description

def NormalizarTipoCoste(description):
    if re.search('FIJO', description.upper()):
        return 'CF'
    else:
        return description

def create_monthly_df(path,file):   
    xl = pd.ExcelFile(path+file)
    sheet = [e for e in xl.sheet_names if re.search('diario',e.lower())][0]
    df = pd.read_excel(path+file, sheet_name=sheet)
    cols =['Cliente ', 'Campaña', 'Objetivo ', 'Sub-Objetivo', 'Objetivo Final', 
           'disciplina', 'soporte', 'tipo_coste', 'pagador', 'producto', 'subproducto', 
           'fecha_dia','impresiones', 'clicks', 'inversion', 'measurable_impressions', 
           'viewable_impressions', 'views', 'video_25', 'video_50', 'video_75', 'video_completions']
    df2 = df[cols].fillna(0)
    df2.rename(columns={'Cliente ':'cliente',
    'Campaña':'campanya',
    'Objetivo ':'objetivo_0',
    'Sub-Objetivo':'subojetivo',
    'Objetivo Final':'objetivo_final',
    'disciplina':'disciplina_0',
    'tipo_coste':'tipo_coste_0',
    'clicks':'clics',
    'measurable_impressions':'impresiones_medibles',
    'viewable_impressions':'impresiones_visibles',
    'video_25':'views_25',
    'video_50':'views_50',
    'video_75':'views_75',
    'video_completions':'views_100'},inplace=True
    )
    df2['objetivo'] = df2.objetivo_0.apply(lambda x: NormalizarObjetivo(x))
    df2['disciplina'] = df2.disciplina_0.apply(lambda x: NormalizarDisciplina(x)) 
    df2['tipo_coste'] = df2.tipo_coste_0.apply(lambda x: NormalizarTipoCoste(x))
    df2['fecha_dia'] = pd.to_datetime(df2['fecha_dia'], format='%Y-%m-%d')
    df2['dia_semana']=df2.fecha_dia.dt.weekday
    df2['timedelta']=df2.dia_semana.apply(lambda x: pd.Timedelta(days=x))
    df2['fecha_semana']=df2.fecha_dia - df2.timedelta
    df2.drop(columns = ['dia_semana','timedelta'], inplace=True)
    df2['mes'] = df2.fecha_dia.apply(lambda x: x.month)
    df2['file'] = file
    df2 = df2.astype({
       'impresiones':'float64',
       'clics':'float64',
       'inversion':'float64',
       'impresiones_medibles':'float64',
       'impresiones_visibles':'float64',
       'views':'float64',
       'views_25':'float64',
       'views_50':'float64',
       'views_75':'float64',
       'views_100':'float64',
    })
    final = df2[['mes','fecha_semana', 'fecha_dia','cliente', 'campanya', 'objetivo', 'subojetivo', 'objetivo_final',
           'disciplina', 'soporte', 'tipo_coste', 'pagador', 'producto',
           'subproducto', 'impresiones', 'clics', 'inversion',
           'impresiones_medibles', 'impresiones_visibles', 'views', 'views_25',
           'views_50', 'views_75', 'views_100', 'file']]
    return final

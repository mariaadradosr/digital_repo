import pandas as pd
import os
from pathlib import Path
import re

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
    'Objetivo ':'objetivo',
    'Sub-Objetivo':'subojetivo',
    'Objetivo Final':'objetivo_final',
    'clicks':'clics',
    'measurable_impressions':'impresiones_medibles',
    'viewable_impressions':'impresiones_visibles',
    'video_25':'views_25',
    'video_50':'views_50',
    'video_75':'views_75',
    'video_completions':'video_100'},inplace=True
    )
    df2['fecha_dia'] = pd.to_datetime(df2['fecha_dia'], format='%Y-%m-%d')
    df2['dia_semana']=df2.fecha_dia.dt.weekday
    df2['timedelta']=df2.dia_semana.apply(lambda x: pd.Timedelta(days=x))
    df2['fecha_semana']=df2.fecha_dia - df2.timedelta
    df2.drop(columns = ['dia_semana','timedelta'], inplace=True)
    df2['mes'] = df2.fecha_dia.apply(lambda x: x.month)
    df2['file'] = file
    df2 = df2[['mes','fecha_semana', 'fecha_dia','cliente', 'campanya', 'objetivo', 'subojetivo', 'objetivo_final',
           'disciplina', 'soporte', 'tipo_coste', 'pagador', 'producto',
           'subproducto', 'impresiones', 'clics', 'inversion',
           'impresiones_medibles', 'impresiones_visibles', 'views', 'views_25',
           'views_50', 'views_75', 'video_100', 'file']]
    return df2

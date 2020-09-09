import pandas as pd
import os
from pathlib import Path
import re
import functions

input_path = './input/'
output_path = './output/'

def main():
    base = pd.read_csv('./output/base.csv',sep=';')
    saved_files = [e.name for e in sorted(Path(input_path).iterdir(), key=os.path.getmtime,reverse=True)]
    print('\nSAVED_FILES....',saved_files)
    base_files = list(base.file.unique())
    print('\nBASE_FILES....',base_files,'\n')
    to_add = [f for f in saved_files if f not in base_files]
    print('\nFiles to add .....',to_add,'\n')
    #Comprobar si los archivos de base están en los guardados
    for file in base_files:
        if file not in saved_files:
            print('removing....',file)
            base = base.drop(base[base['file'] == file].index).reset_index()
    #Añadir archivos a base
    count = 0
    for file in saved_files:
        if file not in base_files:
            to_add = functions.create_monthly_df(path = input_path, file = file)
            base = pd.concat([base,to_add])
            print(file,'.......ADDED to base')
            count += 1
    if count == 0:
        print('\nTHERE IS NO FILE TO ADD TO BASE\n')
    else:
        mensual = base.groupby(by=['mes','cliente', 'campanya', 'objetivo','subojetivo', 'objetivo_final',
        'disciplina', 'soporte', 'tipo_coste', 'pagador', 'producto', 'subproducto']).sum()
        mensual.reset_index(inplace=True)
        mensual.to_csv('./output/mensual.csv',sep=';',encoding='CP1252',index=False)
        print('\nMENSUAL ...... UPDATED\n')

        semanal = base.groupby(by=['mes','fecha_semana','cliente', 'campanya', 'objetivo','subojetivo', 'objetivo_final',
        'disciplina', 'soporte', 'tipo_coste', 'pagador', 'producto', 'subproducto']).sum()
        semanal.reset_index(inplace=True)
        semanal.to_csv('./output/semanal.csv',sep=';',encoding='CP1252',index=False)
        print('\nSEMANAL ...... UPDATED\n')

    base.to_csv('./output/base.csv',sep=';',encoding='CP1252',index=False)
    print('\nBASE ...... UPDATED\n')

if __name__ == "__main__":
    main()
#!pip install openpyxl

import pandas
import openpyxl

def atualizar_origem(sheet1, sheet2):
    # Adicionando coluna de identificação de origem inicialmente com 'Verificacao Manual'
    sheet2['Origem'] = 'Verificacao Manual'

    # Realizando a checagem e atualizando a coluna 'Origem' com base na condição
    condicao = sheet2['Tabela'].isin(sheet1['table_nm'])
    condicao2 = sheet2['Nome'].isin(sheet1['column_name'])

    sheet2 = sheet2.loc[condicao]
    sheet2.loc[condicao2, 'Origem'] = 'MACIE'

    return sheet2

#path da planilha excel
excel_file_path = '/home/dpoli/Brasilcap-masking.xlsx'
excel_sheets=pd.ExcelFile(excel_file_path)

#leitura da aba 'Findings Macie'
sheet1 = excel_sheets.parse(sheet_name='Findings Macie')

#path da planilha a ser gerada
output_excel='/home/dpoli/planilha_atualizada.xlsx'

#Gerando a nova planilha com cada aba atualizada
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    sheet1.to_excel(writer, index=False, sheet_name='Sheet1')
    for sheet_name in excel_sheets.sheet_names:
        if sheet_name!='Findings Macie':
                
            sheet2 = excel_sheets.parse(sheet_name=sheet_name)

            sheet2_atualizado = atualizar_origem(sheet1, sheet2)
            sheet2_atualizado.to_excel(writer, index=False, sheet_name=sheet_name)

excel_sheets.close()
    
    

    



    




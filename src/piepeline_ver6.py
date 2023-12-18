import pandas as pd 
import pymysql
import boto3
import pyarrow
from datetime import datetime

#conectar ao mysql
connection=pymysql.connect(
    host='',
    user='',
    password='',
    db='',
)

#conectar aws
s3=boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
)

#criando dataframes
df_lista=[]
df=pd.DataFrame()

#query mysql
query='SELECT * FROM tabela'

#escolher o  volume de linhas em cada interação
chunksize=500000  

for i, chunk in enumerate (pd.read_sql(query, conn, chunksize=chunksize)):
    df_lista.append(chunk)
    del chunk
print('tudo foi importado')

df=pd.concat(df_lista,ignore_index=True)
df=df.fillna('')
df=df.astype(str)
print('df concatenado')

connection.close()
print('closed connection')

#----------aqui entraria o tratamento, caso necessario------------

#converte para parquet
df.to_parquet('parquet_file.parquet')
print('Dataframe convertido para Parquet com sucesso.')

colunas = df.columns.tolist()
print(colunas)




#uploado bucket
current_date=datetime.now().strftime('%Y%m%d')

bucket='nome do bucket'
key=f'nome do arquivo no bucket_{current_date}.parquet'

s3.upload_file(file_name='parquet_file.parquet',
               bucket=bucket,
               key=key)






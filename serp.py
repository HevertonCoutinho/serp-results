from googlesearch import search
import csv
import pandas as pd
import re
from datetime import datetime
print('================================================')
print('GOOGLE SEARCH')
print('================================================')
# Get user search keyword.
searchKeyWord = input('Digite a sua pesquisa Google: ')
# Get Total number of records.
totalNoOfRecords = input('Quantos resultados de busca você deseja salvar em seu arquivo CSV? ')
print('Por favor aguarde. Sua requisição está sendo processada. \n')
resultLinks = []
# Search the keyword in google.
results = search(searchKeyWord, num_results=int(totalNoOfRecords))
#results = '\n'.join([str(elem) for elem in results])
# Convert result into data frame.
df = pd.DataFrame(results)
now = datetime.now()
outputFileName = 'SearchOutput' + now.strftime("%d-%m-%Y") + '.csv'
# Write output in CSV format.
df.to_csv(outputFileName,mode='a', encoding='utf-8', index=False , header=False)
print('================================================\n')
print('Pesquisa concluida com sucesso!!. Por favor, cheque o arquivo output criado em sua pasta!!\n')
print(outputFileName + '\n')
print('================================================\n')

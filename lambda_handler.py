import uuid
import csv
import boto3
import time


def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    print("Iniciando Lambda function...")
    
    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(bucket_name, file_name)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dynamodb_hexagon')
    
    
    data = s3_object.get()['Body'].read().decode('ISO-8859-15')

    data = str(data).split('\n')
    lines = csv.reader(data, delimiter=';')
    csv_headings = next(lines)
   
    
    with table.batch_writer() as batch:
        for record in lines:
            if len(record):
                batch.put_item(set_Item(record))
            
            
    return "from Lambda!"
    
    
def set_Item(r):
    id = str(uuid.uuid1())
    print(id)
    item = {
                'id': id,
                'Ano_e_mes_do_lancamento' : r[0],
                'Codigo_Orgao_Superior' : r[1],
                'Nome_Orgao_Superior' : r[2],
                'Codigo_Orgao_Subordinado' : r[3],
                'Nome_Orgao_Subordinado' : r[4],
                'Codigo_Unidade_Gestora' : r[5],
                'Nome_Unidade_Gestora' : r[6],
                'Codigo_Gestao' : r[7],
                'Nome_Gestao' : r[8],
                'Codigo_Unidade_Orcamentaria' : r[9],
                'Nome_Unidade_Orcamentaria' : r[10],
                'Codigo_Funcao' : r[11],
                'Nome_Funcao' : r[12],
                'Codigo_Subfucao' : r[13],
                'Nome_Subfuncao' : r[14],
                'Codigo_Programa_Orcamentario' : r[15],
                'Nome_Programa_Orcamentario' : r[16],
                'Codigo_Acao' : r[17],
                'Nome_Acao' : r[18],
                'Codigo_Plano_Orcamentario' : r[19],
                'Plano_Orcamentario' : r[20],
                'Codigo_Programa_Governo' : r[21],
                'Nome_Programa_Governo' : r[22],
                'UF' : r[23],
                'Municipio' : r[24],
                'Codigo_Subtitulo' : r[25],
                'Nome_Subtitulo' : r[26],
                'Codigo_Localizador' : r[27],
                'Nome_Localizador' : r[28],
                'Sigla_Localizador' : r[29],
                'Descricao_Complementar_Localizador' : r[30],
                'Codigo_Autor_Emenda' : r[31],
                'Nome_Autor_Emenda' : r[32],
                'Codigo_Categoria_Economica' : r[33],
                'Nome_Categoria_Economica' : r[34],
                'Codigo_Grupo_de_Despesa' : r[35],
                'Nome_Grupo_de_Despesa' : r[36],
                'Codigo_Elemento_de_Despesa' : r[37],
                'Nome_Elemento_de_Despesa' : r[38],
                'Codigo_Modalidade_da_Despesa' : r[39],
                'Modalidade_da_Despesa': r[40],
                'Valor_Empenhado': r[41],
                'Valor_Liquidado': r[42],
                'Valor_Pago': r[43],
                'Valor_Restos_Pagar_Inscritos': r[44],
                'Valor_Restos_Pagar_Cancelado': r[45],
                'Valor_Restos_Pagar_Pagos': r[46]
            }
    return item

#LocalStack: Deploy Lambda function | LocalStack: Invoke Lambda functioN
import json
import boto3
import os
import logging
from decimal import Decimal

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    # Configurar o DynamoDB para LocalStack
    dynamodb = boto3.resource(
        'dynamodb', 
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    
    # Conectar à tabela DynamoDB
    table = dynamodb.Table('NotasFiscais')

    # Verificar se é uma consulta (GET) 
    if event.get("httpMethod") == "GET": 
        return consultar_registros(event, table)
    # Inserção de registros (POST) 
    if event.get("httpMethod") == "POST": 
        return inserir_registros(event, table)
    
    return {
        'statusCode': 400,
        'body': json.dumps('Erro: Método HTTP não suportado.')
    }

def consultar_registros(event, table):
    try:
        response = table.scan()
        logger.info(f'Consulta realizada com sucesso. Total de registros: {response["Count"]}')
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], default=str)
        }
    except Exception as e:
        logger.error(f"Erro na consulta: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro na consulta.')
        }

def inserir_registros(event, table):
    try:
        # O body vem do API Gateway
        body = json.loads(event['body']) 
        logger.info(f"Processando inserção de registro: {body}")
        
        # Validação básica do registro
        if not all(key in body for key in ["id", "cliente", "valor", "data_emissao"]): 
            return {
                'statusCode': 400, 
                'body': json.dumps('Erro: Campos obrigatórios faltando.')
            }

        # Inserir o registro no DynamoDB 
        body['valor'] = Decimal(str(body['valor'])) 
        table.put_item(Item=body) 
        
        return {
            'statusCode': 200,
            'body': json.dumps('Registro inserido com sucesso!')
        } 
    except Exception as e:
        logger.error(f"Erro ao inserir registro no DynamoDB: {str(e)}") 
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao inserir registro.')
        }

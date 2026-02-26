import json
import boto3
import uuid

# Inicializa o recurso fora do handler para melhor performance
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')

def lambda_handler(event, context):
    # 1. Definimos os cabeçalhos de CORS que serão usados em TODAS as respostas
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # 2. Respondemos IMEDIATAMENTE ao navegador se for um 'Preflight' (OPTIONS)
    # Isso resolve o erro vermelho do console
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS OK')
        }

    try:
        # 3. Pegamos o corpo da requisição com segurança
        body_str = event.get('body', '{}')
        body = json.loads(body_str)
        email_usuario = body.get('email')

        if not email_usuario:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('Email nao fornecido no JSON')
            }

        # 4. Gravação no DynamoDB
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'Emails': email_usuario
            }
        )

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('E-mail cadastrado com sucesso!')
        }

    except Exception as e:
        # Se der erro no banco, retornamos o erro com os Headers de CORS
        # para que o navegador exiba o erro real em vez de travar no CORS
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Erro interno: {str(e)}')
        }
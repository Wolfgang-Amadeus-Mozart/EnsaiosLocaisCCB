import os
import pandas as pd
import boto3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


REGION = "us-east-1" 
TABLE_NAME = "EmailsEnsaiosLocaisGuarulhos"

def buscar_emails_dynamo():
    """Busca todos os e-mails cadastrados na tabela do DynamoDB."""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    # Retorna uma lista apenas com os endereços de e-mail
    return [item['Emails'] for item in response.get('Items', [])]

def enviar_email(destinatarios, mensagem_corpo):
    """Envia o e-mail via SMTP do Gmail usando Segredos do GitHub."""
    remetente = os.environ.get('EMAIL_USER')
    senha = os.environ.get('EMAIL_PASS')
    
    if not remetente or not senha:
        print("Erro: Credenciais de e-mail não configuradas.")
        return

    msg = MIMEText(mensagem_corpo)
    msg['Subject'] = f"Aviso de Ensaio - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = remetente
    msg['To'] = ", ".join(destinatarios)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatarios, msg.as_string())
        print(f"E-mail enviado com sucesso para {len(destinatarios)} pessoas!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def job():
    # 1. Verifica se há evento hoje no seu CSV
    hoje = datetime.now().strftime('%Y-%m-%d')
    df = pd.read_csv('calendario.csv') # Seu CSV do Colab
    
    # Filtra eventos para o dia de hoje
    eventos_hoje = df[df['data'] == hoje]

    if not eventos_hoje.empty:
        evento_nome = eventos_hoje.iloc[0]['evento'] # Ajuste conforme suas colunas
        corpo = f"Olá! Passando para avisar que hoje temos: {evento_nome}."
        
        # 2. Busca a lista de inscritos no DynamoDB
        lista_emails = buscar_emails_dynamo()
        
        if lista_emails:
            # 3. Dispara o e-mail
            enviar_email(lista_emails, corpo)
        else:
            print("Nenhum e-mail cadastrado no banco.")
    else:
        print(f"Nenhum evento agendado para hoje ({hoje}).")

if __name__ == "__main__":
    job()
import os
import pandas as pd
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def enviar_email(destinatarios, mensagem_html):
    remetente = os.environ.get('EMAIL_USER')
    senha = os.environ.get('EMAIL_PASS')
    
    if not remetente or not senha:
        print("Erro: Credenciais de e-mail não configuradas.")
        return

    # Mudança aqui: usamos MIMEMultipart para o Gmail entender que é um e-mail rico
    msg = MIMEMultipart()
    msg['Subject'] = f"🔔 Aviso de Ensaio - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = f"Ensaios Guarulhos <{remetente}>"
    msg['To'] = ", ".join(destinatarios)

    # Anexamos o corpo como HTML
    msg.attach(MIMEText(mensagem_html, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            # enviamos o msg.as_string() que contém o HTML formatado
            server.sendmail(remetente, destinatarios, msg.as_string())
        print(f"E-mail enviado com sucesso para {len(destinatarios)} pessoas!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def job():
    hoje = datetime.now().strftime('%Y-%m-%d')
    df = pd.read_csv('calendario.csv') 
    df['data'] = df['data'].astype(str).str.strip()
    
    eventos_hoje = df[df['data'] == hoje]

    if not eventos_hoje.empty:
        evento = eventos_hoje.iloc[0]
        local = evento['Localidade']
        hora = evento['Horário']
        waze = evento['Waze']

        # Montando o corpo HTML aqui no job
        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #f9f9f9;">
            <h2 style="color: #007bff; text-align: center;">📢 Lembrete de Ensaio</h2>
            <p>Olá! Passando para avisar que <b>hoje</b> temos ensaio agendado:</p>
            
            <div style="background-color: #fff; padding: 15px; border-radius: 8px; border-left: 5px solid #007bff; margin: 20px 0;">
                <p style="margin: 5px 0;"><b>📍 Localidade:</b> {local}</p>
                <p style="margin: 5px 0;"><b>⏰ Horário:</b> {hora}</p>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <a href="{waze}" style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                🗺️ Abrir no Waze
                </a>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 12px; color: #777; text-align: center;">
                Este é um aviso automático do sistema Ensaios Guarulhos, desenvolvido por Filipe Queiroz de Abreu, do parque santos dumont.<br>
                Deus abençoe!
            </p>
            </div>
        </body>
        </html>
    """
        
        lista_emails = buscar_emails_dynamo()
        
        if lista_emails:
            enviar_email(lista_emails, corpo_html)

if __name__ == "__main__":
    job()
import unittest
from infraestrutura.lambda_dynamo.listacontatos import buscar_emails_dynamo, buscar_telefones_dynamo, lambda_handler

class TestListaContatos(unittest.TestCase):
    def test_buscar_emails_dynamo(self):
        # Teste mock para DynamoDB
        pass

    def test_buscar_telefones_dynamo(self):
        # Teste mock para telefones
        pass

    def test_lambda_handler(self):
        # Testar lambda_handler simulando entrada
        pass

if __name__ == "__main__":
    unittest.main()
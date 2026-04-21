import unittest
from infraestrutura.lambda.index import monta_html_email, enviar_email, lambda_handler

class TestIndex(unittest.TestCase):
    def test_monta_html_email(self):
        result = monta_html_email("email", "test@example.com")
        self.assertIn("<html>", result)

    def test_enviar_email(self):
        # Testar chamada simulada (mock) para enviar_email
        pass

    def test_lambda_handler(self):
        # Testar chamadas para lambda_handler com mocks
        pass

if __name__ == "__main__":
    unittest.main()
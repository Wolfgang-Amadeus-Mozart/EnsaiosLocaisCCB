resource "aws_dynamodb_table" "EmailsEnsaiosLocaisGuarulhos" {
  name         = "EmailsEnsaiosLocaisGuarulhos"
  billing_mode = "PAY_PER_REQUEST" 
  hash_key     = "id"

  # Você precisa definir o "id" aqui porque ele é o hash_key
  attribute {
    name = "id"
    type = "S"
  }

  # Você precisa definir o "Emails" aqui porque ele é usado no GSI
  attribute {
    name = "Emails"
    type = "S"
  }

  global_secondary_index {
    name               = "EmailsIndex"
    hash_key           = "Emails"
    projection_type    = "ALL" # Mais simples para começar
  }

  tags = {
    Name        = "dynamodb-table-EmailsEnsaiosLocaisGuarulhos"
    Environment = "production"
    Owner       = "Filipe"
  }
}
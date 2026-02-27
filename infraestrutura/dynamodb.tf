resource "aws_dynamodb_table" "EmailsEnsaiosLocaisGuarulhos" {
  name         = "EmailsEnsaiosLocaisGuarulhos"
  billing_mode = "PAY_PER_REQUEST" 
  hash_key     = "id" #Hash Key = Partition Key, Causa um pouco de confusao mas é a mesma coisa

  attribute {
    name = "id"
    type = "S"
  }

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
resource "aws_dynamodb_table" "bpham-dynamodb-table" {
  name           = "bpham-dev-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "serial_num"

  attribute {
    name = "serial_num"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  tags = {
    Name        = "bpham-dev-table"
    Environment = "staging"
  }
}
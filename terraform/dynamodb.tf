resource "aws_dynamodb_table" "bandon_weather_data" {
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "Date"
  name             = "bandon-weather-data"

  attribute {
    name = "Date"
    type = "S"
  }
}
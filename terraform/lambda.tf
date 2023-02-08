data "archive_file" "email_automation_func" {
  type        = "zip"
  source_file = "./lambda/weather_email.py"
  output_path = "./lambda/lambda.zip"
}

data "archive_file" "email_automation_layer" {
  type        = "zip"
  source_file = "./lambda/requirements.zip"
  output_path = "./lambda/requirements.zip"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "./lambda/requirements.zip"
  layer_name = "weather-email-automation-layer"
  source_code_hash = data.archive_file.email_automation_layer.output_base64sha256
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "email_automation" {
    environment {
      variables = {
        CLIENT_ID = "${var.CLIENT_ID}",
        CLIENT_SECRET = "${var.CLIENT_SECRET}",
        EMAIL_LIST = "${var.EMAIL_LIST}",
        REFRESH_TOKEN = "${var.REFRESH_TOKEN}",
        WEATHER_API_KEY = "${var.WEATHER_API_KEY}",
      }
    }
    function_name = "weather-email-automation"
    filename = "./lambda/lambda.zip"
    handler = "weather_email.lambda_handler"
    layers = [ aws_lambda_layer_version.email_automation_layer.arn ]
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = data.archive_file.email_automation_func.output_base64sha256
    timeout = "5"

    tags = {
      "Name" = "Bandon"
    }

}
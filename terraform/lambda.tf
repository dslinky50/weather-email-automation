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
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = filebase64sha256("./lambda/lambda.zip")
    timeout = "5"

    tags = {
      "Name" = "Bandon"
    }

}
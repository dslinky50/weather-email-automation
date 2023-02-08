resource "aws_lambda_function" "email_automation" {
    function_name = "weather-email-automation"
    filename = "./lambda/lambda.zip"
    handler = "weather_email.lambda_handler"
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    timeout = "5"

    tags = {
      "Name" = "Bandon"
    }
    
}
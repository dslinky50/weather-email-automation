resource "aws_lambda_function" "email_automation" {
    
    environment {
      variables = {
        EMAIL_LIST = "${var.EMAIL_LIST}",
        WEATHER_API_KEY = "${var.WEATHER_API_KEY}",
      }
    }
    function_name = "email-weather-automation"
    filename = "./lambda/email_lambda.zip"
    handler = "email_weather.lambda_handler"
    # layers = [aws_lambda_layer_version.email_automation_layer.arn]
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = filebase64sha256("./lambda/email_lambda.zip")
    timeout = "10"

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_lambda_permission" "email_event_bridge" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.email_automation.function_name
    principal = "events.amazonaws.com"
}
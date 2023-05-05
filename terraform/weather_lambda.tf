resource "aws_lambda_function" "weather_automation" {
    
    environment {
      variables = {
        WEATHER_API_KEY = "${var.WEATHER_API_KEY}",
      }
    }
    function_name = "weather-dynamo-automation"
    filename = "./lambda/weather_lambda.zip"
    handler = "weather_lambda.lambda_handler"
    # layers = [aws_lambda_layer_version.email_automation_layer.arn]
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = filebase64sha256("./lambda/weather_lambda.zip")
    timeout = "10"

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_lambda_permission" "weather_event_bridge" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.weather_automation.function_name
    principal = "events.amazonaws.com"
}
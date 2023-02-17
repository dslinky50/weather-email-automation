resource "aws_lambda_function" "sheets_automation" {
    
    function_name = "sheets-weather-automation"
    filename = "./lambda/sheets_lambda.zip"
    handler = "sheets_weather.lambda_handler"
    role = aws_iam_role.email_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = filebase64sha256("./lambda/sheets_lambda.zip")
    timeout = "10"

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_lambda_permission" "sheets_lambda_invoke" {
    statement_id = "AllowExecutionFromEmailLambda"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.sheets_automation.function_name
    principal = "lambda.amazonaws.com"
}
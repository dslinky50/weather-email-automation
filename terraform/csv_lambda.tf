resource "aws_lambda_function" "csv_automation" {
    function_name = "dynamo-csv-s3-automation"
    filename = "./lambda/dynamo_s3.zip"
    handler = "dynamo_s3.lambda_handler"
    # layers = [aws_lambda_layer_version.email_automation_layer.arn]
    role = aws_iam_role.csv_automation_lambda_role.arn
    runtime = "python3.9"
    source_code_hash = filebase64sha256("./lambda/dynamo_s3.zip")
    timeout = "10"

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_lambda_permission" "csv_event_bridge" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.csv_automation.function_name
    principal = "events.amazonaws.com"
}
resource "aws_cloudwatch_event_rule" "weather_dynamo_schedule" {
    name = "weather-dynamo-schedule"
    description = "Schedule for Lambda Function"
    schedule_expression = "cron(5 7 * * ? *)"

    tags = {
      "Name" = "Bandon"
    }
}

resource "aws_cloudwatch_event_target" "weather_dynamo_target" {
    rule = aws_cloudwatch_event_rule.weather_dynamo_schedule.name
    target_id = "weather_dynamo_lambda"
    arn = aws_lambda_function.weather_automation.arn
}
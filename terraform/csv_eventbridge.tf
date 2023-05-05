resource "aws_cloudwatch_event_rule" "weather_csv_schedule" {
    name = "weather-csv-schedule"
    description = "Schedule for Lambda Function"
    schedule_expression = "cron(10 4 * * ? *)"

    tags = {
      "Name" = "Bandon"
    }
}

resource "aws_cloudwatch_event_target" "weather_csv_target" {
    rule = aws_cloudwatch_event_rule.weather_csv_schedule.name
    target_id = "weather_csv_lambda"
    arn = aws_lambda_function.csv_automation.arn
}
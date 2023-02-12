resource "aws_cloudwatch_event_rule" "email_automation_schedule" {
    name = "email-automation-schedule"
    description = "Schedule for Lambda Function"
    schedule_expression = "cron(30 1 ? * 1 *)"

    tags = {
      "Name" = "Bandon"
    }
}

resource "aws_cloudwatch_event_target" "email_automation_target" {
    rule = aws_cloudwatch_event_rule.email_automation_schedule.name
    target_id = "email_automation_lambda"
    arn = aws_lambda_function.email_automation.arn
}
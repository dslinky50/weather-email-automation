resource "aws_iam_role" "weather_automation_lambda_role" {
    name = "weather-automation-lambda-role"

    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

    tags = {
    "Name" = "Bandon"
    }

}

resource "aws_iam_role_policy" "weather_automation" {
    name = "weather-lambda-dynamo-policy"
    role = aws_iam_role.weather_automation_lambda_role.id

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
    })

}

resource "aws_iam_role_policy_attachment" "weather_cloudwatch_attach" {
  role       = aws_iam_role.weather_automation_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
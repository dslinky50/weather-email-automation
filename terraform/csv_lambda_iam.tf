resource "aws_iam_role" "csv_automation_lambda_role" {
    name = "csv-automation-lambda-role"

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

resource "aws_iam_role_policy" "csv_automation" {
    name = "csv-lambda-dynamo-s3-policy"
    role = aws_iam_role.csv_automation_lambda_role.id

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:Scan",
          "s3:*",
          "s3-object-lambda:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
    })

}

resource "aws_iam_role_policy_attachment" "csv_cloudwatch_attach" {
  role       = aws_iam_role.csv_automation_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
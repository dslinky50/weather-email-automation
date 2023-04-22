resource "aws_iam_role" "email_automation_lambda_role" {
    name = "email-automation-lambda-role"

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

resource "aws_iam_role_policy" "email_automation" {
    name = "email-lambda-s3-ses-policy"
    role = aws_iam_role.email_automation_lambda_role.id

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:*",
          "s3-object-lambda:*",
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
    })

}

resource "aws_iam_role_policy_attachment" "email_cloudwatch_attach" {
  role       = aws_iam_role.email_automation_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
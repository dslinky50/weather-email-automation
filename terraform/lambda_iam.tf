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
    name = "email-lambda-s3-policy"
    role = aws_iam_role.email_automation_lambda_role.id

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:*",
          "s3-object-lambda:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
    })

}

resource "aws_iam_role_policy" "email_sheets_automation" {
    name = "email-lambda-sheets-policy"
    role = aws_iam_role.email_automation_lambda_role.id

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction"
        ]
        Effect   = "Allow"
        Resource = "${aws_lambda_function.sheets_automation.arn}"
      },
    ]
    })

}

resource "aws_iam_role" "sheets_automation_lambda_role" {
    name = "sheets-automation-lambda-role"

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
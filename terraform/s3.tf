resource "aws_s3_bucket" "email_automation" {
    bucket = "weather-email-automation"

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_s3_object" "email_automation" {
    bucket = aws_s3_bucket.email_automation.id
    key = "email_template.html"
    source = "../index/email_template.html"
    source_hash = filemd5("../index/email_template.html")

    tags = {
      "Name" = "Bandon"
    }

}

resource "aws_s3_bucket" "bandon_weather_bucket" {
    bucket = "bandon-weather-data-bucket"

    tags = {
      "Name" = "Bandon"
    }

}
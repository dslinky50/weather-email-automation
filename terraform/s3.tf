resource "aws_s3_bucket" "email_automation" {
    bucket = "weather-email-automation"

    tags = {
      "Name" = "Bandon"
    }
    
}

resource "aws_s3_object" "email_automation" {
    bucket = aws_s3_bucket.email_automation.id
    key = "email_tempalate.html"
    source = "../index/email_template.html"

    tags = {
      "Name" = "Bandon"
    }

}
provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "covid_lambda_exec_role" {
  name = "covid_lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}
resource "aws_iam_policy" "covid_s3_write" {
  name        = "covid_s3_write"
  description = "IAM policy to allow Lambda function to update the covid json file"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPut",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::nicolas17/covid-ar.json",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logging_atch" {
  role       = aws_iam_role.covid_lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
resource "aws_iam_role_policy_attachment" "covid_s3_write_atch" {
  role       = aws_iam_role.covid_lambda_exec_role.name
  policy_arn = aws_iam_policy.covid_s3_write.arn
}

resource "aws_lambda_function" "update_covid_json" {
  filename      = "build/function.zip"
  function_name = "update_covid_json"
  role          = aws_iam_role.covid_lambda_exec_role.arn
  handler       = "main.handler"
  timeout       = 10

  source_code_hash = filebase64sha256("build/function.zip")

  runtime = "python3.7"
}

resource "aws_cloudwatch_event_rule" "covid_cloudwatch_timer" {
  description = "Hourly timer to trigger covid lambda"

  schedule_expression = "rate(60 minutes)"
}
resource "aws_cloudwatch_event_rule" "covid_cloudwatch_timer2" {
  description = "More regular timer near 10pm (UTC-3) to trigger covid lambda"

  schedule_expression = "cron(0/10 1-2 * * ? *)"
}

resource "aws_cloudwatch_event_target" "cloudwatch_timer_target" {
  rule = aws_cloudwatch_event_rule.covid_cloudwatch_timer.name
  arn = aws_lambda_function.update_covid_json.arn
}
resource "aws_cloudwatch_event_target" "cloudwatch_timer_target2" {
  rule = aws_cloudwatch_event_rule.covid_cloudwatch_timer2.name
  arn = aws_lambda_function.update_covid_json.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_covid_json.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.covid_cloudwatch_timer.arn
}

resource "aws_lambda_permission" "allow_cloudwatch2" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_covid_json.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.covid_cloudwatch_timer2.arn
}


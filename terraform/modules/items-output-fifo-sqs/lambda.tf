resource "aws_lambda_function" "copier" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-schedule-queue-adder"
  role             = aws_iam_role.copier.arn
  handler          = "items/schedule_queue.add"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      OUTPUT_FIFO_SQS_URL = aws_sqs_queue.output.url
      PREFIX              = var.prefix
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.copier]
}

resource "aws_cloudwatch_log_group" "copier" {
  name              = "/aws/lambda/${var.prefix}-schedule-queue-adder"
  retention_in_days = 14
}

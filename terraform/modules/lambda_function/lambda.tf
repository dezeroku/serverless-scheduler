resource "aws_lambda_function" "lambda" {
  filename         = var.lambda_zip_path
  function_name    = var.function_name
  role             = aws_iam_role.lambda.arn
  handler          = var.handler
  runtime          = var.runtime
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = var.environment
  }
  timeout    = var.timeout
  depends_on = [aws_cloudwatch_log_group.lambda]

  layers = var.layer_arns
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 14
}

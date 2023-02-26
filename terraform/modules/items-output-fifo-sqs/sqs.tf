resource "aws_sqs_queue" "output" {
  name                        = "${var.prefix}-schedule-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true

  # We allow Lambda to run for 60 seconds, let's make this x10 to make sure function wasn't throttled
  visibility_timeout_seconds = 600

  # TODO: handle dead-letter queue
  #  redrive_policy = jsonencode({
  #  maxReceiveCount = 10
  #  deadLetterTargetArn = "some_queue_arn"
  #  })
}

resource "aws_sqs_queue" "output" {
  name                        = "${var.prefix}-schedule-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

resource "aws_sqs_queue" "output" {
  name                        = "${var.prefix}-items-output.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

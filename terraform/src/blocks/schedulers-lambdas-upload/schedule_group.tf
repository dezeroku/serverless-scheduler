# Prepare the ScheduleGroup to use later on
resource "aws_scheduler_schedule_group" "group" {
  name = var.schedulers_group
}

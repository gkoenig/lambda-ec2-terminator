variable "aws_region" {
    default="eu-central-1"
}

variable "termination_dry_run" {
    default="True"
}
variable "lb_name" {}

variable "lambda_schedule" {
  description = "cron(Minutes Hours Day-of-month Month Day-of-week Year), default: hourly on week days 8-15h UTC"
  default="cron(0 8-17 ? * MON-FRI *)"  
}

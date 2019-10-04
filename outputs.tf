output "aws_account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}
output "aws_caller_user" {
  value = "${data.aws_caller_identity.current.user_id}"
}

output "lambda_function_arn" {
  value = "${aws_lambda_function.lambda_ec2_terminator.arn}"
}
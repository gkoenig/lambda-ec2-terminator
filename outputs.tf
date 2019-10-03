output "aws_account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}
output "aws_caller_user" {
  value = "${data.aws_caller_identity.current.user_id}"
}
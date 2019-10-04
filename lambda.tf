data "archive_file" "my_lambda_function" {
  source_dir  = "${path.module}/code/"
  output_path = "${path.module}/artifact/ec2-terminator.zip"
  type        = "zip"
}

resource "aws_lambda_function" "lambda_ec2_terminator" {
  function_name    = "ec2-terminator"
  handler          = "ec2-terminator.lambda_handler"
  role             = "${aws_iam_role.lambda_ec2terminator_role.arn}"
  runtime          = "python3.7"
  timeout          = 60
  filename         = "${data.archive_file.my_lambda_function.output_path}"
  source_code_hash = "${data.archive_file.my_lambda_function.output_base64sha256}"

  environment {
    variables = {
      LB_NAME = "{var.lb_name}"
      DRY_RUN = "{var.termination_dry_run}"
    }
  }
}

data "template_file" "iam_policy" {
  template = "${file("policy.json.tpl")}"

  vars = {
    aws_account_id = "${data.aws_caller_identity.current.account_id}"
  }
}

resource "aws_iam_policy" "lambda_ec2terminator_policy" {

  policy = "${data.template_file.iam_policy.rendered}"
}

resource "aws_iam_role" "lambda_ec2terminator_role" {
  name = "lambda_ec2_terminator_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# finally attach the policy to the role
resource "aws_iam_policy_attachment" "ec2terminator_policy_attachment" {
  name       = "ec2terminator_policy_attachment"
  roles      = ["${aws_iam_role.lambda_ec2terminator_role.name}"]
  policy_arn = "${aws_iam_policy.lambda_ec2terminator_policy.arn}"
}
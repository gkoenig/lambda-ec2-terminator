{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Effect": "Allow",
        "Action": "autoscaling:Describe*",
        "Resource": "*"
    },
    {
       "Effect": "Allow",
       "Action": [
           "logs:*"
       ],
       "Resource": "arn:aws:logs:*:*:*"
    },
    {
       "Effect": "Allow",
       "Action": "elasticloadbalancing:Describe*",
       "Resource": "*"
    },
    {
       "Effect": "Allow",
       "Action": [
           "ec2:DescribeInstances",
           "ec2:DescribeClassicLinkInstances",
           "ec2:DescribeSecurityGroups"
       ],
       "Resource": "*"
    },
    {
       "Effect": "Allow",
       "Action": "ec2:TerminateInstances",
       "Resource": "arn:aws:ec2:eu-central-1:${aws_account_id}:instance/*"
    }
  ]
}
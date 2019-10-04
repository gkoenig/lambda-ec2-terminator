# EC2 terminator

## What ?
Implementation of a Lambda function, triggered on regular intervalls, to terminate an EC2 instance behind a LoadBalancer....like a _smart chaos-monkey_ .  
The target of the LoadBalancer needs to be one or more Autoscaling group(s) and the function checks the sum of desired instances.
Only if all instances are "InState" the oldest one will be terminated, means as soon as one of the target EC2 instances is out-of-order
the function exits without terminating any further.

In addition to the pure lambda function implementation, the setup/deployment is automated via Terraform.
Via Terraform all the dependent/required resources of the lambda function will be created, like IAM policies, Cloudwatch event and -target, ...

## Handling
### Prerequisites
- aws credentials configured, either in ~/.aws/credentials or via environment variables
- terraform [installed ](https://learn.hashicorp.com/terraform/getting-started/install.html)
  
### Parameters:  

file _variables.tf_
  - *lb_name* (required): name of your loadbalancer, behind which the EC2 instances are configured in a ASG
  - *aws_region* : the AWS region where your ressources are running (default: _eu-central-1_)
  - *termination_dry_run* : either True or False , determines if the final termination shall just be simulated or really executed (default: _True_, means just simulate the termination)
  - *lambda_schedule* : _when_ to trigger the lambda function, specified in cron-like format (default: cron(0 8-17 ? * MON-FRI *) , which means _trigger lambda on any workday on full hour between 8-17h UTC_)

### Deployment
```
terraform init #only once, to fetch the aws provisioner
```
```
terraform validate
terraform plan -var 'lb_name=<<your-loadbalancer-name>>'
terraform apply -var 'lb_name=<<your-loadbalancer-name>>'
```
### Usage

After the terrafrom deployment you can check the created resource(s) in the AWS management console, e.g. the [lambda page](https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-central-1).
Within the lambda console you can also manually trigger your function for testing purposes.  
The logs of the lambda function execution will be sent to Cloudwatch, within a dedicated log-group ```/aws/lambda/ec2-terminator```

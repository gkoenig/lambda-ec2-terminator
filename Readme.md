# EC2 terminator

## What ?

## helpful commands

```
aws --profile aws-gerd lambda list-functions
```
```
zip ec2-terminator.zip ec2-terminator.py
```
```
aws --profile aws-gerd lambda create-function --function-name test-ec2-terminator --zip-file fileb://ec2-terminator.zip --role arn:aws:iam::134246102036:role/lambda-s3-role --runtime python3.6 --handler "ec2-terminator.lambda_handler" --environment Variables={REGION=eu-central-1}
```
```
aws --profile aws-gerd lambda delete-function --function-name test-ec2-terminator
```

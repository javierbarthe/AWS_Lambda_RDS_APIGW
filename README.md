# AWS_Lambda_RDS_APIGW
AWS Lambda Function for insert and select data from a Aurora (PostgreSQL Compatible) by Api Gateway

1. Create your RDS Amazon Aurora PostgreSQL compatible instance.
2. Create the lambda function.
  2.1 Upload code with postgresql libraries folder inside a zip file. You can download postgresql files from https://github.com/jkehler/awslambda-psycopg2.
3. Create the Api Gateway with Lambda integration.
4. For executing the api outside aws you will need AccessKey and SecretKey (IAM).

Test on Lambda side will not work as this function is prepared for Api Gateway request.

Thanks!
Hope Helps.

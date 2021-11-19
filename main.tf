#Provider da AWS - variáveis a setar no arquivo variables.tf
provider "aws" {
    region = "${var.aws_region}"
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
}

provider "archive" {}

data "archive_file" "zip" {
    type = "zip"
    source_file = "lambda_handler.py"
    output_path = "lambda_handler.zip"
}

#criando Role Policy lambdapolicy
resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.role_for_LDC.id

  policy = file("policy.json")
}

#criando Role myrole
resource "aws_iam_role" "role_for_LDC" {
    name = "myrole"
    assume_role_policy = file("assume_role_policy.json")
}

#resource lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "lambda_handler"
  filename = "${data.archive_file.zip.output_path}"
  source_code_hash = "${data.archive_file.zip.output_base64sha256}"
  role = aws_iam_role.role_for_LDC.arn
  handler = "lambda_handler.lambda_handler"
  runtime = "python3.9"
  timeout = "15"
}

#resource S3 bucket
resource "aws_s3_bucket" "bucketcsdcsdcsd" {
    bucket = "buckettestehexagon"
    acl = "private"
}

#resource Dynamondb
resource "aws_dynamodb_table" "dynamodb_hexagon" {
    name = "dynamodb_hexagon"
    range_key          = "Ano_e_mes_do_lancamento"
    hash_key          = "id"
    stream_enabled    = true
    read_capacity  = 5
    write_capacity = 5
    stream_view_type  = "NEW_AND_OLD_IMAGES"
    billing_mode     = "PROVISIONED"

    attribute {
      name = "Ano_e_mes_do_lancamento"
      type = "S"
    }

    attribute {
      name = "id"
      type = "S"
    }
}

#AWS gambiarra para permissão no lambda function
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucketcsdcsdcsd.arn
}

#trigger para S3
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.bucketcsdcsdcsd.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
}

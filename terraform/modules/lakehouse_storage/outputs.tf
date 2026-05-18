output "bucket_name" {
  description = "Name of the lakehouse S3 bucket."
  value       = aws_s3_bucket.lakehouse.bucket
}

output "bucket_arn" {
  description = "ARN of the lakehouse S3 bucket."
  value       = aws_s3_bucket.lakehouse.arn
}

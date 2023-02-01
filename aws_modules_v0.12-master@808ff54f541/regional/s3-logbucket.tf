##################
# S3 Log bucket
##################

resource "aws_s3_bucket" "s3logbucket" {
  bucket        = local.log_bucketname
  policy        = data.template_file.s3_log_bucketpolicy.rendered
  force_destroy = true
  acl           = "log-delivery-write"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    enabled = true

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  tags = merge(local.common_tags, map("Name", format(local.log_bucketname)))
}

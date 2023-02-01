##################
# S3 Infra bucket
##################

resource "aws_s3_bucket" "infraBucket" {
  bucket        = local.infra_bucketname
  policy        = data.template_file.s3_infra_bucketpolicy.rendered
  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = data.aws_kms_key.kms_key_arn.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }

  logging {
    target_bucket = aws_s3_bucket.s3logbucket.id
    target_prefix = "rsc-${local.infra_bucketname}/"
  }

  tags = merge(local.common_tags, map("Name", format(local.infra_bucketname)))
}

# Block account level s3 public access
resource "aws_s3_account_public_access_block" "example" {
  block_public_acls   = true
  block_public_policy = true
}

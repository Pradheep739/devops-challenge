/* Data Life Cycle Policy */
resource "aws_dlm_lifecycle_policy" "dlm_policy_prod" {
 # provider = "aws.Account_assumeRole"
  count = local.common_tags["Environment"] == "Production" ? 1 : 0
  description        = "Data Lifecycle policy which takes snapshots of the instances in the account with a specific tag"
  execution_role_arn = data.aws_iam_role.dlm_lifecycle_role.arn
  state              = "ENABLED"

  policy_details {
    resource_types = ["INSTANCE"]

    schedule {
      name = "Daily snapshots"

      create_rule {
        interval      = 24
        interval_unit = "HOURS"
        times         = ["16:00"]
      }

      retain_rule {
        count = 30
      }

      tags_to_add = {
        SnapshotCreator = "DLM"
      }

      copy_tags = true
    }

    target_tags = {
      Environment = "Production",
      Scheduler = "True"
    }
  }

  # Need to Add Tags
}

/* Data Life Cycle Policy for Non production accounts */
resource "aws_dlm_lifecycle_policy" "dlm_policy_non_prod" {
 # provider = "aws.Account_assumeRole"
  count = local.common_tags["Environment"] != "Production" ? 1 : 0
  description        = "Data Lifecycle policy which takes snapshots of the instances in the account with a specific tag"
  execution_role_arn = data.aws_iam_role.dlm_lifecycle_role.arn
  state              = "ENABLED"

  policy_details {
    resource_types = ["INSTANCE"]

    schedule {
      name = "Daily snapshots"

      create_rule {
        interval      = 24
        interval_unit = "HOURS"
        times         = ["16:00"]
      }

      retain_rule {
        count = 15
      }

      tags_to_add = {
        SnapshotCreator = "DLM"
      }

      copy_tags = true
    }

    target_tags = {
      Scheduler = "True"
    }
  }

  # Need to Add Tags
}

#### IAM ACCOUNT PASSWORD POLICY MODULE ####

resource "aws_iam_account_password_policy" "password_policy" {
  #provider = "aws-use1"
  max_password_age               = 90
  minimum_password_length        = 14
  allow_users_to_change_password = true
  hard_expiry                    = false
  password_reuse_prevention      = 3
  require_lowercase_characters   = true
  require_uppercase_characters   = true
  require_numbers                = true
  require_symbols                = true
}

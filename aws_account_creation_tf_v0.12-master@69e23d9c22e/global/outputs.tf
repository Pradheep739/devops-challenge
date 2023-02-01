#### OUTPUTS ####

output "jenkins-role" {
  value = module.iam.jenkins-role
}

output "adm_role" {
  value = module.iam.adm_role
}

output "ss_role" {
  value = module.iam.ss_role
}

output "pwrusr_role" {
  value = module.iam.pwrusr_role
}

output "suppwusr_role" {
  value = module.iam.suppwusr_role
}

output "read_role" {
  value = module.iam.read_role
}

output "config_role_arn" {
  value = module.common.config_role_arn
}

output "vpcflowlog_role_arn" {
  value = module.iam.vpcflowlog_role_arn
}

output "lambda_role" {
  value = module.iam.lambda_role
}

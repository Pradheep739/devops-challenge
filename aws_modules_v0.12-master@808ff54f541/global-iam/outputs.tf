#### OUTPUTS ####
output "jenkins-role" {
  value = aws_iam_role.jenkins-role.id
}
output "adm_role" {
  value = aws_iam_role.adm_role.id
}
output "ss_role" {
  value = aws_iam_role.ss-cross-role.id
}
output "pwrusr_role" {
  value = aws_iam_role.pwuser_role.id
}
output "suppwusr_role" {
  value = aws_iam_role.suppwusr_role.id
}
output "read_role" {
  value = aws_iam_role.read_role.id
}
output "vpcflowlog_role_arn" {
  value = aws_iam_role.vpcflowlog_role.arn
}
output "lambda_role" {
  value = aws_iam_role.lambda_role.arn
}
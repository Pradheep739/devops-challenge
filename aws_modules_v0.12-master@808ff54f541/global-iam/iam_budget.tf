
resource "aws_budgets_budget" "budget" {
  name              = local.budget_name
  limit_amount      = var.billing_limit_amount
  time_period_start = var.billing_start_time

  #time_period_start = formatdate("YYYY-MM-DD_hh:mm", timestamp())
  budget_type       = "COST"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = split(",", var.billing_subscriber_email_addresses)
  }
}
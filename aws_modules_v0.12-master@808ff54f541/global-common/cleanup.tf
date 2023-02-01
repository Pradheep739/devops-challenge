
# Call the delete default vpc script
resource "null_resource" "delete_default" {
  provisioner "local-exec" {
    command = "${path.module}/delete-default-vpc.sh"
    interpreter = ["/bin/bash"]
  }
}
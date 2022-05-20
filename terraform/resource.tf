/*  Each resource type should be stored in its own separate file.
    Although related resources can be groupd together in a single file.
    
    Provisioners can be used to configure deployed resources.
    They are (often) run within resource blocks.
    `connection` blocks specify how terraform should connect to the provisioned resource.   
    E.g.:
        resource "digitalocean_droplet" "sample" {
            ...
            connection {
                host = self.ipv4_address
                user = "root"
                type = "ssh"
                private_key = file(var.private_key)
                timeout = "3m"
            }

            provisioner "remote-exec" {
                inline = [
                    "apt update",
                    "apt -y install nginx"
                ]
            }
        }
*/

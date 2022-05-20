/* Define variables to be exposed
    Variable values can be passed to the `terraform` command with the `-var` flag.
    E.g. terraform apply -var "pat=HIFEBSjdjrjs"
*/
variable "pat" {}
variable "domain_name" {}

# Data Types
## Primitive types: string, number, bool
## Lists: Accessed by element indices, e.g. droplet_names[2]
variable "droplet_names" {
  type    = list(string)
  default = ["first", "second", "third"]
}

## Maps: Access using the key (always a string). E.g. equals_map["dev"]
    # Maps can be defined with `=` or `:`.
variable "equals_map" {
    type = map(number)
    default = {
        dev = "dev-1"
        staging = "stag-1"
        production = "prod-1"
    }
}

variable "colon_map" {
  type = map(bool)
    default = {
        "1-dev" : true
        "2-dev" : true
        "3-dev" : true
    }
}

## Set
variable "sub_dns_names" {
    type = set(string)
    default = ["dev", "stag", "prod"]
}


# Looping
#   for_each should be used over count.
## for_each: Lists can be passed in, but they need to first be converted to sets with toset(var.list_name)
resource "digitalocean_droplet" "name" {
  for_each = var.droplets_map
  iamge = "ubuntu-20-04-x64"
  name = "${each.key}-${each.value}"
  size = "s-1vcpu-1gb"
}

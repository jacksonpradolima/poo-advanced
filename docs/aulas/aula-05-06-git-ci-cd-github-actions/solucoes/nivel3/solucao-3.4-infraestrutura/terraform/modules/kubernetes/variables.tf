variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
}

variable "namespaces" {
  description = "Lista de namespaces a criar"
  type        = list(string)
}

output "namespace_names" {
  value = kubernetes_namespace.microservices[*].metadata[0].name
}
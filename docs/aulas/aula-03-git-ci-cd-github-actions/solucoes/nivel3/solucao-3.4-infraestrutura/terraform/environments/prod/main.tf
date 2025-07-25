provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "prod"
}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "prod"
  }
}

module "k8s" {
  source      = "../../modules/kubernetes"
  environment = "prod"
  namespaces  = ["microservices", "monitoring", "istio-system"]
}

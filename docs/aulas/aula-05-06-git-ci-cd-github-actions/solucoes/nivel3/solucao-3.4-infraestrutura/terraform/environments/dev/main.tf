provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "dev"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
    config_context = "dev"
  }
}

module "k8s" {
  source      = "../../modules/kubernetes"
  environment = "dev"
  namespaces  = ["microservices", "monitoring", "istio-system"]
}

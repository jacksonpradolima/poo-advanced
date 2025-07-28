provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "staging"
}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "staging"
  }
}

module "k8s" {
  source      = "../../modules/kubernetes"
  environment = "staging"
  namespaces  = ["microservices", "monitoring", "istio-system"]
}

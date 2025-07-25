terraform {
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.16" }
    helm       = { source = "hashicorp/helm", version = "~> 2.7" }
  }
}

resource "kubernetes_namespace" "microservices" {
  for_each = toset(var.namespaces)
  metadata {
    name = each.value
    labels = { environment = var.environment }
  }
}

resource "helm_release" "istio_base" {
  name             = "istio-base"
  repository       = "https://istio-release.storage.googleapis.com/charts"
  chart            = "base"
  namespace        = "istio-system"
  create_namespace = true
  values = [ yamlencode({ global = { meshID = var.environment } }) ]
}

resource "helm_release" "monitoring" {
  name             = "prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
  values           = [ file("${path.module}/values/prometheus-values.yaml") ]
}

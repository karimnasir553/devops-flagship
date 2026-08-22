resource "kubernetes_namespace" "app" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "urlshortener" {
  name      = "urlshortener"
  chart     = "${path.module}/../helm/urlshortener"
  namespace = kubernetes_namespace.app.metadata[0].name

  set {
    name  = "image.tag"
    value = var.image_tag
  }

  set {
    name  = "replicaCount"
    value = var.replicas
  }
}

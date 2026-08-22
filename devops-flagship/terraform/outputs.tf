output "release_name" {
  value = helm_release.urlshortener.name
}

output "namespace" {
  value = kubernetes_namespace.app.metadata[0].name
}

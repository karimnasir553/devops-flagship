variable "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "kube context to deploy into (kind creates 'kind-flagship')"
  type        = string
  default     = "kind-flagship"
}

variable "namespace" {
  description = "Namespace to deploy into"
  type        = string
  default     = "urlshortener"
}

variable "image_tag" {
  description = "Container image tag to deploy"
  type        = string
  default     = "latest"
}

variable "replicas" {
  description = "Number of replicas (used when autoscaling is disabled)"
  type        = number
  default     = 2
}

{{- define "urlshortener.name" -}}urlshortener{{- end -}}
{{- define "urlshortener.labels" -}}
app: {{ include "urlshortener.name" . }}
{{- end -}}

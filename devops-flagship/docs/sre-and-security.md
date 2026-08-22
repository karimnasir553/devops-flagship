# SRE and Security Practices

## Service objectives

For the URL shortener, measure availability as successful non-5xx requests divided by all requests, excluding intentional 4xx validation responses. The initial 30-day target is 99.5% availability and p95 request latency below 500 ms.

A 99.5% target leaves approximately 216 minutes of monthly error budget. When the budget is exhausted, pause risky changes and prioritize remediation. Review the budget weekly with request error rate, latency, pod restarts, database connectivity, and rollout history.

## Alerting and incident response

Prometheus should alert on 5xx ratio, p95 latency, unavailable replicas, failed readiness probes, and PostgreSQL connectivity. Every page needs an owner, impact statement, linked runbook, acknowledgement time, recovery time, and follow-up action.

```bash
kubectl get pods -n urlshortener
kubectl get events -n urlshortener --sort-by=.lastTimestamp
kubectl logs deployment/urlshortener -n urlshortener --previous
kubectl rollout history deployment/urlshortener -n urlshortener
kubectl rollout undo deployment/urlshortener -n urlshortener
```

## Security controls

- Run the container as a non-root user and keep the image minimal.
- Store `DATABASE_URL` in a Kubernetes Secret or external secret manager; never commit production credentials.
- Use a namespace-scoped service account with only the permissions required by the deployment.
- Enforce non-root pods, resource requests/limits, and signed or immutable image tags with Kyverno or OPA/Gatekeeper.
- Use GitHub Actions OIDC for cloud publishing instead of long-lived cloud credentials.

## Capacity planning

Track CPU, memory, filesystem, request rate, latency, replica count, and database connections over 7-day and 30-day windows. Keep at least 20% node headroom for failover. Scale replicas when the service is stateless; increase cluster capacity only after checking requests, limits, and scheduling constraints.

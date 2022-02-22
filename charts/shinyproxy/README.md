A Helm chart to install Shinyproxy

## Parameters

### Global parameters

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry                    | `""`  |
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]`  |


### Common parameters

| Name                | Description                                                                           | Value           |
| ------------------- | ------------------------------------------------------------------------------------- | --------------- |
| `nameOverride`      | String to partially override nginx.fullname template (will maintain the release name) | `""`            |
| `fullnameOverride`  | String to fully override nginx.fullname template                                      | `""`            |
| `kubeVersion`       | Force target Kubernetes version (using Helm capabilities if not set)                  | `""`            |
| `clusterDomain`     | Kubernetes Cluster Domain                                                             | `cluster.local` |
| `extraDeploy`       | Extra objects to deploy (value evaluated as a template)                               | `[]`            |
| `commonLabels`      | Add labels to all the deployed resources                                              | `{}`            |
| `commonAnnotations` | Add annotations to all the deployed resources                                         | `{}`            |


### ShinyProxy parameters

| Name                 | Description                                                          | Value                       |
| -------------------- | -------------------------------------------------------------------- | --------------------------- |
| `image.registry`     | ShinyProxy image registry                                            | `docker.io`                 |
| `image.repository`   | ShinyProxy image repository                                          | `dabbleofdevops/shinyproxy` |
| `image.tag`          | ShinyProxy image tag (immutable tags are recommended)                | `2.6.0`                     |
| `image.pullPolicy`   | ShinyProxy image pull policy                                         | `IfNotPresent`              |
| `image.pullSecrets`  | Specify docker-registry secret names as an array                     | `[]`                        |
| `image.debug`        | Set to true if you would like to see extra information on logs       | `false`                     |
| `hostAliases`        | Deployment pod host aliases                                          | `[]`                        |
| `command`            | Override default container command (useful when using custom images) | `[]`                        |
| `args`               | Override default container args (useful when using custom images)    | `[]`                        |
| `extraEnvVars`       | Extra environment variables to be set on ShinyProxy containers       | `[]`                        |
| `extraEnvVarsCM`     | ConfigMap with extra environment variables                           | `""`                        |
| `extraEnvVarsSecret` | Secret with extra environment variables                              | `""`                        |


### ShinyProxy deployment parameters

| Name                                    | Description                                                                               | Value   |
| --------------------------------------- | ----------------------------------------------------------------------------------------- | ------- |
| `replicaCount`                          | Number of ShinyProxy replicas to deploy                                                   | `1`     |
| `podLabels`                             | Additional labels for ShinyProxy pods                                                     | `{}`    |
| `podAnnotations`                        | Annotations for ShinyProxy pods                                                           | `{}`    |
| `podAffinityPreset`                     | Pod affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`       | `""`    |
| `podAntiAffinityPreset`                 | Pod anti-affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`  | `soft`  |
| `nodeAffinityPreset.type`               | Node affinity preset type. Ignored if `affinity` is set. Allowed values: `soft` or `hard` | `""`    |
| `nodeAffinityPreset.key`                | Node label key to match Ignored if `affinity` is set.                                     | `""`    |
| `nodeAffinityPreset.values`             | Node label values to match. Ignored if `affinity` is set.                                 | `[]`    |
| `affinity`                              | Affinity for pod assignment                                                               | `{}`    |
| `nodeSelector`                          | Node labels for pod assignment. Evaluated as a template.                                  | `{}`    |
| `tolerations`                           | Tolerations for pod assignment. Evaluated as a template.                                  | `{}`    |
| `priorityClassName`                     | Priority class name                                                                       | `""`    |
| `podSecurityContext.enabled`            | Enabled ShinyProxy pods' Security Context                                                 | `false` |
| `podSecurityContext.fsGroup`            | Set ShinyProxy pod's Security Context fsGroup                                             | `1001`  |
| `podSecurityContext.sysctls`            | sysctl settings of the ShinyProxy pods                                                    | `[]`    |
| `containerSecurityContext.enabled`      | Enabled ShinyProxy containers' Security Context                                           | `false` |
| `containerSecurityContext.runAsUser`    | Set ShinyProxy container's Security Context runAsUser                                     | `1001`  |
| `containerSecurityContext.runAsNonRoot` | Set ShinyProxy container's Security Context runAsNonRoot                                  | `true`  |
| `containerPorts.http`                   | Sets http port inside ShinyProxy container                                                | `8080`  |
| `containerPorts.https`                  | Sets https port inside ShinyProxy container                                               | `""`    |
| `resources.requests.cpu`                | The requested resources for the ShinyProxy container                                      | `200m`  |
| `resources.requests.memory`             | The requested resources for the ShinyProxy container                                      | `512Mi` |
| `resources.limits.cpu`                  | The requested resources for the ShinyProxy container                                      | `300m`  |
| `resources.limits.memory`               | The requested resources for the ShinyProxy container                                      | `800Mi` |
| `livenessProbe.enabled`                 | Enable livenessProbe                                                                      | `true`  |
| `livenessProbe.initialDelaySeconds`     | Initial delay seconds for livenessProbe                                                   | `30`    |
| `livenessProbe.periodSeconds`           | Period seconds for livenessProbe                                                          | `10`    |
| `livenessProbe.timeoutSeconds`          | Timeout seconds for livenessProbe                                                         | `5`     |
| `livenessProbe.failureThreshold`        | Failure threshold for livenessProbe                                                       | `6`     |
| `livenessProbe.successThreshold`        | Success threshold for livenessProbe                                                       | `1`     |
| `readinessProbe.enabled`                | Enable readinessProbe                                                                     | `true`  |
| `readinessProbe.initialDelaySeconds`    | Initial delay seconds for readinessProbe                                                  | `5`     |
| `readinessProbe.periodSeconds`          | Period seconds for readinessProbe                                                         | `5`     |
| `readinessProbe.timeoutSeconds`         | Timeout seconds for readinessProbe                                                        | `3`     |
| `readinessProbe.failureThreshold`       | Failure threshold for readinessProbe                                                      | `3`     |
| `readinessProbe.successThreshold`       | Success threshold for readinessProbe                                                      | `1`     |
| `customLivenessProbe`                   | Override default liveness probe                                                           | `{}`    |
| `customReadinessProbe`                  | Override default readiness probe                                                          | `{}`    |
| `autoscaling.enabled`                   | Enable autoscaling for ShinyProxy deployment                                              | `false` |
| `autoscaling.minReplicas`               | Minimum number of replicas to scale back                                                  | `""`    |
| `autoscaling.maxReplicas`               | Maximum number of replicas to scale out                                                   | `""`    |
| `autoscaling.targetCPU`                 | Target CPU utilization percentage                                                         | `""`    |
| `autoscaling.targetMemory`              | Target Memory utilization percentage                                                      | `""`    |
| `extraVolumes`                          | Array to add extra volumes                                                                | `[]`    |
| `extraVolumeMounts`                     | Array to add extra mount                                                                  | `[]`    |
| `serviceAccount.create`                 | Enable creation of ServiceAccount for nginx pod                                           | `false` |
| `serviceAccount.name`                   | The name of the ServiceAccount to use.                                                    | `""`    |
| `serviceAccount.annotations`            | Annotations for service account. Evaluated as a template.                                 | `{}`    |
| `serviceAccount.autoMount`              | Auto-mount the service account token in the pod                                           | `false` |
| `sidecars`                              | Sidecar parameters                                                                        | `[]`    |
| `sidecarSingleProcessNamespace`         | Enable sharing the process namespace with sidecars                                        | `false` |
| `initContainers`                        | Extra init containers                                                                     | `[]`    |
| `pdb.create`                            | Created a PodDisruptionBudget                                                             | `false` |
| `pdb.minAvailable`                      | Min number of pods that must still be available after the eviction                        | `1`     |
| `pdb.maxUnavailable`                    | Max number of pods that can be unavailable after the eviction                             | `0`     |


### ShinyProxy clusterissuer parameters to enable letsEncrypt

| Name                    | Description                                 | Value   |
| ----------------------- | ------------------------------------------- | ------- |
| `clusterIssuer.enabled` | create a clusterissuer let's encrypt secret | `false` |
| `clusterIssuer.email`   | email to add to letsEncrypt                 | `""`    |


### ShinyProxy AppPod application parameters

| Name                               | Description                            | Value   |
| ---------------------------------- | -------------------------------------- | ------- |
| `appPod.resources.requests.cpu`    | -- Resources requests for spawned pods | `200m`  |
| `appPod.resources.requests.memory` | -- Resources requests for spawned pods | `100Mi` |
| `appPod.resources.limits.cpu`      | -- Resources requests for spawned pods | `300m`  |
| `appPod.resources.limits.memory`   | -- Resources requests for spawned pods | `200Mi` |


### ShinyProxy Proxy application parameters

| Name                                   | Description | Value                                                                                                    |
| -------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| `proxy.title`                          |             | `Open Analytics Shiny Proxy`                                                                             |
| `proxy.logo-url`                       |             | `https://github.com/dabble-of-devops-bioanalyze/biohub-info/raw/master/logos/BioHub_v1_logo_only-01.png` |
| `proxy.landing-page`                   |             | `/`                                                                                                      |
| `proxy.heartbeat-rate`                 |             | `10000`                                                                                                  |
| `proxy.heartbeat-timeout`              |             | `60000`                                                                                                  |
| `proxy.authentication`                 |             | `none`                                                                                                   |
| `proxy.container-backend`              |             | `kubernetes`                                                                                             |
| `proxy.kubernetes.internal-networking` |             | `true`                                                                                                   |
| `proxy.specs`                          |             | `[]`                                                                                                     |


### Traffic Exposure parameters

| Name                            | Description                                                                                 | Value          |
| ------------------------------- | ------------------------------------------------------------------------------------------- | -------------- |
| `service.type`                  | Service type                                                                                | `LoadBalancer` |
| `service.port`                  | Service HTTP port                                                                           | `80`           |
| `service.httpsPort`             | Service HTTPS port                                                                          | `443`          |
| `service.nodePorts`             | Specify the nodePort(s) value(s) for the LoadBalancer and NodePort service types.           | `{}`           |
| `service.targetPort`            | Target port reference value for the Loadbalancer service types can be specified explicitly. | `{}`           |
| `service.loadBalancerIP`        | LoadBalancer service IP address                                                             | `""`           |
| `service.annotations`           | Service annotations                                                                         | `{}`           |
| `service.externalTrafficPolicy` | Enable client source IP preservation                                                        | `Cluster`      |


### Ingress parameters

| Name                        | Description                                                                                                                      | Value                    |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `ingress.enabled`           | Set to true to enable ingress record generation                                                                                  | `false`                  |
| `ingress.pathType`          | Ingress path type                                                                                                                | `ImplementationSpecific` |
| `ingress.apiVersion`        | Force Ingress API version (automatically detected if not set)                                                                    | `""`                     |
| `ingress.hostname`          | Default host for the ingress resource                                                                                            | `nginx.local`            |
| `ingress.path`              | The Path to Nginx. You may need to set this to '/*' in order to use this with ALB ingress controllers.                           | `/`                      |
| `ingress.annotations`       | Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations. | `{}`                     |
| `ingress.tls`               | Create TLS Secret                                                                                                                | `false`                  |
| `ingress.extraHosts`        | The list of additional hostnames to be covered with this ingress record.                                                         | `[]`                     |
| `ingress.extraPaths`        | Any additional arbitrary paths that may need to be added to the ingress under the main host.                                     | `[]`                     |
| `ingress.extraTls`          | The tls configuration for additional hostnames to be covered with this ingress record.                                           | `[]`                     |
| `ingress.secrets`           | If you're providing your own certificates, please use this to add the certificates as secrets                                    | `[]`                     |
| `healthIngress.enabled`     | Set to true to enable health ingress record generation                                                                           | `false`                  |
| `healthIngress.pathType`    | Ingress path type                                                                                                                | `ImplementationSpecific` |
| `healthIngress.hostname`    | When the health ingress is enabled, a host pointing to this will be created                                                      | `example.local`          |
| `healthIngress.annotations` | Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations. | `{}`                     |
| `healthIngress.tls`         | Enable TLS configuration for the hostname defined at `healthIngress.hostname` parameter                                          | `false`                  |
| `healthIngress.extraHosts`  | The list of additional hostnames to be covered with this health ingress record                                                   | `[]`                     |
| `healthIngress.extraTls`    | TLS configuration for additional hostnames to be covered                                                                         | `[]`                     |
| `healthIngress.secrets`     | TLS Secret configuration                                                                                                         | `[]`                     |



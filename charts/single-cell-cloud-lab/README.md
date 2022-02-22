A Helm chart to install the [Single Cell Cloud Lab](https://github.com/dabble-of-devops-bioanalyze/single-cell-cloud-lab) backed by [ShinyProxy](https://www.shinyproxy.io/documentation/configuration).

## Parameters

### Global parameters

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry                    | `""`  |
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]`  |
| `global.storageClass`     | Global StorageClass for Persistent Volume(s)    | `""`  |


### Common parameters

| Name                | Description                                        | Value           |
| ------------------- | -------------------------------------------------- | --------------- |
| `kubeVersion`       | Override Kubernetes version                        | `""`            |
| `nameOverride`      | String to partially override common.names.fullname | `""`            |
| `fullnameOverride`  | String to fully override common.names.fullname     | `""`            |
| `commonLabels`      | Labels to add to all deployed objects              | `{}`            |
| `commonAnnotations` | Annotations to add to all deployed objects         | `{}`            |
| `clusterDomain`     | Kubernetes cluster domain name                     | `cluster.local` |
| `extraDeploy`       | Array of extra objects to deploy with the release  | `[]`            |


### ShinyProxy Proxy application parameters

| Name                                                       | Description                                                                                                                                                                                                                                      | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `shinyproxy.ingress.enabled`                               | enable an ingress                                                                                                                                                                                                                                | `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `shinyproxy.ingress.annotations`                           | annotations to add - usually for nginx ingress and/or external-dns                                                                                                                                                                               | `{}`                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.service.type`                            | LoadBalancer or ClusterIP                                                                                                                                                                                                                        | `LoadBalancer`                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `shinyproxy.proxy.kubernetes.pod-wait-time`                | how long to wait for the pod to spin up                                                                                                                                                                                                          | `600000`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `shinyproxy.proxy.resources.requests.cpu`                  | shinyproxy proxy cpu request                                                                                                                                                                                                                     | `1`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `shinyproxy.proxy.resources.requests.memory`               | shinyproxy proxy memory request                                                                                                                                                                                                                  | `512Mi`                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `shinyproxy.proxy.resources.limits.cpu`                    | shinyproxy proxy memory request                                                                                                                                                                                                                  | `8`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `shinyproxy.proxy.resources.limits.memory`                 | shinyproxy proxy memory request                                                                                                                                                                                                                  | `5G`                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.image.repository`                        | Shiny Proxy docker image repo                                                                                                                                                                                                                    | `dabbleofdevops/shinyproxy`                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `shinyproxy.proxy.image.tag`                               | Shiny Proxy docker image tag                                                                                                                                                                                                                     | `503883c`                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `shinyproxy.proxy.title`                                   | The title that is displayed in the ShinyProxy navigation bar;                                                                                                                                                                                    | `BioAnalyze - Single Cell Cloud Lab`                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.logo-url`                                | The url of the logo that is displayed in the ShinyProxy navigation bar; this can also be a local file using the file scheme (file://)                                                                                                            | `https://github.com/dabble-of-devops-bioanalyze/biohub-info/raw/master/logos/BioHub_v1_logo_only-01.png`                                                                                                                                                                                                                                                                                                                                                    |
| `shinyproxy.proxy.authentication`                          | Authentication see the ShinyProxy [docs](https://www.shinyproxy.io/documentation/configuration/#authentication)                                                                                                                                  | `none`                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `shinyproxy.proxy.landing_page`                            | the URL to send a user to after login; default value is / which will redirect the user to a list of the Shiny apps. Other typical values are /app/<app-name> or /app_direct/<app-name> which allows to immediately land on a (single) Shiny app; | `/app_direct/single-cell-cloud-lab/`                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.specs[0].id`                             | application id                                                                                                                                                                                                                                   | `single-cell-cloud-lab`                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `shinyproxy.proxy.specs[0].port`                           | port the internal application is running on                                                                                                                                                                                                      | `5005`                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `shinyproxy.proxy.specs[0].display_name`                   | Name displayed on the landing page                                                                                                                                                                                                               | `Single Cell Cloud Lab`                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `shinyproxy.proxy.specs[0].container-image`                | Docker image                                                                                                                                                                                                                                     | `dabbleofdevops/k8s-single-cell-cloud-lab:v1.0.0`                                                                                                                                                                                                                                                                                                                                                                                                           |
| `shinyproxy.proxy.specs[0].container-wait-time`            |                                                                                                                                                                                                                                                  | `600000`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `shinyproxy.proxy.specs[0].heartbeat-enabled`              |                                                                                                                                                                                                                                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `shinyproxy.proxy.specs[0].heartbeat-timeout`              |                                                                                                                                                                                                                                                  | `600000`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `shinyproxy.proxy.specs[0].container-memory-request`       |                                                                                                                                                                                                                                                  | `2G`                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.specs[0].container-memory-limit`         |                                                                                                                                                                                                                                                  | `10G`                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `shinyproxy.proxy.specs[0].container-cpu-request`          |                                                                                                                                                                                                                                                  | `1`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `shinyproxy.proxy.specs[0].container-cpu-limit`            |                                                                                                                                                                                                                                                  | `8`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `shinyproxy.proxy.specs[0].target-path`                    |                                                                                                                                                                                                                                                  | `#{proxy.getRuntimeValue('SHINYPROXY_PUBLIC_PATH')}`                                                                                                                                                                                                                                                                                                                                                                                                        |
| `shinyproxy.proxy.specs[0].container-env.CELLXGENE_BUCKET` | S3 Bucket to load data from                                                                                                                                                                                                                      | `my-s3-bucket`                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `shinyproxy.proxy.specs[0].container-env.SCRIPT_NAME`      | SCRIPT_NAME env var to pass to gunicorn for correct proxy                                                                                                                                                                                        | `#{proxy.getRuntimeValue('SHINYPROXY_PUBLIC_PATH').replaceFirst('/$','')}`                                                                                                                                                                                                                                                                                                                                                                                  |
| `shinyproxy.proxy.specs[0].container-env.SYNC_ENABLED`     | Sync local cellxgene results to the S3 Bucket                                                                                                                                                                                                    | `True`                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `shinyproxy.proxy.specs[0].container-env.PUBLIC`           | Let ShinyProxy take care of the Auth                                                                                                                                                                                                             | `True`                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `shinyproxy.proxy.specs[0].kubernetes-pod-patches`         | Add some file mounts and env vars                                                                                                                                                                                                                | `- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_ID
      value: "#{proxy.id}"

- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_USERID
      value: "#{proxy.userId}"

# in case the app has no volumes yet:
- op: add
  path: /spec/volumes
  value:
    - name: cache-volume
      emptyDir: {}

- op: add
  path: /spec/containers/0/volumeMounts
  value:
    - mountPath: /cache
      name: cache-volume` |


  path: /spec/containers/0/env/-
  value:
      name: PROXY_ID
      value: "#{proxy.id}"

- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_USERID
      value: "#{proxy.userId}"

# in case the app has no volumes yet:
- op: add
  path: /spec/volumes
  value:
    - name: cache-volume
      emptyDir: {}

- op: add
  path: /spec/containers/0/volumeMounts
  value:
    - mountPath: /cache
      name: cache-volume` |


  path: /spec/containers/0/env/-
  value:
      name: PROXY_ID
      value: "#{proxy.id}"

- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_USERID
      value: "#{proxy.userId}"

# in case the app has no volumes yet:
- op: add
  path: /spec/volumes
  value:
    - name: cache-volume
      emptyDir: {}

- op: add
  path: /spec/containers/0/volumeMounts
  value:
    - mountPath: /cache
      name: cache-volume` |


  path: /spec/containers/0/env/-
  value:
      name: PROXY_ID
      value: "#{proxy.id}"

- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_USERID
      value: "#{proxy.userId}"

# in case the app has no volumes yet:
- op: add
  path: /spec/volumes
  value:
    - name: cache-volume
      emptyDir: {}

- op: add
  path: /spec/containers/0/volumeMounts
  value:
    - mountPath: /cache
      name: cache-volume` |


  path: /spec/containers/0/env/-
  value:
      name: PROXY_ID
      value: "#{proxy.id}"

- op: add
  path: /spec/containers/0/env/-
  value:
      name: PROXY_USERID
      value: "#{proxy.userId}"

# in case the app has no volumes yet:
- op: add
  path: /spec/volumes
  value:
    - name: cache-volume
      emptyDir: {}

- op: add
  path: /spec/containers/0/volumeMounts
  value:
    - mountPath: /cache
      name: cache-volume` |



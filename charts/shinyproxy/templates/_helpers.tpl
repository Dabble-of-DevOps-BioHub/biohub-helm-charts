{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "shinyproxy.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "shinyproxy.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "shinyproxy.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "shinyproxy.labels" -}}
helm.sh/chart: {{ include "shinyproxy.chart" . }}
{{ include "shinyproxy.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "shinyproxy.selectorLabels" -}}
app.kubernetes.io/name: {{ include "shinyproxy.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "shinyproxy.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "shinyproxy.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Debug functions
*/}}
{{- define "magda.var_dump" -}}
{{- . | mustToPrettyJson |printf "\nThe JSON output of the dumped var is: \n%s" | fail }}
{{- end -}}

{{/*
Auth Functions
Get the auth object and return it in the format shinyproxy expects
*/}}
{{- define "shinyproxy.auth" -}}
{{- $auth := pick .Values "auth" }}
{{- $authYAML := get .Values "authYaml" | fromYaml  }}

{{- $auth := merge $auth $authYAML -}}

{{- $values := pick .Values "proxy" "logging" "management" }}

{{- if $auth.authSimpleEnabled }}
  {{- $_ :=  set $values.proxy "authentication" "simple" }}
  {{- $_ := set $values.proxy "users" $auth.users }}
{{- else if $auth.authNoneEnabled }}
  {{- $_ := set $values.proxy "authentication" "none" }}
{{- else if $auth.authLDAPEnabled }}
  {{-  $_ := set $values.proxy "authentication" "ldap" }}
  {{- $_ := set $values.proxy "ldap" $auth.ldap }}
{{- else if $auth.authKerberosEnabled }}
  {{-  $_ := set $values.proxy "authentication" "kerberos" }}
  {{- $_ := set $values.proxy "kerberos" $auth.kerberos }}
{{- else if $auth.authKeyCloakEnabled }}
  {{-  $_ := set $values.proxy "authentication" "keycloak" }}
  {{- $_ := set $values.proxy "keycloak" $auth.keycloak }}
{{- else if $auth.authOpenIDEnabled }}
  {{-  $_ := set $values.proxy "authentication" "openid" }}
  {{- $_ := set $values.proxy "openid" $auth.openid }}
{{- else if $auth.authSAMLEnabled }}
  {{-  $_ := set $values.proxy "authentication" "saml" }}
  {{- $_ := set $values.proxy "saml" $auth.saml }}
{{- else if $auth.authSocialEnabled }}
  {{- $_ := set $values.proxy "authentication" "social" }}
    {{- $_ := set $values.proxy "social" dict }}
    {{- if $auth.social.twitterEnabled -}}
        {{- $_ := set $values.proxy.social "twitter" (pick $auth.social "twitter") }}
    {{- end -}}
    {{- if $auth.social.facebookEnabled -}}
        {{- $_ := set $values.proxy.social "facebook" (pick $auth.social "facebook") }}
    {{- end -}}
    {{- if $auth.social.googleEnabled -}}
        {{- $_ := set $values.proxy.social "google" (pick $auth.social "google") }}
    {{- end -}}
    {{- if $auth.social.githubEnabled -}}
        {{- $_ := set $values.proxy.social "github" (pick $auth.social "github") }}
    {{- end -}}
    {{- if $auth.social.linkedinEnabled -}}
        {{- $_ := set $values.proxy.social "linkedin" (pick $auth.social "linkedin") }}
    {{- end -}}
{{- else if $auth.authWebServiceEnabled }}
  {{-  $_ := set $values.proxy "authentication" "webservice" }}
  {{- $_ := set $values.proxy "webservice" $auth.webservice }}
{{- end }}

{{- mustToJson $values -}}
{{- end }}
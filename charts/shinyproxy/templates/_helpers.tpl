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
Invoke as
{{- template "magda.var_dump" $myVar }}
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
{{- $auth := $auth.auth }}

{{/*
Values
*/}}
{{- $values := pick .Values "proxy" "logging" "management" }}

{{/*
Auth
*/}}
{{- if $auth.authNoneEnabled }}
  {{- $_ := set $values.proxy "authentication" "none" }}
{{- else if $auth.authLDAPEnabled }}
  {{-  $_ := set $values.proxy "authentication" "ldap" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{-  $_ := set $values.proxy "ldap" dict }}
    {{- range $k, $v := $auth.ldap }}
      {{- $_ := set $values.proxy.ldap (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authKerberosEnabled }}
  {{-  $_ := set $values.proxy "authentication" "kerberos" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{-  $_ := set $values.proxy "kerberos" dict }}
    {{- range $k, $v := $auth.kerberos }}
      {{- $_ := set $values.proxy.kerberos (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authKeyCloakEnabled }}
  {{-  $_ := set $values.proxy "authentication" "keycloak" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{-  $_ := set $values.proxy "keycloak" dict }}
    {{- range $k, $v := $auth.keycloak }}
      {{- $_ := set $values.proxy.keycloak (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authOpenIDEnabled }}
  {{-  $_ := set $values.proxy "authentication" "openid" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{-  $_ := set $values.proxy "openid" dict }}
    {{- range $k, $v := $auth.openid }}
      {{- $_ := set $values.proxy.openid (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authSAMLEnabled }}
  {{-  $_ := set $values.proxy "authentication" "saml" }}
  {{-  $_ := set $values.proxy "saml" dict }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{- range $k, $v := $auth.saml }}
      {{- $_ := set $values.proxy.saml (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authSocialEnabled }}
  {{- $_ := set $values.proxy "authentication" "social" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{- $_ := set $values.proxy "social" dict }}
    {{- if $auth.social.twitterEnabled -}}
        {{-  $_ := set $values.proxy.social "twitter" dict }}
        {{- range $k, $v := $auth.social.twitter }}
          {{- $_ := set $values.proxy.social.twitter (kebabcase $k) $v }}
        {{ end }}
    {{- end -}}
    {{- if $auth.social.facebookEnabled -}}
        {{-  $_ := set $values.proxy.social "facebook" dict }}
        {{- range $k, $v := $auth.social.facebook }}
          {{- $_ := set $values.proxy.social.facebook (kebabcase $k) $v }}
        {{ end }}
    {{- end -}}
    {{- if $auth.social.googleEnabled -}}
        {{-  $_ := set $values.proxy.social "google" dict }}
        {{- range $k, $v := $auth.social.google }}
          {{- $_ := set $values.proxy.social.google (kebabcase $k) $v }}
        {{ end }}
    {{- end -}}
    {{- if $auth.social.githubEnabled -}}
        {{-  $_ := set $values.proxy.social "github" dict }}
        {{- range $k, $v := $auth.social.github }}
          {{- $_ := set $values.proxy.social.github (kebabcase $k) $v }}
        {{ end }}
    {{- end -}}
    {{- if $auth.social.linkedinEnabled -}}
        {{-  $_ := set $values.proxy.social "linkedin" dict }}
        {{- range $k, $v := $auth.social.linkedin }}
          {{- $_ := set $values.proxy.social.linkedin (kebabcase $k) $v }}
        {{ end }}
    {{- end -}}
  {{- end -}}
{{- else if $auth.authWebServiceEnabled }}
  {{-  $_ := set $values.proxy "authentication" "webservice" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{-  $_ := set $values.proxy "webservice" dict }}
    {{- range $k, $v := $auth.webservice }}
      {{- $_ := set $values.proxy.webservice (kebabcase $k) $v }}
    {{ end }}
  {{ end }}
{{- else if $auth.authSimpleEnabled }}
  {{- $_ := set $values.proxy "authentication" "simple" }}
  {{- if not .Values.authExistingSecretEnabled }}
    {{- $_ := set $values.proxy "users" $auth.users }}
    {{ if kindIs "slice" $auth.users }}
      {{- $_ := set $values.proxy "users" $auth.users }}
    {{ else }}
      {{- $usersList := list $auth.users }}
      {{- $_ := set $values.proxy "users" $usersList }}
    {{ end }}
  {{ end }}
{{- end }}


{{/*
Proxy
*/}}

{{ if kindIs "map" $values.proxy.specs }}
  {{- $specs := pick $values.proxy "specs" }}
  {{- $specs := list $specs.specs }}
  {{- $_ := unset $values.proxy "specs"  }}
  {{- $_ := set $values.proxy "specs" $specs }}
{{ end }}

{{- range $k, $v := $values.proxy }}
  {{- $_ := set $values.proxy (kebabcase $k) $v }}
  {{- $kebabKey := (kebabcase $k) }}
  {{- if ne $k $kebabKey -}}
    {{- $_ := unset $values.proxy $k }}
  {{ end }}
{{ end }}

{{- range $k, $v := $values.proxy.kubernetes }}
  {{- $_ := set $values.proxy.kubernetes (kebabcase $k) $v }}
  {{- $kebabKey := (kebabcase $k) }}
  {{- if ne $k $kebabKey -}}
    {{- $_ := unset $values.proxy.kubernetes $k }}
  {{ end }}
{{ end }}

{{- range $l := $values.proxy.specs }}
  {{- range $k, $v := $l }}
    {{- $_ := set $l (kebabcase $k) $v }}
    {{- $kebabKey := (kebabcase $k) }}
    {{- if ne $k $kebabKey -}}
      {{- $_ := unset $l $k }}
    {{ end }}
  {{ end }}
{{ end }}

{{- mustToJson $values -}}

{{- end }}
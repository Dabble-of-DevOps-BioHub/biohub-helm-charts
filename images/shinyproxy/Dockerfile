#FROM openjdk:11-jre
FROM bitnami/java:11-debian-10

ARG SHINYPROXY_VERSION="2.6.0"

RUN useradd -m -u 1001 -s /bin/bash shiny
RUN mkdir -p /opt/shinyproxy/ && chown shiny /opt/shinyproxy
COPY templates/ /opt/shinyproxy/templates/
RUN wget https://www.shinyproxy.io/downloads/shinyproxy-$SHINYPROXY_VERSION.jar -O /opt/shinyproxy/shinyproxy.jar

# TODO Change to bitnami 1001?
# non root user!
USER shiny
WORKDIR /opt/shinyproxy/
CMD ["java", "-jar", "shinyproxy.jar"]

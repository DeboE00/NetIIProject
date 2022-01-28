FROM mongo:latest
LABEL maintainer="enrico.debon@studenti.unitn.it"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install net-tools iproute2 -yy --no-install-recommends && apt clean
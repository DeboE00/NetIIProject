FROM mongo:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install net-tools iproute2 iputils-ping -yy --no-install-recommends && apt clean
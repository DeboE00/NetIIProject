FROM open5gs/open5gs-webui:latest

RUN apt-get update && \
  apt-get install -qy iptables net-tools iproute2 iputils-ping -yy --no-install-recommends && apt clean


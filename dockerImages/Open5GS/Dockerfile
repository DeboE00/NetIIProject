FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install software-properties-common -y --no-install-recommends && add-apt-repository ppa:open5gs/latest && apt update && apt install open5gs -y --no-install-recommends && apt clean
COPY ./amf.yaml /etc/open5gs/amf.template.yaml
WORKDIR /
COPY startup.sh /startup.sh
RUN /startup.sj

# Build image
FROM ubuntu:20.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive
ENV UERANSIM_VERSION=v3.2.6
RUN apt update && apt install make gcc g++ libsctp-dev lksctp-tools iproute2 git vim iptables net-tools ifupdown iputils-ping libssl-dev software-properties-common lsb-release wget -y --no-install-recommends && wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main" && apt update && apt install kitware-archive-keyring && apt update && apt install cmake -y --no-install-recommends && apt clean
RUN cd / && git clone https://github.com/aligungr/UERANSIM && cd UERANSIM && git checkout ${UERANSIM_VERSION} && make -j`nproc`
WORKDIR /UERANSIM/build

# Effective image
FROM ubuntu:20.04
RUN apt update && apt install libsctp-dev lksctp-tools iproute2 net-tools iputils-ping iptables netbase ifupdown curl tcpdump python3 python3-numpy python3-psutil iperf3 -y --no-install-recommends && apt clean
RUN mkdir /UERANSIM
WORKDIR /UERANSIM/
ENV PATH="/UERANSIM:${PATH}"
COPY --from=builder /UERANSIM/build/* /UERANSIM/

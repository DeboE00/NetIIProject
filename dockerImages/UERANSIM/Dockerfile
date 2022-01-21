# Build image
FROM ubuntu:20.04 AS builder
MAINTAINER enrico.debon@studenti.unitn.it
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install make gcc g++ libsctp-dev lksctp-tools iproute2 git software-properties-common lsb-release wget -y --no-install-recommends && wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main" && apt update && apt install kitware-archive-keyring && apt update && apt install cmake -y --no-install-recommends && apt clean
RUN cd / && git clone https://github.com/aligungr/UERANSIM && cd UERANSIM && make -j`nproc`
WORKDIR /UERANSIM/build

# Effective image
FROM ubuntu:20.04
MAINTAINER enrico.debon@studenti.unitn.it
RUN apt update && apt install lksctp-tools iproute2 -y --no-install-recommends && apt clean
RUN mkdir /UERANSIM
WORKDIR /UERANSIM/
ENV PATH="/UERANSIM:${PATH}"
COPY --from=builder /UERANSIM/build/* /UERANSIM/

FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
  apt-get install -y locales && \
  locale-gen pt_BR.UTF-8 && \
  update-locale LANG=pt_BR.UTF-8 && \
  echo "LANG=pt_BR.UTF-8" >> /etc/default/locale && \
  echo "keyboard-configuration  keyboard-configuration/layoutcode  select  br" | debconf-set-selections && \
  echo "keyboard-configuration  keyboard-configuration/modelcode  select  abnt2" | debconf-set-selections && \
  echo "keyboard-configuration  keyboard-configuration/variantcode  select  " | debconf-set-selections && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  keyboard-configuration console-setup \
  python3.10 python3-pip python3-dev \
  build-essential pkg-config \
  default-libmysqlclient-dev \
  netcat curl wget nano && \
  apt-get clean

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8
ENV TZ=America/Sao_Paulo

COPY . .

RUN python3 -m pip install --upgrade pip setuptools wheel
ENV PIP_DEFAULT_TIMEOUT=180 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python3 -m pip install --no-cache-dir --timeout 180 --retries 10 -r requirements.txt

EXPOSE 8552

CMD ["sh", "-c", "streamlit run main.py --server.port=8552 --server.address=0.0.0.0"]

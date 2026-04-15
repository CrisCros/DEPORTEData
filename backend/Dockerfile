FROM eclipse-temurin:17-jdk-jammy AS builder


# System + Python
RUN apt-get update && apt-get install -y \
    curl vim wget software-properties-common ssh ca-certificates \
    python3 python3-pip python3-numpy python3-scipy python3-pandas \
    unzip maven git && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Python (+ librerias ejem. "pandas"): FastAPI + PySpark + AWS + MySQL + JWT
RUN pip3 install --no-cache-dir \
    pyspark==3.5.5 boto3 mysql-connector-python pandas \
    "fastapi>=0.110" "uvicorn[standard]>=0.27" "pydantic-settings>=2.0" \
    python-multipart "python-jose[cryptography]>=3.3"

# Spark 3.5.5 (para spark-submit al master remoto)
ENV SPARK_VERSION=3.5.5 \
    HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark \
    PYTHONHASHSEED=1

RUN wget -q "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    -O /tmp/spark.tgz && mkdir -p /opt/spark && \
    tar -xf /tmp/spark.tgz -C /opt/spark --strip-components=1 && rm /tmp/spark.tgz


# JARs via Maven (S3 + MySQL)
WORKDIR /tmp/maven-build
COPY pom.xml .
RUN mvn dependency:copy-dependencies -DoutputDirectory=/opt/spark/jars


# Final image
FROM builder AS deportedata-api

ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

RUN mkdir -p /opt/deportedata-api/app /opt/spark-apps
WORKDIR /opt/deportedata-api

COPY app/ /opt/deportedata-api/app/
COPY spark-jobs/ /opt/spark-apps/

EXPOSE 8000 8001

COPY start-api.sh /start-api.sh
RUN sed -i 's/\r$//g' /start-api.sh && chmod +x /start-api.sh

CMD ["/bin/bash", "/start-api.sh"]

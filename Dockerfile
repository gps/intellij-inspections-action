FROM openkbs/ubuntu-bionic-jdk-mvn-py3

ARG INTELLIJ_VERSION="ideaIC-2019.3.1"

ARG INTELLIJ_IDE_TAR=${INTELLIJ_VERSION}.tar.gz

WORKDIR /opt

COPY jdk.table.xml /etc/idea/config/options/
COPY entrypoint.sh /entrypoint.sh
COPY analyze_inspections.py /analyze_inspections.py

RUN wget -nv https://download-cf.jetbrains.com/idea/${INTELLIJ_IDE_TAR} && \
    tar xzf ${INTELLIJ_IDE_TAR} && \
    tar tzf ${INTELLIJ_IDE_TAR} | head -1 | sed -e 's/\/.*//' | xargs -I{} ln -s {} idea && \
    rm ${INTELLIJ_IDE_TAR} && \
    echo idea.config.path=/etc/idea/config >> idea/bin/idea.properties && \
    chmod -R 777 /etc/idea && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

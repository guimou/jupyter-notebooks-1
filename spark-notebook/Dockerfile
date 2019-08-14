FROM ulaval/s2i-minimal-notebook-s3:prod

USER root

COPY . /tmp/src

RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts

ENV XDG_CACHE_HOME=/opt/app-root/src/.cache

# Install required RPMs and ensure that the packages were installed
RUN yum install -y java-1.8.0-openjdk wget \
    && yum clean all && rm -rf /var/cache/yum \
    && rpm -q java-1.8.0-openjdk wget


# Add all artifacts to the /tmp/artifacts
# directory

RUN wget -P /tmp/artifacts/ https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz

# Environment variables
ENV \
    JBOSS_IMAGE_NAME="radanalyticsio/openshift-spark" \
    JBOSS_IMAGE_VERSION="2.4-latest" \
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/spark/bin" \
    SCL_ENABLE_CMD="" \
    SPARK_HOME="/opt/spark" \
    SPARK_INSTALL="/opt/spark-distro" \
    STI_SCRIPTS_PATH="/usr/libexec/s2i" 

# Labels
LABEL \
      io.cekit.version="2.2.7"  \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"  \
      maintainer="Chad Roberts <croberts@redhat.com>"  \
      name="radanalyticsio/openshift-spark"  \
      org.concrt.version="2.2.7"  \
      sparkversion="2.4.0"  \
      version="2.4-latest" 

# Add scripts used to configure the image
COPY modules /tmp/scripts

# Custom scripts
USER root
RUN [ "bash", "-x", "/tmp/scripts/common/install" ]

USER root
RUN [ "bash", "-x", "/tmp/scripts/spark/install" ]

USER 1001

RUN /tmp/scripts/assemble

CMD [ "/opt/app-root/builder/run" ]

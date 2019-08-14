FROM ulaval/s2i-minimal-notebook-s3:prod

USER root

COPY . /tmp/src

RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts && \
    yum install -y epel-release && \
    rpm -v --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro && \
    rpm -Uvh --force http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm  && \
    yum install -y ffmpeg ffmpeg-devel && \
    yum install -y graphviz-gd


ENV XDG_CACHE_HOME=/opt/app-root/src/.cache

USER 1001

RUN /tmp/scripts/assemble

CMD [ "/opt/app-root/builder/run" ]

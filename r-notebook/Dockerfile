FROM ulaval/s2i-minimal-notebook-s3:prod

USER root

COPY . /tmp/src

RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts
    
ENV PATH="/opt/app-root/src/miniconda3/bin:${PATH}"
    
RUN yum install -y libXrender

USER 1001
    
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN chmod +x Miniconda3-latest-Linux-x86_64.sh && ./Miniconda3-latest-Linux-x86_64.sh -b && rm Miniconda3-latest-Linux-x86_64.sh

RUN /opt/app-root/src/miniconda3/bin/conda install -y -c r \
     r-markdown \
     r-sparklyr \
     r-irkernel \
     gxx_linux-64

RUN echo "IRkernel::installspec()" > /tmp/install.r && /opt/app-root/src/miniconda3/bin/R -f /tmp/install.r 

ENV XDG_CACHE_HOME=/opt/app-root/src/.cache

RUN /opt/app-root/src/miniconda3/bin/conda install --quiet --yes \
    'r-base=3.6.*' \
    'r-rodbc=1.3*' \
    'unixodbc=2.3.*' \
    'r-irkernel=0.8*' \
    'r-plyr=1.8*' \
    'r-devtools=2.0*' \
    'r-tidyverse=1.2*' \
    'r-rsqlite=2.1*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=1.0*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' \
    'r-htmltools=0.3*' \
    'r-htmlwidgets=1.3*' \
    'r-hexbin=1.27*' && \
    /opt/app-root/src/miniconda3/bin/conda clean --all -f -y && \
    fix-permissions $CONDA_DIR

USER 1001

RUN /tmp/scripts/assemble

RUN mkdir '/users/home/${JUPYTERHUB_USER}/Rpackages' && echo -e 'R_LIBS=/users/home/${JUPYTERHUB_USER}/Rpackages' > /opt/app-root/src/.Renviron

CMD [ "/opt/app-root/builder/run" ]

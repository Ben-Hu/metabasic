FROM python:3.7.5-slim

ENV HOME=/opt/metabasic/ \
    PATH=/opt/metabasic/.local/bin:${PATH}

RUN groupadd -g 999 metabasic && \
    useradd -r -s /bin/sh -u 999 -g metabasic -d ${HOME} -m metabasic && \
    chown -R 999:0 ${HOME}

USER metabasic

RUN pip install metabasic --user

CMD python
FROM python:3.5-slim
MAINTAINER The MyBook Developers <dev@mybook.ru>

RUN groupadd kayako_exporter && useradd --no-create-home --gid kayako_exporter kayako_exporter

COPY . /tmp/kayako_exporter
WORKDIR /tmp/kayako_exporter
RUN pip install -e .

EXPOSE 9223
USER kayako_exporter
ENTRYPOINT [ "/usr/local/bin/kayako_exporter" ]

FROM python:alpine
LABEL maintainer "scotte@warped.com"

EXPOSE 8080

ARG python_packages="web.py gkeepapi"
ARG build_packages="gcc g++ make libffi-dev openssl-dev python3-dev"

RUN apk --no-cache upgrade \
	&& apk add --no-cache $build_packages \
	&& pip3 install $python_packages \
	&& apk --no-cache del $build_packages \
	&& rm -rf /tmp/*

WORKDIR /

COPY keep_gateway.py /

# Minimal health check that mostly makes sure web.py is alive, not Keep
HEALTHCHECK --interval=60m --timeout=20s \
	CMD wget --quiet --tries=1 --spider http://localhost:8080/healthcheck || exit 1

CMD /keep_gateway.py

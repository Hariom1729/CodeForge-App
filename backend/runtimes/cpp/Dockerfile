FROM alpine:latest
RUN apk add --no-cache g++
RUN adduser -D runner
WORKDIR /code
USER runner
CMD ["/bin/sh"]

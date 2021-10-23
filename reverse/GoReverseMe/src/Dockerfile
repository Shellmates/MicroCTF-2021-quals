FROM golang:1.17.1
ARG SOURCE
ARG OUTFILE
WORKDIR /build
COPY $SOURCE .
RUN go build -o $OUTFILE $SOURCE
ENTRYPOINT ["tail", "-f", "/dev/null"]
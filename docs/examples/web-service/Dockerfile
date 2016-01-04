FROM golang:1.5

EXPOSE 8080

RUN mkdir -p /go/src/app
WORKDIR /go/src/app

COPY . /go/src/app
RUN go get
RUN go build

CMD [ "./app" ]

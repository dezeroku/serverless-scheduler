FROM golang:1.15.2-alpine as builder

RUN apk --no-cache add build-base

WORKDIR /go/src/github.com/d0ku/monitor_page/manager

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=builder /go/src/github.com/d0ku/monitor_page/manager/manager .
COPY --from=builder /go/src/github.com/d0ku/monitor_page/manager/templates ./templates
CMD ["./manager"]

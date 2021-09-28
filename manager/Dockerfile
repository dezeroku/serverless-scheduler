FROM golang:1.15.2-alpine as base

RUN apk --no-cache add build-base

WORKDIR /go/src/github.com/dezeroku/monitor-page/manager

COPY go.mod go.sum ./
RUN go mod download

COPY . .

FROM base as test
RUN go test

FROM base as build
RUN CGO_ENABLED=1 GOOS=linux go build

FROM alpine:3.13 as production

RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=build /go/src/github.com/dezeroku/monitor-page/manager/manager .
COPY --from=build /go/src/github.com/dezeroku/monitor-page/manager/templates ./templates
CMD ["./manager"]

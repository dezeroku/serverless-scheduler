# Use python:3.10 to just install wheels for dependencies instead of compiling
FROM python:3.10 as build

WORKDIR /app

RUN apt update && apt install -y \
        graphviz

RUN pip install diagrams==0.23.3

#ARG UID=1000
#ARG GID=1000

#RUN groupadd -g $GID -o hostuser
#RUN adduser --uid $UID --gid $GID --system --no-create-home hostuser
#USER hostuser
RUN mkdir created

COPY *.py .
RUN for x in $(ls *.py); do python $x; done; mv ./*.png created;

FROM scratch as output
COPY --from=build /app/created/* .

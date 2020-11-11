# First stage: build the executable.
FROM golang:1.13-alpine AS builder

# git is required to fetch go dependencies
# gcc & lib-dev are required to build goose
RUN apk add --no-cache \
    "git>=2.24.1-r0" \
    "gcc>=9.2.0-r4" \
    "libc-dev>=0.7.2-r0"

# Create the user and group files that will be used in the running
# container to run the process as an unprivileged user.
RUN mkdir /user && \
    echo 'nobody:x:65534:65534:nobody:/:' > /user/passwd && \
    echo 'nobody:x:65534:' > /user/group

# Fetch dependencies first; they are less susceptible to change on every build
# and will therefore be cached for speeding up the next build
RUN go get -u github.com/pressly/goose/cmd/goose

# Final stage: the running container.
FROM alpine:3.11 AS final

# Import the user and group files from the first stage.
COPY --from=builder /user/group /user/passwd /etc/

# Import the compiled executable from the first stage.
COPY --from=builder /go/bin/goose /goose

# Download "wait-for" for docker-compose deployment
ADD https://raw.githubusercontent.com/eficode/wait-for/master/wait-for /wait-for
RUN chmod 755 /wait-for

# Set the working directory
WORKDIR /migrate

# Perform any further action as an unprivileged user.
USER nobody:nobody

# Run goose migrate
CMD ["sh", "-c", "/goose $DATABASE_TYPE \"$DATABASE_ADDRESS\" up"]

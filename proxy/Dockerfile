# Dockerfile
FROM httpd:2.4

# Install curl
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Append the "Include conf/vhosts.conf" line to the existing httpd.conf
RUN echo "Include conf/vhosts.conf" >> /usr/local/apache2/conf/httpd.conf

ARG CONFIG_FILE

# Copy the appropriate config file based on the build argument
COPY ${CONFIG_FILE} /usr/local/apache2/conf/vhosts.conf
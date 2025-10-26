FROM google/cloud-sdk:544.0.0-alpine

# Install PostgreSQL client
RUN apk add --no-cache postgresql-client

# Copy the backup script
COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

# Reset parent entrypoint and set command to run backup script
ENTRYPOINT []
CMD ["/usr/local/bin/backup.sh"]

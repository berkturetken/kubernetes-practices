#!/bin/bash
set -e
set -o pipefail

# Error function to handle errors consistently
error_exit() {
  echo "Error: $1"
  exit 1
}

echo "Starting backup process at $(date)"
echo "---------------------------------------------------------------------------------------------------------"

# Authenticate with GCS using the service account key
echo "Authenticating with Google Cloud..."
gcloud auth activate-service-account "${GCS_SERVICE_ACCOUNT}" --key-file=/secrets/gcs/sa-private-key.json --project="${GCS_PROJECT_ID}"

# Validate required environment variables
if [ -z "${POSTGRES_HOST}" ] || [ -z "${POSTGRES_PORT}" ] || [ -z "${POSTGRES_DB}" ] || [ -z "${POSTGRES_USER}" ] || [ -z "${GCS_BUCKET}" ]; then
  error_exit "Missing required environment variables"
fi

echo "Configuration:"
echo "  --> Database: ${POSTGRES_USER}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
echo "  --> GCS Bucket: ${GCS_BUCKET}"
echo "  --> Retention: ${BACKUP_RETENTION_DAYS} days (which is currently disabled)"

# Create backup filename with timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="backup-${TIMESTAMP}.sql.gz"

echo -e "\nCreating database dump..."
if ! pg_dump -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" | gzip > /tmp/"${BACKUP_FILE}"; then
  error_exit "pg_dump command failed. The file has still been created so do not forget to clean it up manually."
fi

# Check if backup file exists and is not empty
if [ ! -f /tmp/"${BACKUP_FILE}" ]; then
  error_exit "Backup file was not created"
fi

if [ ! -s /tmp/"${BACKUP_FILE}" ]; then
  error_exit "Backup file is empty"
fi

BACKUP_SIZE=$(du -h /tmp/"${BACKUP_FILE}" | cut -f1)
echo "✅ Backup created successfully: ${BACKUP_FILE} (${BACKUP_SIZE})"

# Verify backup file is valid
echo -e "\nVerifying if it's a valid gzip file or not..."
if gunzip -t /tmp/"${BACKUP_FILE}"; then
  echo "✅ Backup file verified successfully"
else
  error_exit "Backup file is not a valid one..."
fi

# Count lines in the backup for additional information
LINE_COUNT=$(gunzip -c /tmp/"${BACKUP_FILE}" | wc -l | tr -d ' ')
echo "Backup contains ${LINE_COUNT} lines"

# Upload to GCS
echo -e "\nUploading backup to gs://${GCS_BUCKET}/${BACKUP_FILE}..."
gcloud storage cp /tmp/"${BACKUP_FILE}" gs://"${GCS_BUCKET}"/

if [ $? -eq 0 ]; then
  echo "✅ Backup uploaded successfully to GCS"
else
  error_exit "Failed to upload backup to GCS"
fi

##### Cleaning up old backups from GCS and local #####
# Cleanup old backups (older than BACKUP_RETENTION_DAYS)
# echo "Cleaning up backups older than ${BACKUP_RETENTION_DAYS} days..."
# CUTOFF_DATE=$(date -d "${BACKUP_RETENTION_DAYS} days ago" +%Y%m%d 2>/dev/null || date -v-${BACKUP_RETENTION_DAYS}d +%Y%m%d)

# gsutil ls gs://${GCS_BUCKET}/backup-*.sql.gz | while read backup; do
#   BACKUP_DATE=$(echo $backup | grep -o 'backup-[0-9]\{8\}' | cut -d'-' -f2)
#   if [ "$BACKUP_DATE" -lt "$CUTOFF_DATE" ]; then
#     echo "Deleting old backup: $backup"
#     gsutil rm $backup
#   fi
# done

# # Cleanup local temp file
# rm -f /tmp/${BACKUP_FILE}
##### Cleaning up old backups from GCS and local #####

echo -e "\n➡️➡️ Backup process completed successfully at $(date)"

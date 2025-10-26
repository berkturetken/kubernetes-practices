# Database Solutions Comparison: Cloud SQL vs Self-Managed PostgreSQL on GKE

This document compares two database approaches for our Todo App running on Google Kubernetes Engine (GKE):

1. **DBaaS (Database as a Service)**: Google Cloud SQL for PostgreSQL
2. **Self-Managed**: PostgreSQL StatefulSet with PersistentVolumeClaims on GKE

---

## Table of Contents

- [0. Executive Summary](#0-executive-summary)
- [1. Initial Setup & Required Work](#1-initial-setup--required-work)
  - [1.1. Google Cloud SQL](#11-google-cloud-sql)
  - [1.2. Self-Managed PostgreSQL (Current Approach)](#12-self-managed-postgresql-current-approach)
- [2. Ongoing Maintenance](#2-ongoing-maintenance)
  - [2.1. Google Cloud SQL](#21-google-cloud-sql)
  - [2.2. Self-Managed PostgreSQL](#22-self-managed-postgresql)
- [3. Backup Methods & Ease of Use](#3-backup-methods--ease-of-use)
  - [3.1. Google Cloud SQL Backups](#31-google-cloud-sql-backups)
  - [3.2. Self-Managed PostgreSQL Backups](#32-self-managed-postgresql-backups)
    - [3.2.1. Option 1: pg_dump CronJob (Simplest)](#321-option-1-pg_dump-cronjob-simplest)
    - [3.2.2. Option 2: WAL Archiving + Point-in-Time Recovery (Advanced)](#321-option-2-wal-archiving--point-in-time-recovery-advanced)
    - [3.2.3. Option 3: Velero (Kubernetes-Native)](#321-option-3-velero-kubernetes-native)
- [4. Cost Comparison](#4-cost-comparison)
  - [4.1. Google Cloud SQL Pricing (us-central1)](#41-google-cloud-sql-pricing-us-central1)
  - [4.2. Self-Managed PostgreSQL on GKE Pricing](#42-self-managed-postgresql-on-gke-pricing)
  - [4.3. Cost Break-Even Analysis](#43-cost-break-even-analysis)
- [5. Other Important Considerations](#5-other-important-considerations)
  - [5.1. Security](#51-security)
  - [5.2. Scalability](#52-scalability)
  - [5.3. Monitoring & Observability](#53-monitoring--observability)
- [6. Migration Complexity](#6-migration-complexity)
- [7. Recommendations](#7-recommendations)
  - [7.1. Choose Google Cloud SQL if](#71-choose-google-cloud-sql-if)
  - [7.2. Choose Self-Managed PostgreSQL if](#72-choose-self-managed-postgresql-if)
  - [7.3. Hybrid Approach (Recommended for Many Cases)](#73-hybrid-approach-recommended-for-many-cases)
- [8. Current Setup Assessment](#8-current-setup-assessment)
  - [8.1. Current Implementation](#81-current-implementation)
  - [8.2. Immediate Action Items if Staying Self-Managed](#82-immediate-action-items-if-staying-self-managed)
  - [8.3. If Migrating to Cloud SQL](#83-if-migrating-to-cloud-sql)
- [9. Conclusion](#9-conclusion)

---

## 0. Executive Summary

| Aspect                       | Cloud SQL (DBaaS)                           | StatefulSet + PVC                      |
| ---------------------------- | ------------------------------------------- | -------------------------------------- |
| **Initial Setup Complexity** | Low                                         | Medium                                 |
| **Ongoing Maintenance**      | Minimal                                     | Moderate                               |
| **Cost (Small Scale)**       | Higher base cost                            | Lower base cost                        |
| **Cost (Large Scale)**       | Predictable, can be expensive               | More cost-effective                    |
| **Backup Management**        | Automated, easy                             | Manual setup required                  |
| **High Availability**        | Built-in, managed                           | Requires configuration                 |
| **Performance Tuning**       | Limited control                             | Full control                           |
| **Best For**                 | Production apps, teams without DB expertise | Cost-conscious, DB expertise available |

## 1. Initial Setup & Required Work

### 1.1. Google Cloud SQL

**Setup Steps:**

```bash
# 1. Create Cloud SQL instance (via gcloud or Console)
gcloud sql instances create todo-db \
    --database-version=POSTGRES_16 \
    --tier=db-f1-micro \
    --region=us-central1

# 2. Create database and user
gcloud sql databases create todo_db --instance=todo-db
gcloud sql users create todo_user --instance=todo-db --password=secure_password

# 3. Enable Cloud SQL Proxy or configure private IP
# 4. Create Kubernetes Secret with connection details
kubectl create secret generic cloudsql-db-credentials \
  --from-literal=username=todo_user \
  --from-literal=password=secure_password \
  --from-literal=database=todo_db

# 5. Update deployment to use Cloud SQL Proxy sidecar
```

**Pros ✅:**

- Quick to get production-ready database (5-10 minutes)
- No need to configure StatefulSets, PVCs, or storage classes
- Automatic OS and PostgreSQL patches
- Point-in-time recovery enabled by default
- Built-in monitoring and alerting via Cloud Console

**Cons ❌:**

- Requires Cloud SQL Proxy sidecar container in pods (adds complexity)
- Must manage IAM permissions and service accounts
- Network configuration (public vs private IP, authorized networks)
- Learning curve for Cloud SQL-specific features

**Current Configuration Changes Needed:**

- Add Cloud SQL Proxy sidecar to `todo_backend/manifests/deployment.yaml`
- Replace `PROD_POSTGRES_HOST` with `127.0.0.1` (proxy runs locally in pod)
- Remove `statefulset.yaml` and `db-service.yaml`
- Create Kubernetes Secret for credentials instead of ConfigMap

### 1.2. Self-Managed PostgreSQL (Current Approach)

**Setup Steps:**

```bash
# 1. Create ConfigMap with DB credentials
kubectl apply -f todo_backend/manifests/configmap.yaml

# 2. Deploy StatefulSet with PVC template
kubectl apply -f todo_backend/manifests/statefulset.yaml

# 3. Deploy headless Service
kubectl apply -f todo_backend/manifests/db-service.yaml

# 4. Wait for PVC to bind and pod to become ready
kubectl wait --for=condition=ready pod/todo-stset-0 -n project --timeout=120s
```

**Pros ✅:**

- Complete control over PostgreSQL configuration
- Lower base cost (only pay for compute/storage)
- No vendor lock-in (portable across cloud providers)
- Simple networking (within cluster, no proxy needed)
- Familiar Kubernetes resources

**Cons ❌:**

- Must understand StatefulSets and PVC management
- Responsible for PostgreSQL upgrades and security patches
- Need to set up backup solution manually
- Need to implement HA/replication yourself
- Monitoring and alerting require additional setup

**Current Setup:**

- Already implemented and working
- 100Mi PVC with ReadWriteOnce access
- Headless service for stable network identity
- ConfigMap-based configuration (passwords in plain text - security concern)

## 2. Ongoing Maintenance

### 2.1. Google Cloud SQL

**Maintenance Tasks:**

| Task                        | Frequency    | Effort | Notes                                         |
| --------------------------- | ------------ | ------ | --------------------------------------------- |
| Security patches            | Automatic    | None   | Google manages                                |
| PostgreSQL version upgrades | As needed    | Low    | Click button in Console or run gcloud command |
| Monitor performance         | Daily/Weekly | Low    | Built-in dashboards                           |
| Adjust resources (CPU/RAM)  | As needed    | Low    | Resize instance type                          |
| Review access logs          | Weekly       | Low    | Available in Cloud Logging                    |
| Disaster recovery testing   | Quarterly    | Low    | Restore from backup to test instance          |

**Maintenance Overhead:** ~1-2 hours/month

**Automatic Features:**

- OS-level security patching
- Automated daily backups (retained 7-30 days)
- Point-in-time recovery
- High availability failover (if configured)
- Automatic storage increase (if enabled)
- Query insights and performance recommendations

### 2.2. Self-Managed PostgreSQL

**Maintenance Tasks:**

| Task                        | Frequency    | Effort | Notes                                          |
| --------------------------- | ------------ | ------ | ---------------------------------------------- |
| Security patches            | Manual       | High   | Must rebuild image or use updated base image   |
| PostgreSQL version upgrades | Manual       | High   | Requires careful migration, potential downtime |
| Monitor performance         | Daily/Weekly | Medium | Need to set up Prometheus/Grafana              |
| Adjust resources            | As needed    | Medium | Edit StatefulSet, may require pod restart      |
| Backup configuration        | One-time     | High   | Set up CronJob with pg_dump or use Velero      |
| Restore testing             | Quarterly    | High   | Manual process, scripting recommended          |
| PVC management              | As needed    | Medium | Monitor disk usage, resize PVC if needed       |
| Database tuning             | As needed    | High   | Requires PostgreSQL expertise                  |

**Maintenance Overhead:** ~4-8 hours/month (more if issues arise)

**Manual Setup Required:**

- Install and configure backup solution (pg_dump CronJob, Velero, or pgBackRest)
- Set up monitoring with Prometheus exporters
- Configure log aggregation (Loki/Alloy - we already have this!)
- Implement alerting for disk space, connection limits, etc.
- Plan and execute major version upgrades
- Handle PostgreSQL configuration tuning (postgresql.conf)

## 3. Backup Methods & Ease of Use

### 3.1. Google Cloud SQL Backups

**Built-in Automated Backups:**

```bash
# Backups are automatic, but you can configure:
gcloud sql instances patch todo-db \
  --backup-start-time=02:00 \
  --retained-backups-count=30

# Restore to a point in time (last 7 days)
gcloud sql backups restore <BACKUP_ID> \
  --backup-instance=todo-db \
  --restore-instance=todo-db-restored

# Or restore to a specific timestamp
gcloud sql backups restore <BACKUP_ID> \
  --point-in-time=2025-10-26T10:30:00Z
```

**Features:**

- **Automated daily backups** - completely hands-off
- **Point-in-time recovery (PITR)** - restore to any second within retention period
- **Binary logs** automatically captured for PITR
- **Cross-region backup** option for disaster recovery
- **Backup verification** - Google ensures backups are valid
- **One-click restore** via Console or simple gcloud command
- **No performance impact** during backups (managed system)

**Backup Storage Cost:** ~$0.08/GB/month (separate from instance cost)

**Recovery Time Objective (RTO):** 5-15 minutes for full restore  
**Recovery Point Objective (RPO):** Near-zero (point-in-time recovery)

### 3.2. Self-Managed PostgreSQL Backups

#### 3.2.1. Option 1: pg_dump CronJob (Simplest)

```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: project
spec:
  schedule: "0 2 * * *" # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: postgres:16
              env:
                - name: PGPASSWORD
                  value: todo_pass
              command:
                - /bin/sh
                - -c
                - |
                  pg_dump -h todo-db-svc -p 7654 -U todo_user todo_db | \
                  gzip > /backups/backup-$(date +\%Y\%m\%d-\%H\%M\%S).sql.gz
              volumeMounts:
                - name: backup-storage
                  mountPath: /backups
          restartPolicy: OnFailure
          volumes:
            - name: backup-storage
              persistentVolumeClaim:
                claimName: backup-pvc
```

**Required Steps:**

1. Create PVC for backup storage (separate from DB storage)
2. Apply CronJob manifest
3. Set up backup retention policy (manual cleanup or script)
4. Store backups in GCS bucket for durability (additional CronJob)
5. Test restore process regularly

**Restore Process:**

```bash
# Copy backup file to pod
kubectl cp backup-20251026.sql.gz project/todo-stset-0:/tmp/

# Exec into pod and restore
kubectl exec -it todo-stset-0 -n project -- bash
gunzip -c /tmp/backup-20251026.sql.gz | psql -U todo_user -d todo_db
```

**Pros ✅:**

- Simple to implement
- Lightweight solution
- No additional tools needed

**Cons ❌:**

- Full database dumps (slower for large databases)
- No point-in-time recovery
- Manual restore process
- Need to manage backup retention
- Backups stored on cluster (need to copy to GCS for safety)

#### 3.2.1. Option 2: WAL Archiving + Point-in-Time Recovery (Advanced)

Requires:

1. Configure PostgreSQL for continuous archiving
2. Store WAL files in GCS bucket
3. Set up base backups (pg_basebackup)
4. Configure recovery.conf for PITR

**Pros ✅:**

- Point-in-time recovery capability
- Continuous backup (minimal data loss)
- Industry best practice

**Cons ❌:**

- Complex setup and configuration
- Requires deep PostgreSQL knowledge
- More storage needed (WAL files)
- Complex restore procedure

#### 3.2.1. Option 3: Velero (Kubernetes-Native)

```bash
# Install Velero
velero install --provider gcp --bucket velero-backups \
  --secret-file ./credentials-velero

# Create scheduled backup
velero schedule create todo-daily \
  --schedule="0 2 * * *" \
  --include-namespaces project \
  --ttl 720h
```

**Pros ✅:**

- Backs up entire namespace (app + database)
- Kubernetes-native solution
- Can restore to different cluster
- Disaster recovery for entire app stack

**Cons ❌:**

- Additional tool to learn and maintain
- Backs up PVC state (crash-consistent, not transaction-consistent)
- Large backups (entire PVC)
- May need application quiescing for consistency

## 4. Cost Comparison

### 4.1. Google Cloud SQL Pricing (us-central1)

| Instance Type                           | Specs                   | Instance Cost | Storage Cost            | Backup Cost         | **Total (Single)** | **Total (HA)** |
| --------------------------------------- | ----------------------- | ------------- | ----------------------- | ------------------- | ------------------ | -------------- |
| **db-f1-micro**<br>_(Development)_      | Shared CPU<br>0.6GB RAM | ~$15/mo       | ~$1.70/mo<br>(10GB SSD) | ~$0.80/mo<br>(10GB) | **~$17.50/mo**     | N/A            |
| **db-g1-small**<br>_(Small Production)_ | Shared CPU<br>1.7GB RAM | ~$35/mo       | ~$3.40/mo<br>(20GB SSD) | ~$1.60/mo<br>(20GB) | **~$40/mo**        | N/A            |
| **db-custom-2-7680**<br>_(Production)_  | 2 vCPU<br>7.68GB RAM    | ~$140/mo      | ~$17/mo<br>(100GB SSD)  | ~$8/mo<br>(100GB)   | **~$165/mo**       | **~$330/mo**   |

**Additional Costs:**

- Network egress (usually minimal for in-region traffic)
- Point-in-time recovery logs (included in backup storage)

### 4.2. Self-Managed PostgreSQL on GKE Pricing

| Setup Type                            | Compute Cost                                    | Storage Cost                 | Backup Cost                | **Total**     | Notes                             |
| ------------------------------------- | ----------------------------------------------- | ---------------------------- | -------------------------- | ------------- | --------------------------------- |
| **Development**<br>_(Current Config)_ | Part of GKE node pool<br>(~$0)                  | ~$0.017/mo<br>(100Mi PVC)    | N/A                        | **~$0.02/mo** | Essentially free                  |
| **Small Production**                  | Part of existing node<br>(or ~$25/mo dedicated) | ~$3.40/mo<br>(20GB SSD PD)   | ~$0.40/mo<br>(20GB in GCS) | **~$4/mo**    | Using existing nodes              |
| **Production**                        | ~$50/mo<br>(n1-standard-2 node)                 | ~$17/mo<br>(100GB SSD PD)    | ~$2/mo<br>(100GB in GCS)   | **~$69/mo**   | Single instance                   |
| **High Availability**                 | ~$100/mo<br>(2x nodes)                          | ~$34/mo<br>(2x 100GB SSD PD) | ~$2/mo<br>(100GB in GCS)   | **~$136/mo**  | Requires manual replication setup |

### 4.3. Cost Break-Even Analysis

| Scenario             | Cloud SQL | Self-Managed | Winner                     |
| -------------------- | --------- | ------------ | -------------------------- |
| **Development**      | $17.50/mo | $0.02/mo     | Self-Managed (99% cheaper) |
| **Small Production** | $40/mo    | $4/mo        | Self-Managed (90% cheaper) |
| **Production**       | $165/mo   | $69/mo       | Self-Managed (58% cheaper) |
| **HA Production**    | $330/mo   | $136/mo      | Self-Managed (59% cheaper) |

**BUT:** Factor in engineer time:

- Cloud SQL maintenance: ~4 hours/month @ $30/hour = $120/month
- Self-Managed maintenance: ~12 hours/month @ $30/hour = $360/month

**True Total Cost (Production):**

- Cloud SQL: $165 + $120 = **$285/month**
- Self-Managed: $69 + $360 = **$429/month**

👉 **Cloud SQL becomes cost-effective when factoring in engineering time!**

## 5. Other Important Considerations

### 5.1. Security

| Feature                    | Cloud SQL                 | Self-Managed                            |
| -------------------------- | ------------------------- | --------------------------------------- |
| Encryption at rest         | ✅ Automatic              | ⚠️ Depends on storage class             |
| Encryption in transit      | ✅ Built-in (SSL)         | ⚠️ Must configure                       |
| Automatic security patches | ✅ Yes                    | ❌ Manual                               |
| IAM integration            | ✅ Native                 | ❌ Not available                        |
| Audit logging              | ✅ Built-in               | ⚠️ Must configure                       |
| Secret management          | ⚠️ Still need K8s Secrets | ⚠️ Currently using ConfigMap (insecure) |

**Security Issue in Current Setup:**  
❗ Passwords stored in ConfigMap (plain text) - should use Kubernetes Secrets + SOPS or Google Secret Manager

### 5.2. Scalability

| Aspect                | Cloud SQL                               | Self-Managed                                     |
| --------------------- | --------------------------------------- | ------------------------------------------------ |
| Vertical scaling      | ✅ Easy (change tier, minimal downtime) | ⚠️ Requires pod restart, possible data migration |
| Read replicas         | ✅ Easy to add (1 command)              | ❌ Complex setup                                 |
| Connection pooling    | ⚠️ Need external (PgBouncer)            | ⚠️ Need to configure                             |
| Storage auto-increase | ✅ Available                            | ❌ Manual PVC resize                             |

### 5.3. Monitoring & Observability

| Feature                | Cloud SQL                                           | Self-Managed                               |
| ---------------------- | --------------------------------------------------- | ------------------------------------------ |
| **Dashboards**         | ✅ Built-in (CPU, memory, connections, queries/sec) | ⚠️ Need to configure Grafana dashboards    |
| **Metrics Collection** | ✅ Cloud Monitoring integration (automatic)         | ⚠️ Deploy postgres_exporter for Prometheus |
| **Query Analysis**     | ✅ Query Insights (slow query analysis)             | ❌ Need pg_stat_statements + custom setup  |
| **Recommendations**    | ✅ Recommendations engine                           | ❌ Not available                           |
| **Log Aggregation**    | ✅ Cloud Logging (automatic)                        | ✅ Loki/Alloy (we have this!)              |
| **Alerting**           | ✅ Built-in alert policies                          | ⚠️ Must configure manually                 |
| **Setup Effort**       | None                                                | Medium-High                                |

## 6. Migration Complexity

| Migration Path               | Difficulty | Steps                                           | Expected Downtime                |
| ---------------------------- | ---------- | ----------------------------------------------- | -------------------------------- |
| **Cloud SQL → Self-Managed** | Medium     | Export with pg_dump, import into StatefulSet    | 5-30 minutes (depending on size) |
| **Self-Managed → Cloud SQL** | Easy       | pg_dump from pod, import to Cloud SQL via proxy | 5-30 minutes (depending on size) |

## 7. Recommendations

### 7.1. Choose Google Cloud SQL if:

- You're running a **production application** with uptime requirements
- Your team **lacks deep PostgreSQL expertise**
- You want to **minimize operational overhead**
- **High availability** is critical (HA setup is easy)
- You need **automated, reliable backups** without effort
- You value **managed security patching**
- Budget allows for higher infrastructure costs
- You want **fast time to market**

### 7.2. Choose Self-Managed PostgreSQL if:

- You're building a **development/staging environment**
- You have **strong DevOps/PostgreSQL expertise** on the team
- **Budget is constrained** (startup, side project)
- You need **full control** over database configuration
- You want **maximum portability** across cloud providers
- You're willing to invest time in **custom optimizations**
- You already have robust **backup/monitoring infrastructure**
- Occasional downtime is acceptable (non-critical workloads)

### 7.3. Hybrid Approach (Recommended for Many Cases):

1. **Development/Feature Branches**: Self-managed StatefulSet (current setup)
2. **Staging**: Cloud SQL db-f1-micro ($17/month)
3. **Production**: Cloud SQL db-g1-small or higher with HA

This gives:

- Cost savings in dev (where you spend most time)
- Production reliability without operational burden
- Clear path from dev to prod
- Budget-conscious approach

## 8. Current Setup Assessment

### 8.1. Current Implementation:

- ✅ StatefulSet with PVC (100Mi)
- ✅ Headless service configured correctly
- ✅ ConfigMap for environment variables
- ⚠️ **No backup solution implemented**
- ⚠️ **Passwords in plain text** (ConfigMap instead of Secret)
- ⚠️ **Single replica** (no HA)
- ⚠️ **Small storage** (100Mi - adequate for dev, tiny for prod)

### 8.2. Immediate Action Items if Staying Self-Managed:

1. Implement backup CronJob with GCS storage
2. Move passwords to Kubernetes Secrets (use SOPS for GitOps)
3. Set up monitoring with postgres_exporter
4. Increase PVC size for production namespace
5. Document restore procedure
6. Test disaster recovery

### 8.3. If Migrating to Cloud SQL:

1. Create Cloud SQL instance (db-g1-small for staging)
2. Set up Cloud SQL Proxy in deployment
3. Migrate credentials to Secret
4. Test connection with port-forwarding
5. Export data from StatefulSet and import to Cloud SQL
6. Update DNS/service endpoints
7. Remove StatefulSet and db-service

## 9. Conclusion

There's no universally "best" solution! It depends on the priorities:

- **Cloud SQL** trades money for time and peace of mind
- **Self-Managed** trades time and expertise for cost savings

For most production applications, **Cloud SQL is worth the investment** once you factor in engineering time, reliability, and opportunity cost. For development environments and learning purposes, **self-managed PostgreSQL is excellent**.

The current setup is well-implemented (I guess?) for development! Consider Cloud SQL when moving to production, or invest in proper backup/HA infrastructure if staying self-managed.

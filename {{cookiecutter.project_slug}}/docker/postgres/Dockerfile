FROM postgres:17-trixie

# Set by Docker: amd64 or arm64
ARG TARGETARCH
ARG WALG_VERSION=v3.0.9

# WAL-G needs CA certificates to reach S3 over HTTPS.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Installation as documented in https://github.com/wal-g/wal-g/tree/master/docs#installation
# WAL-G names its arm64 build "aarch64"
RUN case "$TARGETARCH" in amd64) arch=amd64 ;; arm64) arch=aarch64 ;; esac \
    && WALG_ASSET="wal-g-pg-24.04-$arch" \
    && cd /tmp \
    && curl -fsSLO "https://github.com/wal-g/wal-g/releases/download/$WALG_VERSION/$WALG_ASSET.tar.gz" \
    && curl -fsSLO "https://github.com/wal-g/wal-g/releases/download/$WALG_VERSION/$WALG_ASSET.tar.gz.sha256" \
    && sha256sum -c "$WALG_ASSET.tar.gz.sha256" \
    && tar -zxvf "$WALG_ASSET.tar.gz" \
    && mv "$WALG_ASSET" /usr/local/bin/wal-g \
    && rm "$WALG_ASSET.tar.gz" "$WALG_ASSET.tar.gz.sha256" \
    && wal-g --version

# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.49/supercronic-linux-${TARGETARCH} \
    SUPERCRONIC=supercronic-linux-${TARGETARCH}

# Checksum per build, from the release notes
RUN case "$TARGETARCH" in \
        amd64) SUPERCRONIC_SHA1SUM=e63c11a9726b775a6a11801e81af4f3fb926aa68 ;; \
        arm64) SUPERCRONIC_SHA1SUM=0b6c5bb743e0b0dafed1132198c81807927ac413 ;; \
    esac \
 && curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Local backups and restore target folders, only accessible by postgres
RUN install -d -m 700 -o postgres -g postgres /backups /restore

# Save backups locally unless walg.env sets S3
ENV WALG_FILE_PREFIX=/backups \
    WALG_COMPRESSION_METHOD=zstd

# Nightly backup schedule
COPY crontab /etc/supercronic/crontab
COPY backup.sh backup-scheduler.sh restore.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/backup.sh /usr/local/bin/backup-scheduler.sh /usr/local/bin/restore.sh

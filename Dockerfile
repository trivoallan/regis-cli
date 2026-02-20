# Use an official Python slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies and analyzers
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    skopeo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with a home directory and ensure it's writable
RUN groupadd -g 1001 regis && \
    useradd -u 1001 -g regis -m -d /home/regis regis && \
    chmod 755 /home/regis
ENV HOME=/home/regis

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install Hadolint
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then hadolint_arch="x86_64"; else hadolint_arch="arm64"; fi && \
    curl -sSfL "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-${hadolint_arch}" -o /usr/local/bin/hadolint && \
    chmod +x /usr/local/bin/hadolint

# Set work directory and ensure it's owned by regis
WORKDIR /app
RUN chown regis:regis /app && chmod 777 /app

# Copy project files and ensure ownership
COPY --chown=regis:regis . .

# Install regis-cli
RUN pip install --no-cache-dir .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD regis-cli list || exit 1

# Switch to non-root user
USER regis

# Default command
ENTRYPOINT ["regis-cli"]
CMD ["--help"]

FROM python:3.12-slim

LABEL org.opencontainers.image.title="MCP-Fortress"
LABEL org.opencontainers.image.description="Production-grade security firewall & proxy for AI Agent MCP"
LABEL org.opencontainers.image.source="https://github.com/Avoceous/mcpshield"
LABEL org.opencontainers.image.licenses="MIT"

# Create non-root user
RUN addgroup --system mcpshield && \
    adduser --system --ingroup mcpshield mcpshield

WORKDIR /app

# Copy files required to build the package
COPY pyproject.toml .
COPY README.md .
COPY mcpshield ./mcpshield

# Install package
RUN pip install --no-cache-dir ".[proxy,yaml]"

# Copy remaining project files
COPY examples ./examples
COPY tests ./tests
COPY docs ./docs

RUN mkdir -p /app/config /app/logs

RUN cp examples/policy_enterprise.yaml /app/config/policy.yaml

RUN chown -R mcpshield:mcpshield /app

USER mcpshield

EXPOSE 8100
EXPOSE 8101

ENV UPSTREAM_MCP_URL=http://localhost:3000
ENV MCPSHIELD_HOST=0.0.0.0
ENV MCPSHIELD_PORT=8100
ENV MCPSHIELD_POLICY=/app/config/policy.yaml
ENV MCPSHIELD_AUDIT_LOG=/app/logs/audit.jsonl

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8100/api/v1/health')"

CMD [
    "mcp-fortress",
    "proxy",
    "--upstream",
    "http://localhost:3000",
    "--host",
    "0.0.0.0",
    "--port",
    "8100",
    "--policy",
    "/app/config/policy.yaml"
]

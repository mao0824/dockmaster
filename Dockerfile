FROM python:3.12-alpine
WORKDIR /app
COPY app.py index.html ./
EXPOSE 13002
HEALTHCHECK --interval=60s --timeout=10s --retries=3 --start-period=15s \
  CMD python3 -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:13002/api/status',timeout=5)"
CMD ["python3","-u","app.py"]

FROM python:slim
RUN useradd --create-home --shell /bin/bash scanner
WORKDIR /home/scanner
USER scanner
ENV MONGODB_USER=user
ENV MONGODB_PASS=password
RUN mkdir -p .local/share/webtech
RUN mkdir geoip2
COPY geoip2 ./geoip2
COPY webtech ./.local/share/webtech
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./scanner ./
ENTRYPOINT [ "python3","CLI.py"]


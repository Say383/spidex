FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash scanner
WORKDIR /home/scanner
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER scanner
COPY ./scanner ./
COPY ./ranges ./
CMD ["bash"]



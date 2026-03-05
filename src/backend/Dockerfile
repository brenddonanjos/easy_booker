FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade "pip<26" "setuptools<82" wheel

COPY requirements.txt ./

# usa o mesmo ambiente (com setuptools<82) para buildar o whisper
RUN pip install --no-build-isolation -r requirements.txt

COPY . .

EXPOSE 5000
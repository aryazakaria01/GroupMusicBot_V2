FROM nikolaik/python-nodejs:python3.12-nodejs21

WORKDIR /app/

RUN apt-get -qq update -y && apt-get -qq upgrade -y
RUN python3.10 -m pip install -U pip

COPY . /app/
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
RUN pip3 install --upgrade yt-dlp
RUN apt-cache policy yt-dlp
RUN rm -rf requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash", "start"]

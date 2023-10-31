FROM python:3.9.18

WORKDIR /home/ubuntu/mlopspipeline/docker/deeplearning/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR ./app

CMD 

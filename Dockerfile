FROM python:3.7.7

COPY requirements.txt /
RUN pip install -r /requirements.txt \ 
&& apt update \
&& apt-get install p7zip-full -y

COPY start_bot.sh /
RUN chmod +x /start_bot.sh

COPY . .
WORKDIR /comedy_bot/models/text_gen/
RUN wget https://www.dropbox.com/s/ay8q3f85alpn8b7/text_gen.7z?dl=0 -O text_gen.7z \
&& 7za e text_gen.7z \
&& rm text_gen.7z

WORKDIR /comedy_bot/models/text_classify/
RUN wget https://www.dropbox.com/s/s48j3ql8hyw01ad/text_classify.7z?dl=0 -O text_classify.7z \
&& 7za e text_classify.7z \
&& rm text_classify.7z

WORKDIR /

CMD [ "/start_bot.sh" ]
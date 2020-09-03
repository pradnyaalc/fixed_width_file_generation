FROM python:3

ADD spec.json /

ADD unittests.py /

ADD fixed_width_gen.py /

RUN apt-get update

RUN apt-get install -y vim

CMD [ "python", "fixed_width_gen.py" ]
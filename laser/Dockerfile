FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN sed -i.bak -e "s%http://archive.ubuntu.com/ubuntu/%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list

ENV TZ Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing && \
    apt-get install -y build-essential wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion \
        vim unzip tzdata language-pack-ja-base && \
    apt-get clean

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

RUN /opt/conda/bin/conda install -y pytorch==1.2.0 torchvision==0.4.0 faiss-gpu==1.6.0 cudatoolkit=10.0 -c pytorch

RUN /opt/conda/bin/pip install Cython==0.29.6 transliterate==1.10.2 jieba==0.39

RUN /opt/conda/bin/pip install setuptools
RUN /opt/conda/bin/pip install ipykernel jedi flake8 autopep8

WORKDIR /root

RUN git clone --depth 1 https://github.com/taku910/mecab && \
    cd mecab/mecab && \
    ./configure --enable-utf8-only && \
    make && \
    make check && \
    make install && \
    /opt/conda/bin/pip install --no-cache-dir mecab-python3 && \
    ldconfig && \
    cd ../mecab-ipadic && \
    ./configure --with-charset=utf8 && \
    make && \
    make install

RUN git clone https://github.com/facebookresearch/LASER.git
##  RUN git checkout 311b25e  # commit hash when tested
ENV LASER /root/LASER
RUN echo "export LASER=$LASER" >> ~/.bashrc

WORKDIR $LASER

#RUN /bin/bash ./install_models.sh
#RUN /bin/bash ./install_external_tools.sh

RUN mkdir -p ./tools-external/mecab/bin && \
    ln -s /usr/local/bin/mecab /root/LASER/tools-external/mecab/bin/mecab

CMD [ "/bin/bash" ]

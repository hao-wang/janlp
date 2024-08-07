FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#?? unidic是unidic-py包（https://github.com/polm/unidic-py），对
# RUN bash -c "python -m unidic download"
# If there is a network error use local copies
# The latter ./dicdir is a must, otherwise only the contents of dicdir 
# will be copied to /app 
COPY dicdir/ ./dicdir/ 

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
  cd /usr/local/bin && \
  ln -s /opt/poetry/bin/poetry && \
  poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

# Set PyPI mirror based on LOC argument
# docker build --build-arg LOC=CN -t image-name .
# ARG LOC=US
# RUN if [ "$LOC" = "CN" ]; then \
#       export POETRY_PYPI_MIRROR_URL=https://mirrors.cloud.tencent.com/pypi/simple/; \
#     fi
# RUN bash -c echo "$POETRY_PYPI_MIRROR_URL"

#ARG INSTALL_DEV=false
#RUN echo "INSTALL_DEV set to: $INSTALL_DEV"
# ??Bash脚本中，[ 条件语句 ]中的空格一定要保留，否则会被当成一整个字符串
# ?? 变量不加引号，变量的值会被分割成单词；加了的话就会被当成一个整体
# ?? 单双引号的区别：双引号内的变量会被解析，单引号就不会（比如echo '$var'就会打印'$var'）
RUN bash -c "poetry install"


COPY ./janlp ./janlp
#?? 设置后可以解决找不到janlp module的问题
ENV PYTHONPATH=/app

COPY ./start-reload.sh .
# Command to run the application
CMD ["fastapi", "run", "janlp/main.py", "--host", "0.0.0.0", "--port", "8000"]
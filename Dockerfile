FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
  cd /usr/local/bin && \
  ln -s /opt/poetry/bin/poetry && \
  poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

# Set PyPI mirror based on LOC argument
# docker build --build-arg LOC=CN -t image-name .
ARG LOC
RUN if [ "$LOC" = "CN" ]; then \
		poetry config repositories.pypi.url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple; \
	fi

ARG INSTALL_DEV=false
RUN echo "INSTALL_DEV set to: $INSTALL_DEV"

# ??Bash脚本中，[ 条件语句 ]中的空格一定要保留，否则会被当成一整个字符串
# ?? 变量不加引号，变量的值会被分割成单词；加了的话就会被当成一个整体
# ?? 单双引号的区别：双引号内的变量会被解析，单引号就不会（比如echo '$var'就会打印'$var'）
RUN bash -c poetry install --no-root


# Copy the application
COPY ./janlp ./janlp

# Command to run the application
CMD ["poetry", "run", "uvicorn", "janlp.main:app", "--host", "0.0.0.0", "--port", "8000"]
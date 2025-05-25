#!/bin/bash

# 确保脚本在错误时退出
set -e

# 检查是否提供了 Docker 用户名
if [ -z "$1" ]; then
    echo "请提供 Docker Hub 用户名"
    echo "使用方法: ./publish.sh <docker_username>"
    exit 1
fi

# 设置 Docker 用户名
export DOCKER_USERNAME=$1

# 确保已登录到 Docker Hub
echo "请确保已经登录到 Docker Hub..."
docker login

# 构建镜像
echo "构建 Docker 镜像..."
docker compose build

# Tag with version
docker tag $DOCKER_USERNAME/janlp:latest $DOCKER_USERNAME/janlp:0.4.3

# 推送镜像
echo "推送镜像到 Docker Hub..."
docker compose push

echo "完成！镜像已推送到 Docker Hub: $DOCKER_USERNAME/janlp:latest" 
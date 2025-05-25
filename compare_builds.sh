#!/bin/bash

echo "=== 对比 Docker 构建方式 ==="
echo

# 设置环境变量
export DOCKER_USERNAME=testuser

echo "1. 直接使用 docker build："
echo "命令: docker build -t janlp-direct:latest ."
echo "生成镜像标签: janlp-direct:latest"
echo

echo "2. 使用 docker compose build："
echo "命令: docker compose build janlp"
echo "配置文件: compose.yml + compose.override.yml"
echo "生成镜像标签: \$DOCKER_USERNAME/janlp:latest (即: $DOCKER_USERNAME/janlp:latest)"
echo

echo "=== 主要区别 ==="
echo

echo "📝 镜像命名："
echo "  - docker build: 需要手动指定 -t 标签，否则只有 IMAGE ID"
echo "  - compose build: 使用 compose.yml 中的 image 字段自动命名"
echo

echo "⚙️  配置管理："
echo "  - docker build: 只使用 Dockerfile"
echo "  - compose build: 结合 Dockerfile + compose.yml + compose.override.yml"
echo

echo "🔧 环境变量："
echo "  - docker build: 需要通过 --build-arg 传递"
echo "  - compose build: 自动读取环境变量（如 \$DOCKER_USERNAME）"
echo

echo "🐳 生产环境差异："
echo "  - docker build: 使用 Dockerfile 中的 CMD"
echo "  - compose build: 可能被 compose.override.yml 中的 command 覆盖"
echo

echo "=== 当前配置分析 ==="

echo "📄 Dockerfile CMD:"
grep "CMD" Dockerfile

echo "📄 compose.override.yml command:"
grep -A1 "command:" compose.override.yml

echo
echo "⚠️  注意: 开发环境和生产环境使用的启动命令可能不同！"
echo "   - 生产环境（Dockerfile）: uvicorn janlp.main:app"
echo "   - 开发环境（override）: uvicorn janlp.main:app --reload" 
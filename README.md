# 🛒 电商自动化测试框架

基于 Pytest + Selenium + Allure + Docker 的自动化测试框架，支持本地开发和 CI/CD 集成。

## 🚀 快速开始

### 前置条件
- Docker & Docker Compose 已安装
- Git 已安装

### 本地运行
```bash
git clone https://github.com/your-username/ecommerce-automation.git
cd ecommerce-automation

# 1. 配置环境变量（可选，不配置则使用默认值）
cp .env.example .env
# 编辑 .env 文件，填入你的测试账号密码

# 2. 启动 Allure 报告服务
docker compose up -d allure

# 3. 运行测试
docker compose run --rm test-runner pytest

# 4. 查看报告
# 浏览器访问 http://localhost:5050
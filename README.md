<div align="center">

<img src="images/2.png" alt="红墨 - 灵感一触即发 让创作从未如此简单" width="600"/>

# 红墨 RedInk

**AI 驱动的小红书图文生成器**

输入一句话，自动生成完整的小红书图文内容

</div>

---

## 目录

- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
  - [Windows 本地开发](#windows-本地开发)
  - [macOS / Linux 本地开发](#macos--linux-本地开发)
- [服务器部署](#服务器部署)
  - [基础部署](#基础部署)
  - [持久化运行](#持久化运行)
  - [Nginx 反向代理](#nginx-反向代理)
- [配置说明](#配置说明)
- [用户认证系统](#用户认证系统)
- [常见问题](#常见问题)

---

## 功能特性

- **智能大纲生成**：输入主题，AI 自动生成多页内容大纲
- **封面页生成**：生成符合小红书风格的精美封面
- **内容页批量生成**：并发生成所有内页（支持高并发模式）
- **文案生成**：自动生成标题、正文和标签
- **历史记录**：保存所有生成记录，支持重新编辑
- **用户认证**：Token 认证系统，支持多用户管理

---

## 技术架构

| 层级 | 技术栈 |
|------|--------|
| **前端** | Vue 3 + TypeScript + Vite + Pinia |
| **后端** | Python 3.11+ + Flask |
| **包管理** | uv (Python) / pnpm (Node.js) |
| **文案 AI** | Google Gemini / OpenAI 兼容接口 |
| **图片 AI** | Google Gemini / OpenAI 兼容接口 |

---

## 快速开始

### 前置要求

- **Python** 3.11+
- **Node.js** 18+
- **pnpm**（`npm install -g pnpm`）
- **uv**（Python 包管理器）

#### 安装 uv

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### Windows 本地开发

#### 方式一：一键启动（推荐）

1. 克隆项目
```powershell
git clone https://github.com/HisMax/RedInk.git
cd RedInk
```

2. 双击运行 `start.bat`

脚本会自动：
- 检查并安装 Python 依赖
- 检查并安装前端依赖
- 启动后端服务（端口 12398）
- 启动前端开发服务器（端口 5173）
- 自动打开浏览器

#### 方式二：手动启动

1. **克隆项目**
```powershell
git clone https://github.com/HisMax/RedInk.git
cd RedInk
```

2. **安装后端依赖**
```powershell
uv sync
```

3. **安装前端依赖**
```powershell
cd frontend
pnpm install
cd ..
```

4. **启动后端**（新开一个终端）
```powershell
uv run python -m backend.app
```
后端运行在：http://localhost:12398

5. **启动前端**（新开一个终端）
```powershell
cd frontend
pnpm dev
```
前端运行在：http://localhost:5173

6. **访问应用**

打开浏览器访问 http://localhost:5173

---

### macOS / Linux 本地开发

#### 方式一：一键启动

```bash
git clone https://github.com/HisMax/RedInk.git
cd RedInk
chmod +x start.sh
./start.sh
```

#### 方式二：手动启动

```bash
# 克隆项目
git clone https://github.com/HisMax/RedInk.git
cd RedInk

# 安装后端依赖
uv sync

# 安装前端依赖
cd frontend && pnpm install && cd ..

# 启动后端（终端 1）
uv run python -m backend.app

# 启动前端（终端 2）
cd frontend && pnpm dev
```

---

## 服务器部署

### 基础部署

以 Ubuntu/Debian 服务器为例：

#### 1. 安装系统依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.11+
sudo apt install python3.11 python3.11-venv -y

# 安装 Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 安装 pnpm
npm install -g pnpm

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

#### 2. 克隆项目

```bash
cd /opt
sudo git clone https://github.com/HisMax/RedInk.git
sudo chown -R $USER:$USER RedInk
cd RedInk
```

#### 3. 安装依赖

```bash
# 后端依赖
uv sync

# 前端依赖并构建
cd frontend
pnpm install
pnpm build
cd ..
```

#### 4. 配置 API

编辑配置文件，填入你的 API Key：

```bash
# 文本生成配置
nano text_providers.yaml

# 图片生成配置
nano image_providers.yaml
```

#### 5. 测试运行

```bash
uv run python -m backend.app
```

访问 `http://服务器IP:12398` 验证是否正常运行。

---

### 持久化运行

#### 方式一：Systemd（推荐）

1. **创建服务文件**

```bash
sudo nano /etc/systemd/system/redink.service
```

写入以下内容：

```ini
[Unit]
Description=RedInk AI Image Generator
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/RedInk
Environment="PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/uv run python -m backend.app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> 注意：将 `/home/ubuntu/.local/bin` 替换为你的 uv 安装路径（运行 `which uv` 查看）

2. **设置目录权限**

```bash
sudo chown -R www-data:www-data /opt/RedInk
```

3. **启动服务**

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start redink

# 设置开机自启
sudo systemctl enable redink

# 查看状态
sudo systemctl status redink

# 查看日志
sudo journalctl -u redink -f
```

4. **常用命令**

```bash
# 停止服务
sudo systemctl stop redink

# 重启服务
sudo systemctl restart redink

# 禁用开机自启
sudo systemctl disable redink
```

#### 方式二：PM2

1. **安装 PM2**

```bash
npm install -g pm2
```

2. **创建启动脚本**

```bash
nano /opt/RedInk/start-pm2.sh
```

写入：

```bash
#!/bin/bash
cd /opt/RedInk
/home/ubuntu/.local/bin/uv run python -m backend.app
```

3. **启动服务**

```bash
chmod +x /opt/RedInk/start-pm2.sh
pm2 start /opt/RedInk/start-pm2.sh --name redink
pm2 save
pm2 startup
```

4. **常用命令**

```bash
pm2 status          # 查看状态
pm2 logs redink     # 查看日志
pm2 restart redink  # 重启
pm2 stop redink     # 停止
```

#### 方式三：Screen（临时方案）

```bash
# 创建 screen 会话
screen -S redink

# 启动服务
cd /opt/RedInk
uv run python -m backend.app

# 按 Ctrl+A 然后按 D 分离会话

# 重新连接会话
screen -r redink
```

---

### Nginx 反向代理

#### 1. 安装 Nginx

```bash
sudo apt install nginx -y
```

#### 2. 创建配置文件

```bash
sudo nano /etc/nginx/sites-available/redink
```

写入：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    # 前端静态文件和 API 代理
    location / {
        proxy_pass http://127.0.0.1:12398;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # SSE 支持（用于流式生成）
        proxy_buffering off;
        proxy_read_timeout 300s;
    }

    # 上传文件大小限制
    client_max_body_size 50M;
}
```

#### 3. 启用配置

```bash
sudo ln -s /etc/nginx/sites-available/redink /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. 配置 HTTPS（可选但推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

---

## 配置说明

### 配置方式

1. **Web 界面配置**（推荐）：启动后在设置页面可视化配置
2. **YAML 文件配置**：直接编辑配置文件

### 文本生成配置

文件：`text_providers.yaml`

```yaml
active_provider: gemini

providers:
  gemini:
    type: google_gemini
    api_key: AIzaxxxxxxxxxxxxxxxxxxxxxxxxx
    model: gemini-2.0-flash

  openai:
    type: openai_compatible
    api_key: sk-xxxxxxxxxxxxxxxxxxxx
    base_url: https://api.openai.com/v1
    model: gpt-4o
```

### 图片生成配置

文件：`image_providers.yaml`

```yaml
active_provider: gemini

providers:
  gemini:
    type: google_genai
    api_key: AIzaxxxxxxxxxxxxxxxxxxxxxxxxx
    model: gemini-3-pro-image-preview
    high_concurrency: false
```

### 高并发模式

- **关闭（默认）**：图片逐张生成，适合有速率限制的 API
- **开启**：图片并行生成（最多 15 张），需要 API 支持高并发

---

## 用户认证系统

### 管理员面板

访问 `/admin` 进入管理面板（默认密码：`redink2025`）

功能：
- 创建/删除用户
- 查看用户 Token
- 查看用户最后使用时间

### 用户登录

1. 管理员在面板创建用户，获取 Token
2. 用户使用 Token 登录前端

### 数据存储

用户数据存储在 `backend/data/users.json`

### 环境变量

```bash
# 管理员密码（可选，默认 redink2025）
export REDINK_ADMIN_PASSWORD=your-secure-password

# Session 密钥（生产环境必须修改）
export REDINK_SECRET_KEY=your-random-secret-key
```

---

## 常见问题

### Q: 端口被占用怎么办？

修改 `backend/config.py` 中的 `PORT` 配置：

```python
PORT = 12399  # 改为其他端口
```

### Q: API 调用失败？

1. 检查 API Key 是否正确
2. 检查网络是否能访问 API 服务
3. 查看后端日志获取详细错误信息

### Q: 图片生成很慢？

1. 检查网络连接
2. 如果 API 支持，可以开启高并发模式
3. GCP 试用账号不建议开启高并发

### Q: 如何备份数据？

需要备份的目录：
- `history/` - 历史记录
- `backend/data/` - 用户数据
- `text_providers.yaml` - 文本配置
- `image_providers.yaml` - 图片配置

---

## 开源协议

本项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 协议

- ✅ 个人使用、学习、研究
- ✅ 分享和修改（需署名、相同协议）
- ❌ 商业用途（需联系作者获取授权）

商业授权联系：histonemax@gmail.com

---

## 联系作者

- **Email**: histonemax@gmail.com
- **微信**: Histone2024
- **GitHub**: [@HisMax](https://github.com/HisMax)

---

**如果这个项目帮到了你，欢迎给个 Star ⭐**

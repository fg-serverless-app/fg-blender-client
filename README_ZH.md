# Blender 渲染任务提交应用

这是一个基于 FastAPI 的 Web 应用，用于提交 Blender 渲染任务到华为云函数工作流。

## 功能特性
- 支持图像和动画渲染
- 可配置输入文件、输出路径、帧范围等参数
- 支持多种渲染引擎（Cycles、Eevee、Workbench）
- 提供丰富的输出格式选项

## 快速开始

### 环境要求
- Python 3.9+
- Docker（可选）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置
1. 将 `config` 目录中的`config.yaml.example` 重命名为 `config.yaml`， 然后在其中配置华为云相关参数：
```yaml
huawei:
  ak: "your-access-key"
  sk: "your-secret-key"
  bucket: "your-bucket-name" // 存放源文件和渲染结果的OBS桶
  endpoint: "your-endpoint" 
  function_urn: "your-function-urn"
```
endpoint是FunctionGraph在所在区域的接入点，可在[此处](https://console.huaweicloud.com/apiexplorer/#/endpoint/FunctionGraph)获取


### 运行应用
```bash
uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
```

或者使用 Docker：
```bash
docker build -t fg-blender-client .
docker run -p 8000:8000 -v /path/to/your/config:/app/config fg-blender-client
```

### 访问应用
打开浏览器访问 `http://localhost:8000`

## 使用说明
1. 在页面表单中填写渲染参数：
   - 选择渲染类型（图像或动画）
   - 输入 Blender 文件在OBS桶中的路径
   - 设置渲染结果在OBS桶中的输出路径和文件名
   - 选择输出格式
   - 配置帧范围、线程数等参数
   - 选择渲染引擎

2. 点击 "Submit Render Task" 提交任务

3. 任务提交成功后，会显示任务ID

## 文件结构
```
├── .gitignore              # Git忽略文件
├── Dockerfile              # Docker 配置文件
├── fastapi_server.py       # FastAPI 主程序
├── index.html              # 前端页面
├── README.md               # 项目说明文档
├── requirements.txt        # Python 依赖
├── config/                 # 配置目录
│   └── config.yaml.example # 配置文件示例
└── static/                 # 静态资源目录
    └── favicon.ico         # 网站图标
```

## 注意事项
- 确保华为云函数工作流已正确配置
- 输入文件路径需与华为云 OBS 存储桶中的路径一致
- 输出路径将用于保存渲染结果
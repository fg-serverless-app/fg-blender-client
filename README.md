# Blender Render Task Submission Application

A FastAPI-based web application for submitting Blender rendering tasks to Huawei Cloud FunctionGraph.

## Features
- Support for both image and animation rendering
- Configurable input files, output paths, frame ranges, etc.
- Multiple rendering engines supported (Cycles, Eevee, Workbench)
- Rich output format options

## Quick Start

### Requirements
- Python 3.9+
- Docker (optional)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
1. Rename `config/config.yaml.example` to `config.yaml` in the config directory, then configure Huawei Cloud parameters:
```yaml
huawei:
  ak: "your-access-key"
  sk: "your-secret-key"
  bucket: "your-bucket-name"  # OBS bucket for source files and render results
  endpoint: "your-endpoint"
  function_urn: "your-function-urn"
```
Endpoint is the FunctionGraph access point for your region, available [here](https://console.huaweicloud.com/apiexplorer/#/endpoint/FunctionGraph)

### Run the Application
```bash
uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
```

Or using Docker:
```bash
docker build -t fg-blender-client .
docker run -p 8000:8000 -v /path/to/your/config:/app/config fg-blender-client
```

### Access the Application
Open your browser to `http://localhost:8000`

## Usage Guide
1. Fill in rendering parameters in the web form:
   - Select render type (Image or Animation)
   - Input Blender file path in OBS bucket
   - Set output path and filename in OBS bucket
   - Select output format
   - Configure frame range, thread count, etc.
   - Choose rendering engine

2. Click "Submit Render Task" to submit

3. Upon successful submission, you'll receive a task ID

## File Structure
```
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration
├── fastapi_server.py       # FastAPI main application
├── index.html              # Frontend page
├── README.md               # Documentation (this file)
├── requirements.txt        # Python dependencies
├── config/                 # Configuration directory
│   └── config.yaml.example # Example config file
└── static/                 # Static assets
    └── favicon.ico         # Website favicon
```

## Important Notes
- Ensure Huawei Cloud FunctionGraph is properly configured
- Input file paths must match actual paths in Huawei OBS bucket
- Output paths will be used to store rendering results
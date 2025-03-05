from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfunctiongraph.v2 import AsyncInvokeFunctionRequest, FunctionGraphClient, AsyncInvokeFunctionResponse
import yaml
import os

app = FastAPI()

# 加载配置文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config/config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

# 从配置文件中获取华为云相关参数
huawei_config = config.get("huawei", {})
ak = huawei_config.get("ak")
sk = huawei_config.get("sk")
bucket = huawei_config.get("bucket")
endpoint = huawei_config.get("endpoint")
function_urn = huawei_config.get("function_urn")

from enum import Enum

class RenderEngine(str, Enum):
    CYCLES = "CYCLES"
    BLENDER_EEVEE = "BLENDER_EEVEE"
    BLENDER_WORKBENCH = "BLENDER_WORKBENCH"

class TaskRequest(BaseModel):
    inputFile: str
    renderType: str
    outputDir: str
    outputFile: str
    outputFormat: str
    startFrame: int
    endFrame: int
    frameStep: int
    threads: int
    engine: RenderEngine
    containerFormat: Optional[str] = "MPEG4"

@app.get("/", response_class=HTMLResponse)
async def get_client():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/task")
async def submit_task(task: TaskRequest):
    try:
        # 使用从配置文件加载的参数
        credentials = BasicCredentials(ak, sk)

        client = FunctionGraphClient.new_builder() \
            .with_credentials(credentials) \
            .with_endpoint(endpoint) \
            .build()
        
        request = AsyncInvokeFunctionRequest()
        request.function_urn = function_urn
        request.body = {
            "bucketName": bucket,
            "renderType": task.renderType,
            "inputFile": task.inputFile,
            "outputDir": task.outputDir,
            "outputFile": task.outputFile,
            "outputFormat": task.outputFormat,
            "startFrame": task.startFrame,
            "endFrame": task.endFrame,
            "frameStep": task.frameStep,
            "threads": task.threads,
            "engine": task.engine,
            "containerFormat": task.containerFormat
        }
        response = client.async_invoke_function(request)
        return {
            "taskId": response.request_id,
        }
    except Exception as e:
        print(f"Error occurred in submit_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from flask import Flask, jsonify, request
import runpod
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)

runpod.api_key = os.environ.get("RUNPOD_API_KEY")
print(os.environ.get("RUNPOD_API_KEY"))


@app.route("/start_server", methods=["GET"])
def start_server():
    try:
        pod_name = str(uuid.uuid4())
        pod = runpod.create_pod(
            name=pod_name,
            image_name="hurairahhere/flux-lora-trainer:latest",  # Your Docker container
            gpu_type_id="NVIDIA A40",
            gpu_count=1,
            container_disk_in_gb=20,
            volume_in_gb=70,
            volume_mount_path="/workspace",
            cloud_type="SECURE",
            ports="5000/http,2121/tcp",
            env={
                # Add any environment variables your container needs
                "WORKSPACE_DIR": "/workspace",
                "PYTHONPATH": "/workspace",
            },
        )
        pod_id = pod["id"]

        return (
            jsonify(
                {
                    "status": True,
                    "response": pod_id,
                    "message": "Pod created successfully",
                    "status_code": 200,
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": False,
                    "message": str(e),
                    "response": None,
                    "status_code": 500,
                }
            ),
            500,
        )


@app.route("/start_generation_server", methods=["GET"])
def start_generation_server():
    try:
        pod_name = f"{str(uuid.uuid4())}_image_generation"
        pod = runpod.create_pod(
            name=pod_name,
            image_name="hurairahhere/flux-image-generation",
            gpu_type_id="NVIDIA A40",
            gpu_count=1,
            container_disk_in_gb=55,
            cloud_type="SECURE",
            ports="5000/http,2121/tcp",
        )
        pod_id = pod["id"]

        return (
            jsonify(
                {
                    "status": True,
                    "response": pod_id,
                    "message": "Pod created successfully",
                    "status_code": 200,
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": False,
                    "message": str(e),
                    "response": None,
                    "status_code": 500,
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

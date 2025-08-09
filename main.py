from flask import Flask, jsonify, request
import runpod
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

runpod.api_key = os.environ.get("RUNPOD_API_KEY")


@app.route("/start_server", methods=["GET"])
def start_server():
    pod = runpod.create_pod(
        name="test_pod",
        image_name="ubuntu:latest",
        gpu_type_id="NVIDIA A40",
        gpu_count=1,
        container_disk_in_gb=40,
        volume_in_gb=10,
        cloud_type="SECURE",
        ports="5000/http,2121/tcp",
        docker_args="sleep infinity",
    )
    pod_id = pod["id"]
    return jsonify(pod_id), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

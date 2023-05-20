STARTUP_SCRIPT = """#!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl start docker
    systemctl enable docker
    docker pull hummer12007/parcs-node
    """
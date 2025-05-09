#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

def build_docker_image(base_image=None, image_name=None, dockerfile=None, build_args=None):
    """
    Build a Docker image with the specified parameters.
    
    Args:
        base_image (str): Base image to use (default: python:3.10-slim)
        image_name (str): Name for the built image (default: website-parse-and-data)
        dockerfile (str): Path to the Dockerfile (default: Dockerfile in current directory)
        build_args (dict): Additional build arguments
    """
    # Default values
    if base_image is None:
        base_image = "python:3.10-slim"
    
    if image_name is None:
        image_name = "website-parse-and-data"
    
    if build_args is None:
        build_args = {}
    
    # Prepare build command
    cmd = ["docker", "build", "-t", image_name]
    
    # Add Dockerfile path if specified
    if dockerfile:
        dockerfile_path = Path(dockerfile)
        if dockerfile_path.exists():
            cmd.extend(["-f", str(dockerfile_path)])
        else:
            print(f"Warning: Dockerfile at {dockerfile_path} not found. Using default.")
    
    # Add build arguments
    build_args["BASE_IMAGE"] = base_image
    for arg_name, arg_value in build_args.items():
        cmd.extend(["--build-arg", f"{arg_name}={arg_value}"])
    
    # Add the build context
    cmd.append(".")
    
    # Execute the build command
    print(f"Building Docker image '{image_name}' based on '{base_image}'...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully built Docker image: {image_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")
        return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Docker image for WebsiteParseAndData")
    parser.add_argument("--base-image", default="python:3.10-slim", 
                        help="Base Docker image (default: python:3.10-slim)")
    parser.add_argument("--image-name", default="website-parse-and-data", 
                        help="Name for the built image (default: website-parse-and-data)")
    parser.add_argument(
        "--dockerfile",
        default=None,
        help=(
            "Path to the Dockerfile (default: Dockerfile in current directory)\n"
            "e.g. --dockerfile ./DockerBuilds/Dockerfile"
            ))
    
    args = parser.parse_args()
    
    # Build the Docker image
    build_docker_image(args.base_image, args.image_name, args.dockerfile)
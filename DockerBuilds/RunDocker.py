#!/usr/bin/env python3
"""
Usage:
python ./DockerBuilds/RunDocker.py
You have to run it from base of the repository in order for the relative path in
COPY command in Dockerfile to work.
"""

import subprocess
import argparse
from pathlib import Path

def parse_config_file():
    """Parse the run_docker_configuration.txt file for port and volume mappings."""
    config = {
        'ports': [],
        'volumes': []
    }
    
    # Get the directory of the current script
    script_dir = Path(__file__).parent
    config_path = script_dir / "run_docker_configuration.txt"
    
    if not config_path.exists():
        return config
    
    with config_path.open('r') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
                
            key, value = line.split('=', 1)
            key = key.strip().upper()
            value = value.strip()
            
            if key.startswith('EXPOSE_PORT'):
                config['ports'].append(value)
            elif key.startswith('MOUNT_PATH'):
                config['volumes'].append(value)
    
    return config

def run_docker_container(image_name=None, env_file=None, shell=True):
    """
    Run a Docker container with the specified parameters.
    
    Args:
        image_name (str): Name of the Docker image to run (default: website-parse-and-data)
        env_file (str): Path to .env file (default: .env in current directory)
        shell (bool): Whether to run a shell in the container (default: True)
    """
    # Default values
    if image_name is None:
        image_name = "website-parse-and-data"
    
    # Get configuration from file
    config = parse_config_file()
    
    # Use port mappings from config file or default
    if config['ports']:
        port_mappings = config['ports']
    else:
        port_mappings = ["8501:8501"]
    
    # Use volume mappings from config file or default
    if config['volumes']:
        volume_mappings = config['volumes']
    else:
        volume_mappings = [f"{Path.cwd()}:/app"]
    
    # Prepare run command
    cmd = ["docker", "run", "--rm"]
    
    # Add port mappings
    for port_map in port_mappings:
        cmd.extend(["-p", port_map])
    
    # Add volume mappings
    for volume_map in volume_mappings:
        cmd.extend(["-v", volume_map])
    
    # Add environment file if specified
    if env_file:
        env_path = Path(env_file)
        if env_path.exists():
            cmd.extend(["--env-file", str(env_path)])
        else:
            print(f"Warning: Environment file {env_file} not found.")
    
    # Add interactive mode with TTY
    cmd.extend(["-it"])
    
    # Add the image name
    cmd.append(image_name)
    
    # Add shell command if requested
    if shell:
        cmd.append("/bin/bash")
    
    # Execute the run command
    print(f"Running Docker container from image '{image_name}'...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker container: {e}")
        return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Docker container for WebsiteParseAndData")
    parser.add_argument("--image-name", default="website-parse-and-data", 
                        help="Name of the Docker image to run (default: website-parse-and-data)")
    parser.add_argument("--env-file", default=".env", 
                        help="Path to .env file (default: .env in current directory)")
    parser.add_argument("--no-shell", action="store_true",
                        help="Don't run a shell in the container (use default CMD)")
    
    args = parser.parse_args()
    
    # Run the Docker container
    run_docker_container(
        args.image_name,
        args.env_file,
        not args.no_shell  # Invert the flag - by default we want shell=True
    )
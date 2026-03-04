import os
import shutil
import subprocess


def run_analysis(image, output_dir):
    print(f"Generating live report for {image} in {output_dir}...")
    
    # Ensure directory exists but run will overwrite contents
    os.makedirs(output_dir, exist_ok=True)
    
    # Use pipenv run regis-cli to ensure we're using the project's dependencies
    cmd = [
        "pipenv", "run", "regis-cli", "analyze", image,
        "-s", "-D", output_dir
    ]
    subprocess.run(cmd, check=True)

def main():
    # Execute from project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    examples_dir = "docs/modules/ROOT/assets/attachments/examples"
    
    # 1. Alpine Linux
    alpine_dir = os.path.join(examples_dir, "alpine")
    run_analysis("alpine:latest", alpine_dir)
    
    # 2. Regis CLI (always analyze latest)
    regis_dir = os.path.join(examples_dir, "regis-cli")
    run_analysis("ghcr.io/trivoallan/regis-cli:latest", regis_dir)
    
    # Clean up the old regis-cli-0.5 directory if it exists
    old_regis_dir = os.path.join(examples_dir, "regis-cli-0.5")
    if os.path.exists(old_regis_dir):
        print(f"Removing old examples directory {old_regis_dir}...")
        shutil.rmtree(old_regis_dir)

if __name__ == "__main__":
    main()

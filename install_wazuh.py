import os
import subprocess

def run_command(command, description):
    """Runs a shell command with a description."""
    print(f"\n[INFO] {description}...")
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode != 0:
        print(f"[ERROR] {description} failed: {process.stderr}")
        exit(1)
    print(f"[INFO] {description} completed successfully.")


def install_docker():
    """Installs Docker."""
    run_command(
        "sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common",
        "Installing prerequisites for Docker",
    )

    run_command(
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
        "Adding Docker GPG key",
    )

    run_command(
        "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
        "Adding Docker repository",
    )

    run_command(
        "sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io",
        "Installing Docker",
    )

    run_command("sudo systemctl enable --now docker", "Enabling Docker service")


def install_docker_compose():
    """Installs Docker Compose."""
    run_command(
        "sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
        "Downloading Docker Compose",
    )
    run_command("sudo chmod +x /usr/local/bin/docker-compose", "Making Docker Compose executable")


def install_wazuh(password):
    """Installs and configures Wazuh."""
    run_command(
        "curl -sO https://packages.wazuh.com/4.4/docker/docker-compose.yml",
        "Downloading Wazuh Docker Compose file",
    )

    run_command("sudo docker-compose -f docker-compose.yml up -d", "Starting Wazuh containers")

    print("\n[INFO] Waiting for Wazuh Manager to initialize...")
    subprocess.run("sleep 60", shell=True)  # Allow time for the Wazuh manager to initialize

    run_command(
        f"sudo docker exec wazuh /var/ossec/framework/python/bin/python3 /var/ossec/api/scripts/configuration/user_password_set.py admin {password}",
        "Setting Wazuh admin password",
    )


def main():
    print("Welcome to the Docker & Wazuh installation script!")

    password = input("Please enter the password for the Wazuh admin user: ")
    if not password:
        print("[ERROR] Password cannot be empty.")
        exit(1)

    install_docker()
    install_docker_compose()
    install_wazuh(password)

    print("\n[INFO] Wazuh installation and configuration complete!")
    print("You can access Wazuh at https://<your_server_ip>:5601 with the username 'admin' and your configured password.")


if __name__ == "__main__":
    main()

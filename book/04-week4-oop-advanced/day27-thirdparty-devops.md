# Day 27 — Third-Party Libraries for DevOps

Keywords: `requests`, `pyyaml`, `boto3`, `docker`, `paramiko`, `rich`, `click`, `typer`, `pytest`

## Keywords + Methods

### HTTP & Configuration Management
- **Type:** REST APIs and YAML configuration
- **Methods:** `requests.get`, `yaml.safe_load`, `yaml.dump`
- **Example:**
  ```python
  import requests
  import yaml

  def fetch_metrics(host: str):
      resp = requests.get(f"http://{host}:9090/metrics", timeout=5)
      return resp.json() if resp.status_code == 200 else {}

  def load_config(path: str):
      with open(path) as f:
          return yaml.safe_load(f)

  def save_config(path: str, config):
      with open(path, 'w') as f:
          yaml.dump(config, f, default_flow_style=False)

  config = load_config("infra.yaml")
  metrics = fetch_metrics(config["host"])
  save_config("infra-backup.yaml", config)
  ```

### Cloud and Container Automation
- **Type:** AWS SDK and Docker SDK
- **Methods:** `boto3.client`, `boto3.resource`, `docker.from_env`, `docker.models.containers`
- **Example:**
  ```python
  import boto3
  import docker

  # Start EC2 instance via AWS SDK
  ec2 = boto3.client('ec2')
  response = ec2.run_instances(
      ImageId='ami-0c55b159cbfafe1f0',
      InstanceType='t2.micro',
      MinCount=1,
      MaxCount=1,
  )
  instance_id = response['Instances'][0]['InstanceId']

  # Run container via Docker SDK
  client = docker.from_env()
  container = client.containers.run(
      'nginx:latest',
      name='nginx-proxy',
      ports={'80/tcp': 8080},
      detach=True
  )
  print(f"Container ID: {container.id}")
  ```

### Remote Execution & CLI Enhancement
- **Type:** SSH and advanced terminal UI
- **Methods:** `paramiko.SSHClient`, `rich.console`, `click.command`, `typer.Typer`
- **Example:**
  ```python
  import paramiko
  from rich.console import Console
  from click import command

  console = Console()

  def ssh_run(host: str, cmd: str):
      client = paramiko.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(host, username='ubuntu')
      stdin, stdout, stderr = client.exec_command(cmd)
      output = stdout.read().decode()
      client.close()
      return output

  @command()
  def deploy(app: str):
      console.print(f"Deploying {app} to remote server...")
      output = ssh_run("prod-server", f"git pull origin {app}")
      console.print(output)

  deploy()
  ```

### Testing
- **Type:** Pytest fixtures and assertions
- **Methods:** `@pytest.fixture`, `pytest.raises`
- **Example:**
  ```python
  import pytest

  @pytest.fixture
  def temp_config():
      import tempfile, yaml
      with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as f:
          yaml.dump({'host': 'test.local'}, f)
          yield f.name

  def test_load_config(temp_config):
      import yaml
      with open(temp_config) as f:
          cfg = yaml.safe_load(f)
          assert cfg['host'] == 'test.local'
  ```

## DevOps Context: Building Automation Toolkit
Third-party packages extend Python's native capabilities to cover real-world DevOps tasks: infrastructure monitoring, cloud provisioning, CI/CD, and human-friendly CLI/UIs.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day27 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day27 -v` — see `tests/day27/test_day27.py`

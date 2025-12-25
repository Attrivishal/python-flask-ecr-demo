# Python Flask ECR Demo

A minimal Python Flask application packaged with Docker and pushed to AWS Elastic Container Registry (ECR).

## Table of contents

- [Project](#project)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Local development](#local-development)
- [Docker](#docker)
- [Push to AWS ECR](#push-to-aws-ecr)
- [Environment variables](#environment-variables)
- [Health & testing](#health--testing)
- [CI/CD ideas](#cicd-ideas)
- [Contributing](#contributing)
- [License](#license)

## Project

This repository contains a simple Python Flask application intended to be built into a Docker image and published to AWS ECR. The app is deliberately small so it can be used as a demo or starter for containerizing and deploying Flask apps.

## Tech stack

- Python 3.8+ (compatible with 3.9, 3.10)
- Flask
- Docker
- AWS ECR for container registry

## Prerequisites

- Python 3.8+ and pip (for local development)
- Docker (to build and run containers)
- AWS CLI v2 configured with credentials that can access/create ECR repositories
- IAM permissions to push/pull ECR images (AmazonEC2ContainerRegistryFullAccess or equivalent)

## Local development

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows (PowerShell)
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask app locally:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

Or run directly with Python:

```bash
python app.py
```

Visit http://localhost:5000 to see the app.

## Docker

Build the Docker image locally:

```bash
docker build -t python-flask-ecr-demo:latest .
```

Run the image locally:

```bash
docker run --rm -p 5000:5000 python-flask-ecr-demo:latest
```

## Push to AWS ECR

Steps to push the Docker image to ECR (replace placeholders):

1. Create the ECR repository (if it doesn't exist):

```bash
aws ecr create-repository --repository-name python-flask-ecr-demo --region <aws-region>
```

2. Authenticate Docker to ECR:

```bash
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws-region>.amazonaws.com
```

3. Tag the local image for ECR:

```bash
docker tag python-flask-ecr-demo:latest <aws_account_id>.dkr.ecr.<aws-region>.amazonaws.com/python-flask-ecr-demo:latest
```

4. Push the image:

```bash
docker push <aws_account_id>.dkr.ecr.<aws-region>.amazonaws.com/python-flask-ecr-demo:latest
```

Notes:
- Replace `<aws_account_id>` and `<aws-region>` with your AWS account ID and region (e.g. us-east-1).
- Ensure your AWS credentials (profile or environment variables) have permission to create repositories and push images.

## Environment variables

If your app reads environment variables, document them here. Example:

- FLASK_ENV: development | production
- PORT: Port application listens on (default: 5000)

Add any app-specific variables and their defaults/meaning.

## Health & testing

- The app exposes a basic endpoint at `/` (or whatever endpoint the repo contains). Add health checks for production (e.g. `/health`).
- Use a local pytest setup if tests are added in the future.

## CI/CD ideas

- Use GitHub Actions to build the Docker image and push to ECR on push to main or when creating releases.
- Typical workflow steps:
  - Checkout code
  - Set up Python and install deps (for unit tests / lint)
  - Build Docker image
  - Authenticate to ECR
  - Tag & push image

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch
3. Open a pull request with a clear description

Please add tests for significant changes.

## License

This project currently has no license specified. Add a LICENSE file or update this README with the chosen license.

---

If you want, I can also:
- Add a basic GitHub Actions workflow to build and push the image to ECR
- Add a LICENSE file (MIT/Apache-2.0/etc.)
- Customize README with exact commands for your AWS account (if you provide account ID and preferred region)

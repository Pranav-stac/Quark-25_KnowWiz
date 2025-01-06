# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- AWS account with ECR and ECS configured
- Domain name and SSL certificates
- PostgreSQL database instance

## Local Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the application at http://localhost:8501

## Production Deployment

1. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your production values
```

2. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Initialize the database:
```bash
docker-compose -f docker-compose.prod.yml exec web alembic upgrade head
```

## AWS Deployment

1. Create ECR repository:
```bash
aws ecr create-repository --repository-name health-monitor
```

2. Configure ECS cluster and service:
```bash
aws ecs create-cluster --cluster-name health-monitor
# Follow AWS ECS setup guide for service configuration
```

3. Set up GitHub Secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- Other API keys and environment variables

4. Push to main branch to trigger deployment

## Monitoring

- Access logs: `docker-compose logs -f`
- Monitor ECS metrics in AWS CloudWatch
- Check application health at `/health`

## Backup

1. Database backup:
```bash
docker-compose exec db pg_dump -U postgres health_monitor > backup.sql
```

2. Restore from backup:
```bash
cat backup.sql | docker-compose exec -T db psql -U postgres health_monitor
``` 
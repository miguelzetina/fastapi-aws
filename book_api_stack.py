from constructs import Construct
from aws_cdk import (
    aws_ec2 as _ec2, aws_ecs as _ecs, aws_ecr as _ecr,
    aws_ecs_patterns as _ecs_patterns
)
from aws_cdk.core import Stack
from src.config import settings


class ContainerizedGraphQLAPIStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        api_name = settings.APP_NAME.lower().replace(' ', '-')
        api_resource_prefix = f"{api_name}-{settings.ENV_TYPE.lower()}"
        image_name = settings.APP_NAME.lower().replace(' ', '')

        # Create a VPC
        vpc = _ec2.Vpc(self, 'BookAPIVPC', max_azs=3)

        cluster = _ecs.Cluster(self, f"{api_resource_prefix}-cluster",
                              vpc=vpc)

        # Environment variables required by container
        env_var = {
            "DB_URL": settings.DB_URL,
            "DB_NAME": settings.DB_NAME,
            "HOST": settings.HOST,
            "PORT": str(settings.PORT)
        }

        # User the bookapi image from private book-api ECR repository
        repo = _ecr.Repository.from_repository_name(self, f"{image_name}",
                                                    repository_name=f"api_name")

        image = _ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=_ecs.EcrImage.from_ecr_repository(repository=repo),
            container_name=api_resource_prefix,
            container_port=settings.PORT,
            environment=env_var  # required or else service will crash
        )

        _ecs_patterns.ApplicationLoadBalancedFargateService(
            self, id=api_resource_prefix, service_name=api_resource_prefix,
            cluster=cluster, cpu=256, desired_count=1,
            task_image_options=image, memory_limit_mib=512,
            public_load_balancer=True
        )



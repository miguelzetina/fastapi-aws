from constructs import Construct
from aws_cdk import (
    aws_certificatemanager as _cert_manager,
    aws_ec2 as _ec2,
    aws_ecr as _ecr,
    aws_ecs as _ecs,
    aws_ecs_patterns as _ecs_patterns,
    aws_route53 as _route53,
    aws_route53_targets as _targets
)
from aws_cdk.core import Duration, Stack
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
                                                    repository_name=f"{api_name}")

        image = _ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=_ecs.EcrImage.from_ecr_repository(repository=repo),
            container_name=api_resource_prefix,
            container_port=settings.PORT,
            environment=env_var  # required or else service will crash
        )

        hosted_zone = _route53.HostedZone.from_lookup(
            self,
            f"{image_name}-hosted-zone",
            domain_name=settings.DOMAIN_NAME
        )

        # Create certificate for the above domain
        certificate = _cert_manager.Certificate(
            self,
            f"{image_name}-certificate",
            domain_name=f"*.{settings.DOMAIN_NAME}",
            validation=_cert_manager.CertificateValidation.from_dns(hosted_zone)
        )

        service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            id=api_resource_prefix,
            service_name=api_resource_prefix,
            cluster=cluster,
            cpu=256,
            desired_count=1,
            task_image_options=image,
            memory_limit_mib=512,
            public_load_balancer=True,
            certificate=certificate
        )

        record_target = _route53.RecordTarget.from_alias(
            _targets.LoadBalancerTarget(service.load_balancer)
        )

        _route53.ARecord(
            self,
            f"{image_name}-dns-record",
            zone=hosted_zone,
            record_name='book-api',
            ttl=Duration.minutes(1),
            target=record_target
        )


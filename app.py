from aws_cdk import core as cdk

from book_api_stack import ContainerizedGraphQLAPIStack
from src.config import settings


app = cdk.App()

ContainerizedGraphQLAPIStack(
    app,
    "ContainerizedGraphQLAPIStack",
    env=cdk.Environment(account=settings.AWS_ACCOUNT, region=settings.AWS_REGION),
)
app.synth()

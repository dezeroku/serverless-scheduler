from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import DDB, Redshift
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.generic.compute import Rack
from diagrams.programming.framework import React

with Diagram("High Level Overview", show=False, outformat=["png"]):
    ui_source = React("Web UI")
    source = APIGateway("Items")

    with Cluster("Items endpoints"):
        items_endpoints = [
            Lambda("create"),
            Lambda("update"),
            Lambda("delete"),
            Lambda("get"),
        ]

    items_db = DDB("Items")
    item_changes_sqs = SQS("FIFO item-changes")
    item_changes_lambda = Lambda("ScheduleController")

    with Cluster("Scheduled Jobs"):
        scheduled_jobs_eventbridge = [
            Eventbridge("ScheduledJob1"),
            Eventbridge("ScheduledJob2"),
            Eventbridge("ScheduledJob3"),
        ]

    distribution_sns = SNS("Distribution")
    # potential_outside_source = Rack("Outside triggerer")

    with Cluster("Job Handlers"):
        job_handlers_sqs = [SQS("JobType1"), SQS("JobType2"), SQS("JobType3")]

        job_handlers_lambdas = [
            Lambda("JobType1Handler"),
            Lambda("JobType2Handler"),
            Lambda("JobType3Handler"),
        ]

    output = SQS("Output")
    mail_sender = SES("SES")

    ui_source >> source >> items_endpoints >> items_db >> item_changes_sqs
    (
        item_changes_sqs
        >> item_changes_lambda
        >> scheduled_jobs_eventbridge
        >> distribution_sns
    )
    distribution_sns >> job_handlers_sqs
    for sqs, handler in zip(job_handlers_sqs, job_handlers_lambdas):
        sqs >> handler
        handler >> output

    output >> mail_sender
    # potential_outside_source >> distribution_sns

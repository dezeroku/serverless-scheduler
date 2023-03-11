from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DDB
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.programming.framework import React
from diagrams.programming.language import Python

with Diagram("High Level Overview", show=False, outformat=["png"]):
    with Cluster("Main Project Scope"):
        with Cluster("front"):
            ui_source = React("Web UI")

        with Cluster("common"):
            common_models = Python("Payload Models")

        with Cluster("items"):
            cognito = Cognito("Users")
            source = APIGateway("Items")

            with Cluster("Items endpoints"):
                items_endpoints = [
                    Lambda("create"),
                    Lambda("update"),
                    Lambda("delete"),
                    Lambda("get"),
                    Lambda("job_types"),
                ]

            items_db = DDB("Items")
            items_db_stream_lambda = Lambda("ChangeAnalyzer")
            item_changes_sqs = SQS("FIFO ScheduleQueue")

        with Cluster("schedulers"):
            item_changes_lambda = Lambda("ScheduleController")
            with Cluster("Managed Schedulers"):
                scheduled_jobs_eventbridge = [
                    Eventbridge("Scheduler1"),
                    Eventbridge("Scheduler2"),
                    Eventbridge("Scheduler3"),
                ]

        with Cluster("distribution"):
            distribution_sns = SNS("Distribution")

    with Cluster("serverless-scheduler-html-checker"):
        html_handler_sqs = [SQS("html_monitor_job")]

        html_handler_lambda = Lambda("HTMLMonitorJobHandler")

        html_data_bucket = S3("TempDataBucket")

    with Cluster("Custom Job Handlers"):
        job_handlers_sqs = [SQS("JobType1"), SQS("JobType2"), SQS("JobType3")]

        job_handlers_lambdas = [
            Lambda("JobType1Handler"),
            Lambda("JobType2Handler"),
            Lambda("JobType3Handler"),
        ]

    output = SQS("Output")
    mail_sender = SES("SES")
    mail_sender_html = SES("SES")

    ui_edge = Edge(label="ScheduledJob")

    ui_source >> Edge() >> cognito
    source >> Edge() >> cognito
    (
        ui_source
        >> ui_edge
        << source
        >> items_endpoints
        >> items_db
        >> Edge(label="DDB Stream")
        >> items_db_stream_lambda
    )
    items_db_stream_lambda >> item_changes_sqs
    (
        item_changes_sqs
        >> Edge(label="SchedulerChangeEvent")
        >> item_changes_lambda
        >> scheduled_jobs_eventbridge
    )

    for index, scheduler in enumerate(scheduled_jobs_eventbridge):
        scheduler >> Edge(label=f"JobType{index + 1}") >> distribution_sns

    for index, handler in enumerate(job_handlers_sqs):
        distribution_sns >> Edge(label=f"job_type = JobType{index + 1}") >> handler

    for sqs, handler in zip(job_handlers_sqs, job_handlers_lambdas):
        sqs >> handler
    #    handler >> output
    job_handlers_lambdas[0] >> mail_sender
    job_handlers_lambdas[1] >> output

    (
        distribution_sns
        >> Edge(label=f"job_type = html_monitor_job")
        >> html_handler_sqs
        >> html_handler_lambda
        >> mail_sender_html
    )
    html_handler_lambda >> Edge() << html_data_bucket
    # output >> mail_sender
    # potential_outside_source = Python("Custom triggerer")
    # potential_outside_source >> distribution_sns

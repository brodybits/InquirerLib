# NOTE: Following example requires boto3 package.
import os

import boto3

from InquirerLib.InquirerPy import inquirer
from InquirerLib.InquirerPy.exceptions import InvalidArgument
from InquirerLib.InquirerPy.validator import PathValidator

client = boto3.client("s3")
os.environ["INQUIRERPY_VI_MODE"] = "true"


def get_bucket(_):
    return [bucket["Name"] for bucket in client.list_buckets()["Buckets"]]


def walk_s3_bucket(bucket):
    response = []
    paginator = client.get_paginator("list_objects")
    for result in paginator.paginate(Bucket=bucket):
        for file in result["Contents"]:
            response.append(file["Key"])
    return response


try:
    action = inquirer.select(
        message="Select an S3 action:", choices=["Upload", "Download"]
    ).execute()

    if action == "Upload":
        file_to_upload = inquirer.filepath(
            message="Enter the filepath to upload:",
            validate=PathValidator(),
            only_files=True,
        ).execute()
        bucket = inquirer.fuzzy(
            message="Select a bucket:", choices=get_bucket, spinner_enable=True
        ).execute()
    else:
        bucket = inquirer.fuzzy(
            message="Select a bucket:", choices=get_bucket, spinner_enable=True
        ).execute()
        file_to_download = inquirer.fuzzy(
            message="Select files to download:",
            choices=lambda _: walk_s3_bucket(bucket),
            multiselect=True,
            spinner_enable=True,
        ).execute()
        destination = inquirer.filepath(
            message="Enter destination folder:",
            only_directories=True,
            validate=PathValidator(),
        ).execute()

    confirm = inquirer.confirm(message="Confirm?").execute()
except InvalidArgument:
    print("No available choices")

# Download or Upload the file based on result ...

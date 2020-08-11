import boto3, botocore
from app import app  ## starting from the root directory, which is curriculum-nextagram-template
import braintree


s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config["S3_KEY"],
   aws_secret_access_key=app.config["S3_SECRET"]
)

def upload_file_s3_retype(file,username, acl="public-read"):
    try:
        s3_upload_fileobj(file,
                            app.config.get("S3_BUCKET"),
                            f"{username}/{file.filename}",
                            ExtraArgs={
                                "ACL":acl,
                                "ContentType":file.content_type
                            })

    except Exception as e:
        print("Something happened------>",e)
        return e

    return f"{username}/{file.filename}"





def upload_file_s3(file, username, acl="public-read"): #username is for folder creation , jw's gist don't have it
    try:
        s3.upload_fileobj(
            file,  # our image file object
            app.config.get("S3_BUCKET"), # the bucket that we want to uplaod to
            "{}/{}".format(username, file.filename), # pathway  to upload to s3 bucket
            ExtraArgs={
                "ACL": acl, #without setting ACL to public-read, only i can view it when i am logged into my aws.
                "ContentType": file.content_type   # it stop us from downloading it when i key in the url in the browser.
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}/{}".format(username, file.filename)



gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config.get("BRAINTREE_MERCHANT_ID"),
        public_key=app.config.get("BRAINTREE_PUBLIC_KEY"),
        private_key=app.config.get("BRAINTREE_PRIVATE_KEY")
    )
)
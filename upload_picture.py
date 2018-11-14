# Imports
import cv2
import base64
import sys
import boto3

from botocore.exceptions import ClientError
from boto.s3.connection import S3Connection

# Encode image
with open(str(sys.argv[1]), "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# Specify bucket and file details
bucket1 = 'faceAnalyzer'
bucket2 = 'faceRecords'
file_name = encoded_string

# Create a Boto3 session for other clients to use
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
)

# Function to return how many times the script has been ran
def get_var_value(filename="varstore.dat"):
    with open(filename, "a+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

# Update a counter with how many times the script has been ran, and add that to the key    
counter = get_var_value(filename="varstore.dat")
key1 = 'face' + counter

# Specify lambda message contents and details
CHARSET = "UTF-8"
SENDER = "rwchinn1459@eagle.fgcu.edu"
RECIPIENT = "hjbedwell7492@eagle.fgcu.edu"
CONFIGURATION_SET = "ConfigSet"
SUBJECT = "Possible Security Threat Detected"
BODY_TEXT = ("To whom it may concern,\r\n"
             "We may have picked up suspicious activity on the premises near your device. To secure your belongings, "
             "we would recommend taking appropriate actions in order to ensure this individual is someone you know."
)

BODY_HTML = """<html>
<head></head>
<body>
  <img src="https://s3.amazonaws.com/faceAnalyzer/""" + key1 + """".jpg" width="1280" height="720">
</body>
</html>
"""

# Initiate the cascade classifier to the xml file specified below
faceCascade = cv2.CascadeClassifier()
faceCascade.load('haarcascade_frontalface_default.xml')
image = cv2.imread(encoded_string)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

# If there are greater than 0 faces found, upload the image to Amazon S3
if faces > 0:
    s3 = session.client('s3')
    s3.upload_file(file_name, bucket1, key1)

# Function to compare faces on an image to image basis
def compare_faces(bucket1, key1, bucket2, key2, threshold = 80, region = "eu-east-2"):
    rekognition = session.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage = {
            "S3Object": {
                "Bucket": bucket1,
                "Name": key1,
            }
        },
        TargetImage = {
            "S3Object": {
                "Bucket": bucket2,
                "Name": key2,
            }
        },
        SimilarityThreshold = threshold,
    )
    return response['SourceImageFace'], response['FaceMatches']

# Create a seperate S3 connection, which will be used to iterate through faceRecords
conn = S3Connection('ACCESS_KEY','SECRET_KEY')
bucket = conn.get_bucket('faceRecords')

# Iterate through the collection to compare the passed in photo with those that have been 
for key in bucket.list(): # pre-populated
    key2 = key
    source_face, matches = compare_faces(bucket1, key1, bucket2, key2)

if matches == 0: # Trigger a lambda function if no matches are found, for the purpose of warning 
    client = session.client('ses', region_name = "us-east-2") # the user
    
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

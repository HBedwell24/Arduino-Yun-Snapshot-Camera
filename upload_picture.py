import cv2
import boto3

from botocore.exceptions import ClientError
from boto.s3.connection import S3Connection

with open(str(sys.argv[1]), "rb") as image_file:
  encoded_string = base64.b64encode(image_file.read())

bucket = 'faceAnalyzer'
bucket_target = 'faceRecords'
file_name = encoded_string

counter = get_var_value()
key = 'face' + counter

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
  <img src="https://s3.amazonaws.com/faceAnalyzer/face.jpg" width="1280" height="720">
</body>
</html>
            """			
s3 = boto3.client('s3')
image = cv2.imread(encoded_string)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier(???)

faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

if faces != 0:
	s3.upload_file(file_name, bucket, key)
}

def get_var_value(filename="varstore.dat"):
    with open(filename, "a+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

def compare_faces(bucket, key, bucket_target, key_target, threshold = 80, region = "eu-east-2"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage = {
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        TargetImage = {
            "S3Object": {
                "Bucket": bucket_target,
                "Name": key_target,
            }
        },
        SimilarityThreshold = threshold,
    )
    return response['SourceImageFace'], response['FaceMatches']

conn = S3Connection('access-key','secret-access-key')
bucket = conn.get_bucket('faceRecords')

for key in bucket.list():
	key_target = key
	source_face, matches = compare_faces(bucket, key, bucket_target, key_target)

if matches = 0:
	client = boto3.client('ses',region_name = "us-east-2")
	
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
}

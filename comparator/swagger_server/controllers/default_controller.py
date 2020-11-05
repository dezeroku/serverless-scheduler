import connexion
import six

from flask import jsonify

import base64
import uuid

# Image diff calculation
from skimage.metrics import structural_similarity
import imutils
import cv2

from swagger_server.models.compare_request import CompareRequest  # noqa: E501
from swagger_server.models.compare_response import CompareResponse  # noqa: E501
from swagger_server import util

def _mark_diff_images(first, second, output):
    # Load images.
    im1 = cv2.imread(first)
    im2 = cv2.imread(second)

    # Convert to grayscale.
    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Compute similarity index.
    (score, diff) = structural_similarity(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    print("Image similarity: {}".format(score))

    # Find contours of the differences.
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV |
                           cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Draw rectangles that indicate differences.
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(im1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Write files.
    cv2.imwrite(output, im2)

    return score



def compare(body=None):  # noqa: E501
    """returns score and picture diff of provided images

     # noqa: E501

    :param body: data
    :type body: dict | bytes

    :rtype: CompareResponse
    """
    if connexion.request.is_json:
        body = CompareRequest.from_dict(connexion.request.get_json())  # noqa: E501

    first = 'first' + str(uuid.uuid4()) + ".png"
    second = 'second' + str(uuid.uuid4()) + ".png"


    decoded = base64.b64decode(body.first)
    with open(first, 'wb') as f:
        f.write(decoded)
        f.close()

    decoded = base64.b64decode(body.second)
    with open(second, 'wb') as f:
        f.write(decoded)


    diff = 'diff' + str(uuid.uuid4()) + ".png"
    score = _mark_diff_images(first, second, diff)

    with open(diff, 'rb') as f:
            data = f.read()
            f.close()
    encoded = base64.b64encode(data).decode()

    response = {"score": score, "diff_image": encoded}

    return jsonify(response)


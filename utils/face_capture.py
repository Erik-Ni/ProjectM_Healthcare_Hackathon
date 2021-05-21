import cv2
import pandas as pd
import numpy as np
from .landmarks import firstmodify, ifoverborder, finalmodify


def deep_convert(config, frame):
	net = cv2.dnn.readNetFromCaffe(config['PROTOTXT_DIRECTORY'], config['CAFFEMODEL_DIRECTORY'])
	left, up, right, bottom = -1, -1, -1, -1
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
	net.setInput(blob)
	detections = net.forward()

	height, width, channels = frame.shape

	line_thick = round(height / 120)

	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.75:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			len = detections[0, 0, i, 3:7]

			if len[3] < 1:
				(startX, startY, endX, endY) = box.astype("int")
				startX = max(startX, 0)
				startY = max(startY, 0)

				left, right, up, bottom = firstmodify(startX, endX, startY, endY)
				left, right, up, bottom = ifoverborder(left, right, up, bottom, w, h)
				left, right, up, bottom = finalmodify(left, right, up, bottom)

				width = (right - left)
				height = (bottom - up)
				f = 0.3

				left += int(width * f / 2)
				right -= int(width * f / 2)
				up += int(height * f / 2)
				bottom -= int(height * f / 2)

				roi = frame[up:bottom, left:right]

				cv2.rectangle(frame, (left, up), (right, bottom), config['COLOR'], thickness=config['RECTANGLE_THICKNESS'])

				return True, roi

	return False, None

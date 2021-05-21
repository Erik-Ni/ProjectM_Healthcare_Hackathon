from .face_capture import deep_convert
import cv2
import numpy as np

import json
import requests

import threading
import queue


que = queue.Queue()


def storeInQueue(f):
	def wrapper(*args):
		que.put(f(*args))
	return wrapper


@storeInQueue
def get_tf_response(config, roi, model_mode):
	max_idx = 5
	max_percentage = 100
	api = config['EMOTION_API']

	push_data_json = wrap_data(roi)

	if model_mode == 0:
		max_idx, max_percentage = 5, 100
		api = config['MOOD_API']

	try:
		request = requests.post(api, data=push_data_json, timeout=config['REQUEST_TIMEOUT']).text
		response = json.loads(request)
		if 'predictions' in response:
			predictions = response['predictions'][0]
			max_idx = np.argmax(predictions)
			max_percentage = round(predictions[max_idx] * 100, 2)
		else:
			print(emotion_response)
		return max_idx, max_percentage

	except:
		print('Catch error when requesting to apis')
		return max_idx, max_percentage


def wrap_data(roi):
	roi = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_AREA)
	output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	output = output.reshape(1, 200, 200) / 255.
	img_info = output.tolist()
	data = {'instances': img_info}
	push_data_json = json.dumps(data, sort_keys=True, separators=(',', ': '))
	return push_data_json


def video_access(config, video_dir):
	num_frames = 0
	max_emotion_idx, max_mood_idx = 5, 1
	max_emotion_percentage, max_mood_percentage = 100, 100
	result = 'Emotion: {} ({}%) - Mood: {} ({}%)'

	cap = cv2.VideoCapture(video_dir)

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	size = (frame_width, frame_height)

	threads = []

	if not (cap.isOpened()):
		print('Could not open video device')
	else:
		ret, frame = cap.read()

		while ret:
			found_face, roi = deep_convert(config, frame)

			if found_face:
				if num_frames % config['FRAMES_PER_REQUEST'] == 0:
					mode = (num_frames / config['FRAMES_PER_REQUEST'] - 1) % 2
					if len(threads) > 0:
						threads[0].join()
						threads.pop(0)
						max_idx, max_percentage = que.get()

						if mode == 0:
							max_emotion_idx, max_emotion_percentage = max_idx, max_percentage
						else:
							max_mood_idx, max_mood_percentage = max_idx, max_percentage

					t = threading.Thread(target=get_tf_response, args=(config, roi, mode))
					t.setDaemon(True)
					threads.append(t)
					t.start()

				cv2.putText(
					frame,
					result.format(config['EMOTIONS'][max_emotion_idx], max_emotion_percentage, config['MOODS'][max_mood_idx], max_mood_percentage),
					(20, 20), config['FONT_STYLE'], config['FONT_SCALE'], config['COLOR'], config['TEXT_THICKNESS'])
				num_frames += 1

			# show the frame
			cv2.imshow('Video Streaming', frame)

			key = cv2.waitKey(1) & 0xFF
			# if the `q` key was pressed, break from the loop
			if key == ord('q'):
				break

			ret, frame = cap.read()

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	return

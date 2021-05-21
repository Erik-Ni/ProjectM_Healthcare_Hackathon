############################################################################################################################################

from .face_capture import deep_convert
import cv2
import numpy as np

#extra module
import json
import requests

############################################################################################################################################

def get_tf_response(config, roi):
	max_emotion_idx = 5
	max_mood_idx = 1
	max_emotion_percentage = 100
	max_mood_percentage = 100

	roi = cv2.resize(roi, (200, 200), interpolation = cv2.INTER_AREA)
	output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	output = output.reshape(1, 200, 200) /255.

	img_info = output.tolist()

	data = {'instances':img_info}
	push_data_json = json.dumps(data, sort_keys = True, separators=(',', ': '))

	emotion_request = requests.post(config['EMOTION_URL'], data=push_data_json).text
	emotion_response = json.loads(emotion_request)
	if 'predictions' in emotion_response:
		emotion_predictions = emotion_response['predictions'][0]
		max_emotion_idx = np.argmax(emotion_predictions)
		max_emotion_percentage = round(emotion_predictions[max_emotion_idx] * 100, 2)
	else:
		print('No emotion found at frame {}'.format(num_frames))
		print(emotion_response)

	mood_request = requests.post(config['MOOD_URL'], data = push_data_json).text
	mood_response = json.loads(mood_request)
	if 'predictions' in mood_response:
		mood_predictions = mood_response['predictions'][0]
		max_mood_idx = np.argmax(mood_predictions)
		max_mood_percentage = round(mood_predictions[max_mood_idx] * 100, 2)

	else:
		print('No mood found at frame {}'.format(num_frames))		
		print(mood_response)

	return max_emotion_idx, max_emotion_percentage, max_mood_idx, max_mood_percentage

def video_access(config, video_dir):
	num_frames = 0
	max_emotion_idx, max_mood_idx = 5, 1
	max_emotion_percentage, max_mood_percentage = 100, 100
	result = 'Emotion: {} ({}%) - Mood: {} ({}%)'

	cap = cv2.VideoCapture(video_dir)

	frame_width = int(cap.get(3)) 
	frame_height = int(cap.get(4))
	size = (frame_width, frame_height)

	if not (cap.isOpened()):
		print('Could not open video device')
	else:
		# loop over the frames from the video stream
		while True:
			ret, frame = cap.read()

			found_face, roi = deep_convert(config, frame)

			if found_face:
				num_frames += 1

				if (num_frames % config['FRAMES_PER_REQUEST']) == 0:
					max_emotion_idx, max_emotion_percentage, max_mood_idx, max_mood_percentage = get_tf_response(config, roi)
				
				cv2.putText(
					frame,
					result.format(config['EMOTIONS'][max_emotion_idx], max_emotion_percentage, config['MOODS'][max_mood_idx], max_mood_percentage),
					(20, 20), cv2.FONT_HERSHEY_COMPLEX, config['FONT_SCALE'], config['COLOR'], config['TEXT_THICKNESS'])

			# show the frame
			cv2.imshow('Frame', frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			if key == ord('q'):
				break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	return
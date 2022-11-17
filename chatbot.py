
### INIT ###

import json,re
class Responses:
	def __init__(self,response=['Error. Please contact the adminstrator.']) -> None:
		if type(response)!=list: raise TypeError(f'Error. \'{response}\' is not loadHeader list type')
		self.response=response
	def returnResponse(self):
		if len(self.response)==1:
			return self.response[0]
		elif len(self.response)>1:
			try:self.count+=1
			except:self.count=0
			try:return self.response[self.count]
			except:
				self.count=0
				return self.response[self.count]
replies,answers,requiredWords,outputMsg,DEBUG,FILEPATH={},{},{},[],False,'responses.json'

### INIT ###

### LOAD ###

with open(FILEPATH,'r') as file:
	data=json.load(file)
	for loadHeader,loadBody in data.items():
		if DEBUG==True:print(f'\nHeader: {loadHeader}')
		for loadKey,loadValue in loadBody.items():
			# Check if required words inside answer
			if not(loadKey in ['requiredWords','reply','answer']):print(f'There are other categories in the json file which will be ignored.\nThis will not affect the program. Header | \'{loadHeader}\'')
			elif loadKey == 'requiredWords':
				try:
					checkWords,reqWords=[],loadBody['requiredWords']
					for req in loadBody['answer']:
						if req in reqWords:checkWords.append(req)
					if len(reqWords)!=len(checkWords):raise TypeError(f"\nOnly '{', '.join(checkWords)}' was found in answers.\nPlease check that the required answers appears in the answers. | Header: {loadHeader}\nAnswers: {loadBody['answer']}\nReq Words: {loadBody['requiredWords']}")
				except KeyError:pass

### DEBUG ###

				if DEBUG:print('|\n|Required Words:\n|>- %s' % ("\n|>- ".join(reqWords)))
			elif loadKey == 'reply':
				if len(loadValue)==0: raise ValueError(f"Reply is empty. | Header: {loadHeader}")
				elif DEBUG:print('|\n|Reply:\n|>- %s' % ("\n|>- ".join(loadValue)))
			elif loadKey == 'answer':
				if len(loadValue)==0 and loadHeader!='others':raise ValueError(f"Answer is empty. | Header: {loadHeader}")
				elif ''.join(loadValue).lower() != ''.join(loadValue): raise TypeError(f"Answers are not in lower case. | Header: {loadHeader}")
				elif loadHeader=='others' and len(loadValue)!=0:print('The answer in header \'others\' is not empty.\nThis is not an error, but the characters inside will be ignored.')
				elif DEBUG and loadHeader!='others':print('|\n|Answer:\n|>- %s' % ("\n|>- ".join(loadValue)))
	if data['others']['answer']: print()
	if DEBUG:print()

### DEBUG ###

for header,body in data.items():
	for key,value in body.items():
		match key:
			case'reply':replies[header]=Responses(value)
			case'answer':answers[header]=value
			case'requiredWords':requiredWords[header]=value

### LOAD ###

### ALGORITHM ###
while True:
	user_input=input('You: ')
	split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
	highest_prob_list = {}
	def response(bot_response, list_of_words, single_response=False, required_words=[]):
		message_certainty,has_required_words = 0,True
		for word in split_message:
			if word in list_of_words: message_certainty += 1
		for word in required_words:
			if word not in split_message:
				has_required_words = False
				break
		highest_prob_list[bot_response] = int(float(message_certainty) / float(len(list_of_words)) * 100) if has_required_words or single_response else 0
	# Responses -------------------------------------------------------------------------------------------------------
	for keys in answers.keys():
		if keys!= 'others':
			try: response(replies[keys].returnResponse(), answers[keys], required_words=requiredWords[keys])
			except KeyError: response(replies[keys].returnResponse(), answers[keys], single_response=True)
	best_match = max(highest_prob_list, key=highest_prob_list.get)
	response = replies['others'].returnResponse() if highest_prob_list[best_match] < 1 else best_match
	print('Bot: ' + response)

### ALGORITHM ###

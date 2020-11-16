'''
Created by auto_sdk on 2020.09.23
'''
from dingtalk.api.base import RestApi
class OapiDingmiRobotPushRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.conversation_id = None
		self.msg_key = None
		self.msg_param = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingmi.robot.push'

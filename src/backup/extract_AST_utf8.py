import re
import sys
import os
import struct
from common import *

# ---------------- Group: AST -------------------
def parseImp(content, listCtrl, dealOnce):
	dealText = 0 # 0不处理 1已读WINDOW 尝试处理 2已进行处理至少一行
	for contentIndex in range(len(content)):
		if contentIndex < 1: continue #起始跳过行数
		lineData = content[contentIndex]
		#每行
		#print('>>> Line ' + str(contentIndex), ': ', lineData)
		if dealText == 1:
			if re.match(r'[<\n]', lineData):
				dealText = 0 #废弃上一个window
		if re.match(r'[;]', lineData): continue#注释行
		if dealText == 0:
			if re.match(r'<WINDOW', lineData): #名字行
				dealText = 1
				ret = re.search(r'NAME=".*?"', lineData)
				if ret:
					start = ret.start() + 6
					end = ret.end() - 1
					text = lineData[start:end]
					ctrl = {'pos':[contentIndex, start, end]}
					ctrl['name'] = True #名字标记
					#print(ctrl)
					if dealOnce(text, ctrl):
						listCtrl.append(ctrl)
			continue
		#处理对话
		else:
			if re.match(r'[<\n]', lineData):
				dealText = 0
				if 'unfinish' in listCtrl[-1]:
					del listCtrl[-1]['unfinish']
				continue
			dealText = 2
			#print(lineData, start, len(lineData))
			start = 0
			end = len(lineData) - 1
			ret = re.search(r'<', lineData)
			if ret:
				end = ret.start()
			text = lineData[start:end]
			#0行数，1起始字符下标（包含），2结束字符下标（不包含）
			ctrl = {'pos':[contentIndex, start, end]}
			ctrl['unfinish'] = True
			#print(ctrl)
			if dealOnce(text, ctrl):
				listCtrl.append(ctrl)

# -----------------------------------
def replaceOnceImp(content, lCtrl, lTrans):
	#print(lCtrl)
	#print(lTrans)
	num = len(lCtrl)
	for i in range(num):
		# 位置
		ctrl = lCtrl[i]
		contentIndex, start, end = ctrl['pos']
		trans = lTrans[i]
		#写入new
		strNew = content[contentIndex][:start] + trans + content[contentIndex][end:]
		#print(strNew)
		content[contentIndex] = strNew
		return True
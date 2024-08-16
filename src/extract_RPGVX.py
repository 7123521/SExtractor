import re
from common import *
from extract_TXT import ParseVar, dealLastCtrl, searchLine, initParseVar
from extract_RPGMV import replaceOnceImp as replaceOnceImpRPGMV
from extract_RPGMV import RPGParserMV 


# ---------------- Group: RPG Maker VX Ace -------------------
#解析
def parseImp(content, listCtrl, dealOnce):
	ExVar.jsonWrite = 0
	parser = RPGParserMV('@')
	parser.init(content, listCtrl, dealOnce)

	#处理
	parser.parseNode(content)

# -----------------------------------
def replaceOnceImp(content, lCtrl, lTrans):
	replaceOnceImpRPGMV(content, lCtrl, lTrans)
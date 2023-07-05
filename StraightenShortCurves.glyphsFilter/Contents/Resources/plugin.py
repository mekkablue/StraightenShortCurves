# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

@objc.python_method
def straightenSmallCurves(layer, threshold=12):
	for p in layer.paths:
		for i in range(len(p.nodes)-1,-1,-1):
			n = p.nodes[i]
			nn = n.nextNode
			nnn = n.nextNode.nextNode
			nnnn = n.nextNode.nextNode.nextNode
			if nn.type==OFFCURVE and nnn.type==OFFCURVE and nnnn.type!=OFFCURVE and not nnn.index < n.index:
				length = distance(n.position, nn.position)
				length += distance(nn.position, nnn.position)
				length += distance(nnn.position, nnnn.position)
				if length < threshold:
					nnnn.type = LINE
					del p.nodes[i+2]
					del p.nodes[i+1]

class StraightenShortCurves(FilterWithDialog):

	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	thresholdField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Straighten Short Curves',
			# 'de': 'Mein Filter',
			# 'fr': 'Mon filtre',
			# 'es': 'Mi filtro',
			# 'pt': 'Meu filtro',
			# 'jp': '私のフィルター',
			# 'ko': '내 필터',
			# 'zh': '我的过滤器',
			})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Straighten',
			# 'de': 'Anwenden',
			# 'fr': 'Appliquer',
			# 'es': 'Aplicar',
			# 'pt': 'Aplique',
			# 'jp': '申し込む',
			# 'ko': '대다',
			# 'zh': '应用',
			})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		
		# Set default value
		Glyphs.registerDefault('com.mekkablue.StraightenShortCurves.threshold', 12.0)
		
		# Set value of text field
		self.thresholdField.setStringValue_(Glyphs.defaults['com.mekkablue.StraightenShortCurves.threshold'])
		
		# Set focus to text field
		self.thresholdField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setThreshold_( self, sender ):
		
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.StraightenShortCurves.threshold'] = sender.floatValue()
		
		# Trigger redraw
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		if "threshold" in customParameters:
			threshold = customParameters['threshold']
		else:
			threshold = float(Glyphs.defaults['com.mekkablue.StraightenShortCurves.threshold'])
		
		straightenSmallCurves(layer, threshold=threshold)

	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; threshold:%s;" % (self.__class__.__name__, Glyphs.defaults['com.mekkablue.StraightenShortCurves.threshold'] )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

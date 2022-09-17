from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from enigma import eTimer
from Plugins.Extensions.DreamSat.core.commons import cfg ,isDreamOS

class DreamSatMessageBox(Screen):
	TYPE_YESNO = 0
	TYPE_INFO = 1
	TYPE_WARNING = 2
	TYPE_ERROR = 3
	
	def __init__(self, session, text, type = TYPE_YESNO, timeout = -1, close_on_any_key = False, default = True, enable_input = True, msgBoxID = None):
		self.type = type
		Screen.__init__(self, session)
		self.skin = self.buildSkin()
		self.msgBoxID = msgBoxID
		self['text'] = Label(text)
		self['Text'] = StaticText(text)
		self['selectedChoice'] = StaticText()
		self.text = text
		self.close_on_any_key = close_on_any_key
		self['ErrorPixmap'] = Pixmap()
		self['QuestionPixmap'] = Pixmap()
		self['InfoPixmap'] = Pixmap()
		self.origTitle = None
		self.timerRunning = False
		self.initTimeout(timeout)
		self.list = []
		if type != self.TYPE_ERROR:
			self['ErrorPixmap'].hide()
		if type != self.TYPE_YESNO:
			self['QuestionPixmap'].hide()
		if type != self.TYPE_INFO:
			self['InfoPixmap'].hide()
		if type == self.TYPE_YESNO:
			if default == True:
				self.list = [(_('yes'), 0), (_('no'), 1)]
			else:
				self.list = [(_('no'), 1), (_('yes'), 0)]
		if self.list:
			self['selectedChoice'].setText(self.list[0][0])
		self['list'] = MenuList(self.list)
		if enable_input:
			self['actions'] = ActionMap(['MsgBoxActions', 'DreamSatPanelActions', 'DirectionActions'], {'cancel': self.cancel,
			 'ok': self.ok,
			 'alwaysOK': self.alwaysOK,
			 'up': self.up,
			 'down': self.down,
			 'left': self.left,
			 'right': self.right,
			 'upRepeated': self.up,
			 'downRepeated': self.down,
			 'leftRepeated': self.left,
			 'rightRepeated': self.right}, -1)
		self.onLayoutFinish.append(self.setMessageTitle)
		self.onLayoutFinish.append(self.layoutFinished)
		return

	def buildSkin(self):
		primaryColor = cfg.primaryColor.getValue()
		primaryColorLabel = cfg.primaryColorLabel.getValue()
		secondaryColor = cfg.secondaryColor.getValue()
		secondaryColorLabel = cfg.secondaryColorLabel.getValue()
		if isDreamOS():
			skin = """<screen backgroundColor="{}" flags="wfNoBorder" name="MessageBox" position="center,center" size="900,10" title="Message">
					<widget backgroundColor="{}" font="LiFont;30" foregroundColor="{}" halign="left" noWrap="1" position="130,10" render="Label" size="750,40" source="Title" transparent="0" valign="center" zPosition="11" />
					<widget backgroundColor="{}" font="LiFont;27" foregroundColor="{}" halign="left" name="text" position="130,30" size="750,0" transparent="0" valign="center" zPosition="10" />
					<widget alphatest="blend" name="ErrorPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/disclaimer.png" position="20,40" size="84,84" />
					<widget alphatest="blend" name="QuestionPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/question.png" position="20,40" size="84,84" />
					<widget alphatest="blend" name="InfoPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/info.png" position="20,40" size="84,84" />
					<widget backgroundColor="{}" enableWrapAround="1" name="list" position="0,0" size="900,100" transparent="0" foregroundColorSelected="{}" backgroundColorSelected="{}" />
					</screen>""".format(primaryColor,primaryColor,primaryColorLabel,primaryColor,primaryColorLabel,primaryColor,secondaryColorLabel,secondaryColor)
		else:
			skin = """<screen backgroundColor="{}" flags="wfNoBorder" name="MessageBox" position="center,center" size="900,10" title="Message">
					<widget backgroundColor="{}" font="LiFont;30" foregroundColor="{}" halign="left" noWrap="1" position="130,10" render="Label" size="750,40" source="Title" transparent="0" valign="center" zPosition="11" />
					<widget backgroundColor="{}" font="LiFont;27" foregroundColor="{}" halign="left" name="text" position="130,30" size="750,0" transparent="0" valign="center" zPosition="10" />
					<widget alphatest="blend" name="ErrorPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/disclaimer.png" position="20,40" size="84,84" />
					<widget alphatest="blend" name="QuestionPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/question.png" position="20,40" size="84,84" />
					<widget alphatest="blend" name="InfoPixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/images/info.png" position="20,40" size="84,84" />
					<widget backgroundColor="{}" enableWrapAround="1" name="list" itemHeight="50" position="0,0" size="900,100" transparent="0" foregroundColorSelected="{}" backgroundColorSelected="{}" />

					</screen>""".format(primaryColor,primaryColor,primaryColorLabel,primaryColor,primaryColorLabel,primaryColor,secondaryColorLabel,secondaryColor)
		return skin

	def getOrigTitle(self):
		title = self.instance.getTitle()
		if self.type == self.TYPE_WARNING and title == _('Message'):
			title = _('Warning')
		elif self.type == self.TYPE_ERROR and title == _('Message'):
			title = _('Error')
		return title

	def layoutFinished(self):
		from enigma import eSize, ePoint
		if self.type != self.TYPE_YESNO:
			self.Title = ''
			wsize = (400, 10)
			self.instance.resize(eSize(*wsize))
		orgwidth = self.instance.size().width()
		orgpos = self.instance.position()
		textsize = self["text"].getSize()
		# y size still must be fixed in font stuff...
		textsize = (textsize[0] + 80, textsize[1] + 80)
		upperheight = 40
		offset = 70
		if self.type == self.TYPE_YESNO:
			offset = 120
			wsizex = textsize[0] + 115
			wsizey = textsize[1] + offset + upperheight
			upperheight += textsize[1]
			if (115 > upperheight):
				upperheight = 104
			if (600 > wsizex):
				wsizex = 900
			wsize = (wsizex, wsizey)
		else:
			wsizex = textsize[0] + 105
			wsizey = textsize[1] + 30
			if (115 > wsizey):
				wsizey = 115
			if (500 > wsizex):
				wsizex = 500
			wsize = (wsizex, wsizey)
		# resize
		self.instance.resize(eSize(*wsize))

		# resize label
		self["text"].instance.resize(eSize(*textsize))

		if self.type == self.TYPE_YESNO:
			# move list
			self["QuestionPixmap"].instance.move(ePoint(20, int((upperheight - 84)/ 2)))
			listsize = (wsizex, 100)
			self["list"].instance.move(ePoint(0, int(upperheight)+10))
			self["list"].instance.resize(eSize(*listsize))
			# center window
			newwidth = wsize[0]
			self.instance.move(ePoint(1920 -  int(wsize[0]), 1000 - int(wsizey)))
		else:
			self["list"].hide()
			self["ErrorPixmap"].instance.move(ePoint(20, (wsizey - 84)/ 2))
			self["InfoPixmap"].instance.move(ePoint(20, (wsizey - 84)/ 2))
			self.instance.move(ePoint(1920 -  wsize[0], 1000 - wsizey))

	def setMessageTitle(self):
		if self.origTitle is None:
			self.origTitle = self.getOrigTitle()
		self.setTitle(self.origTitle)
		return

	def initTimeout(self, timeout):
		self.timeout = timeout
		if timeout > 0:
			self.timer = eTimer()
			try:
				self.timer.callback.append(self.timerTick)
			except:
				self.timer_conn = self.timer.timeout.connect(self.timerTick)
			self.onExecBegin.append(self.startTimer)
			self.origTitle = None
			if self.execing:
				self.timerTick()
			else:
				self.onShown.append(self.__onShown)
			self.timerRunning = True
		else:
			self.timerRunning = False
		return

	def __onShown(self):
		self.onShown.remove(self.__onShown)
		self.timerTick()

	def startTimer(self):
		self.timer.start(1000)

	def stopTimer(self):
		if self.timerRunning:
			del self.timer
			self.onExecBegin.remove(self.startTimer)
			self.setTitle(self.origTitle)
			self.timerRunning = False

	def timerTick(self):
		if self.execing:
			self.timeout -= 1
			if self.origTitle is None:
				self.origTitle = self.getOrigTitle()
			self.setTitle(self.origTitle + ' (' + str(self.timeout) + ')')
			if self.timeout == 0:
				self.timer.stop()
				self.timerRunning = False
				self.timeoutCallback()
		return

	def timeoutCallback(self):
		self.ok()

	def cancel(self):
		self.close(False)

	def ok(self):
		if self.type == self.TYPE_YESNO:
			self.close(self['list'].getCurrent()[1] == 0)
		else:
			self.close(True)

	def alwaysOK(self):
		self.close(True)

	def up(self):
		self.move(self['list'].instance.moveUp)

	def down(self):
		self.move(self['list'].instance.moveDown)

	def left(self):
		self.move(self['list'].instance.pageUp)

	def right(self):
		self.move(self['list'].instance.pageDown)

	def move(self, direction):
		if self.close_on_any_key:
			self.close(True)
		self['list'].instance.moveSelection(direction)
		if self.list:
			self['selectedChoice'].setText(self['list'].getCurrent()[0])
		self.stopTimer()

	def __repr__(self):
		return str(type(self)) + '(' + self.text + ')'
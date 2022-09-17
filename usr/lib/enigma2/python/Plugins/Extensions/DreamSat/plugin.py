from Plugins.Plugin import PluginDescriptor
from enigma import addFont
from Plugins.Extensions.DreamSat.ui.launcher import LinuxsatLauncher
from Screens.MessageBox import MessageBox
from Plugins.Extensions.DreamSat.core.commons import isHD

addFont("/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/fonts/miso-bold.ttf", "LiFont", 100, 1)
addFont("/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/fonts/google-font.ttf", "GOI", 100, 1)
addFont("/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/assets/fonts/font_default.otf", "ArabicFont", 100, 1)

Ver = 1.3

def main(session, **kwargs):
    if isHD():
        session.open(MessageBox, _('Skin is not supported\nDreamSat Panel works only with FHD skins'), MessageBox.TYPE_ERROR)
    else:
        session.open(LinuxsatLauncher)

def showmenu(menuid, **kwargs):
    if menuid == "mainmenu":
        return [("DreamSatPanel", main, "DreamSatPanel", 1)]
    else:
        return []        

def Plugins(**kwargs):
    Descriptors=[]
    Descriptors.append(PluginDescriptor(where=[PluginDescriptor.WHERE_MENU], fnc=showmenu))
    Descriptors.append(PluginDescriptor(name='DreamSatPanel', description='DreamSatPanel By Linuxsat {}'.format(Ver), where=PluginDescriptor.WHERE_PLUGINMENU, icon='genuine.png', fnc=main))
    return Descriptors
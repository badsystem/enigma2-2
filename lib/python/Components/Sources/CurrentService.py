# -*- coding: utf-8 -*-
from Components.PerServiceDisplay import PerServiceBase
from enigma import iPlayableService
from Components.Sources.Source import Source
from Components.Element import cached
import NavigationInstance


class CurrentService(PerServiceBase, Source):
	def __init__(self, navcore):
		Source.__init__(self)
		PerServiceBase.__init__(self, navcore,
			{
				iPlayableService.evStart: self.serviceEvent,
				iPlayableService.evEnd: self.serviceEvent,
				# FIXME: we should check 'interesting_events'
				# which is not always provided.
				iPlayableService.evUpdatedInfo: self.serviceEvent,
				iPlayableService.evUpdatedEventInfo: self.serviceEvent,
				iPlayableService.evNewProgramInfo: self.serviceEvent,
				iPlayableService.evCuesheetChanged: self.serviceEvent,
				iPlayableService.evVideoSizeChanged: self.serviceEvent,
				iPlayableService.evVideoGammaChanged: self.serviceEvent,
				iPlayableService.evHBBTVInfo: self.serviceEvent
			}, with_event=True)
		self.navcore = navcore

	def serviceEvent(self, event):
		self.changed((self.CHANGED_SPECIFIC, event))

	@cached
	def getCurrentService(self):
		return self.navcore.getCurrentService()

	service = property(getCurrentService)

	@cached
	def getCurrentServiceRef(self):
		if NavigationInstance.instance is not None:
			return NavigationInstance.instance.getCurrentlyPlayingServiceOrGroup()
		return None

	serviceref = property(getCurrentServiceRef)

	@cached
	def getCurrentBouquetName(self):
		if NavigationInstance.instance is not None:
			return NavigationInstance.instance.currentBouquetName
		return ""

	currentBouquetName = property(getCurrentBouquetName)

	def destroy(self):
		PerServiceBase.destroy(self)
		Source.destroy(self)

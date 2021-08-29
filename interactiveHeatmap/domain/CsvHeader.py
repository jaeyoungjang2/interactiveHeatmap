from enum import Enum, unique

@unique
class CsvHeader(Enum):
	GENE_ID = ("Gene_ID")
	NORMALIZED_EXPRESSION_VALUE = ("N_")
	# __targetIndexLst = []
	# __resultHeaderLst = []

	def __init__(self, value):
		self.value = value

	def getTarget(self, headerColumnLst):
		for index, headerColumn in enumerate(headerColumnLst):
			__targetIndexLst.append(index)
			__resultHeaderLst.append(headerColumn)

	def getTargetIndexLst(self):
		return targetIndexLst

	def getResultHeaderLst(self):
		return getResultHeaderLst

	def getValueList(self):
		return [csvHeader.value for csvHeader in CsvHeader]
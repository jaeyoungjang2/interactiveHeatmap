import json

class JsonFileParser:
	def run(self, data3File, inputDir, outputDir, degGroup, sampleInfoFile):
		self.data3File = data3File
		self.inputDir = inputDir
		self.outputDir = outputDir
		self.degGroup = degGroup
		self.SampleInfoFile = sampleInfoFile
		self.addData3Info()
		self.replaceSampleName()
		self.addDEGgroupInfo()
		self.addSampleInDegGroup()
		self.writeJsonFile()

	def addData3Info(self):
		ColumnDic = {}
		self.infoDic = {}

		# set ColumnDic for self.infoDic
		# ColumnDic = { 0 : geneID , 1 : transcriptID...}
		fr = open(self.inputDir+self.data3File,'r')
		headerLst = fr.readline().strip().split('\t')

		for index, header in enumerate(headerLst):
			ColumnDic[index] = header

		# set self.infoDic
		# self.infoDic = { gene : { "Transcript_ID" : Transcript_ID , "Gene_Symbol" : Gene_Symbol }}
		for line in fr:
			li = line.strip().split('\t')
			for index, value in enumerate(li):
				if index == 0:
					geneID = value
					self.infoDic[value] = {}
					continue
				ColumnName = ColumnDic[index]
				self.infoDic[geneID][ColumnName] = value

		with open(self.outputDir+self.data3File+'_Inchlib_output.json', 'r') as json_file:
			self.json_data = json.load(json_file)
			for node in self.json_data["data"]["nodes"]:
				if "objects" in self.json_data["data"]["nodes"][node]:
					geneID = self.json_data["data"]["nodes"][node]["objects"][0]
					self.json_data["data"]["nodes"][node]["information"] = self.infoDic[geneID]

		# with open('/mnt/garnet/Analysis/BI/RNA-Seq/HN00153743/DEG/Output/outputOfInchlib_addExpression.json','w')
		with open(self.outputDir+self.data3File+"_addExpression.json",'w') as fw:
			json.dump(self.json_data,fw,indent=4)


	def replaceSampleName(self):
		sampleNameLst = []
		for sampleName in self.json_data["data"]["feature_names"]:
			sampleNameLst.append(sampleName.replace("Z_",""))
		self.json_data["data"]["feature_names"] = sampleNameLst


	def addDEGgroupInfo(self):
		self.testGroup = self.degGroup.split("_vs_")[0]
		self.controlGroup = self.degGroup.split("_vs_")[1]

		# self.json_data["data"]["group_names"]["test"] = self.testGroup
		# self.json_data["data"]["group_names"]["control"] = self.controlGroup
		self.json_data["data"]["group_names"] = {"test": self.testGroup, "control": self.controlGroup}

	def addSampleInDegGroup(self):
		self.testGroupSampleLst = []
		self.controlGroupSampleLst = []

		fr = open(self.SampleInfoFile,'r')
		headerLst = fr.readline().strip().split('\t')
		numOfColumn = len(headerLst)

		for line in fr:
			li = line.strip().split('\t')
			sampleName = li[1]
			for index in range(2, numOfColumn):
				groupName = li[index]
				if groupName == self.testGroup:
					self.testGroupSampleLst.append(sampleName)
				elif groupName == self.controlGroup:
					self.controlGroupSampleLst.append(sampleName)

		self.json_data["data"]["test"] = self.testGroupSampleLst
		self.json_data["data"]["control"] = self.controlGroupSampleLst

	def writeJsonFile(self):
		with open(self.outputDir+self.data3File+"_jsonParserInit.json",'w') as fw:
			json.dump(self.json_data,fw,indent=4)

	def addGroupNameOnHeader(self, headerName):
		fr = open(self.outputDir+self.data3File+"_jsonParserInit.json",'r')
		fw = open(self.outputDir+self.data3File+"_Final.json",'w')
		header = fr.readline().strip()
		header = headerName +'='+ header
		fw.write(header+'\n')
		for line in fr:
			fw.write(line)
		fr.close()
		fw.close()

	def getTestGroupSampleLst(self):
		return self.testGroupSampleLst

	def getControlGroupSampleLst(self):
		return self.controlGroupSampleLst

	def getData3InfoDic(self):
		return self.infoDic
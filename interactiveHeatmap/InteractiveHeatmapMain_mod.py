from utils.InputFormatChanger import InputFormatChanger
from utils.JsonFileParser_mod import JsonFileParser
from domain.Analysis import Analysis
from domain.HtmlReport import HtmlReport
from domain.HtmlWithoutPval import HtmlWithoutPval
from domain.Data3HtmlReport import Data3HtmlReport
from domain.Data3HtmlReportWithoutPval import Data3HtmlReportWithoutPval
from utils.Gprofiler import Gprofiler
from utils.KEGG import KEGG
from config.__config__ import program as pg

import os, sys, copy, argparse

def run():
	# degOutputDir = sys.argv[1]+"/"
	# degTool = sys.argv[2]
	# isPval = sys.argv[3]
	runGprofiler = "yes"
	runKegg = "yes"
	outputDir = f"{degOutputDir}../interactive_Output/"
	resultDir = f"{degOutputDir}../interactive_Result/"
	convertValue = {"edgeR":".logCPM","DESeq2":".baseMean"}
	converPlotName = {"edgeR":"MA plot","DESeq2":"Smear plot"}

	groupMean = ".volume"
	plotName = "Volume plot"
	if degTool in convertValue:
		groupMean = convertValue[degTool]
		plotName = converPlotName[degTool]

	inputFormatChanger = InputFormatChanger()
	analysis = Analysis()
	DegGroupDic, representativeData3Dic = getDegGroupInfo(degOutputDir, degOutputDir)

	os.system(f'mkdir -p {outputDir}')

	for data3File in DegGroupDic:
		if isPval == "yes":
			htmlReport = HtmlReport()
		else:
			htmlReport = HtmlWithoutPval()

		os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}')
		os.system(f'mkdir -p {resultDir+"html/"}')
		# 특정 조합의 data3 file을 기반으로한 json 파일 만드는 작업.
		inputFormatChanger.addZscore(data3File, degOutputDir, outputDir)
		inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(data3File, outputDir)
		analysis.runIncHlib(data3File, outputDir)
		# jsonFileParser.run(data3File, degOutputDir, outputDir, DegGoupDic[data3File], degOutputDir+'Sample.Info.txt')
		jsonFileParser = JsonFileParser(data3File)
		jsonFileParser.addData3Info(degOutputDir, outputDir)
		jsonFileParser.replaceSampleName()
		jsonFileParser.addDEGgroupInfo(DegGroupDic[data3File])
		jsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
		jsonFileParser.writeJsonFile(outputDir)
		jsonFileParser.addGroupNameOnHeader(outputDir, DegGroupDic[data3File])

		testGroupSampleLst = jsonFileParser.getTestGroupSampleLst()
		controlGroupSampleLst = jsonFileParser.getControlGroupSampleLst()
		totalSampleLst = testGroupSampleLst + controlGroupSampleLst
		data3InfoDic = jsonFileParser.getData3InfoDic()

		# data3 result copy
		os.system(f"cp \"{outputDir}/{data3File}_Final.json\" \"{resultDir}/json/data3_{DegGroupDic[data3File]}.json\"")

		if runGprofiler == "yes":
			goDic = {"BP":{}, "MF":{}, "CC":{}}
			# goAnalysis
			# 특정 조합의 유의미한 GO term을 기반으로한 json 파일 만드는 작업

			degGoOutputDir = degOutputDir+"gprofiler/stat.p/"
			goStatFile = data3File[:-3]+"GO.stat.p"
			outputGoDir = outputDir+"gprofiler/"

			gprofiler = Gprofiler(data3InfoDic, groupMean, totalSampleLst)
			gprofiler.findTargetIndex(degGoOutputDir+goStatFile)
			# 특정 조합의 GO stat 파일 확인

			os.system(f'mkdir -p {outputGoDir}/{DegGroupDic[data3File]}')

			fr = open(degGoOutputDir+goStatFile,'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				if gprofiler.isValidGoTerm(line) == False:
					continue
				if isPval == 'yes':
					goDic = gprofiler.makeGoData3File(f'{outputGoDir}/{DegGroupDic[data3File]}/', DegGroupDic[data3File], goDic)
				else:
					goDic = gprofiler.makeGoQuantileExceptPvalFile(f'{outputGoDir}/{DegGroupDic[data3File]}/', DegGroupDic[data3File], goDic)

				termName = gprofiler.getTermName()
				inputFormatChanger.addZscore(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				analysis.runIncHlib(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/')

				goJsonFileParser = JsonFileParser(f'{termName}.txt')
				goJsonFileParser.addData3Info(f'{outputGoDir}/{DegGroupDic[data3File]}/', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				goJsonFileParser.replaceSampleName()
				goJsonFileParser.addDEGgroupInfo(DegGroupDic[data3File])
				goJsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
				goJsonFileParser.writeJsonFile(f'{outputGoDir}/{DegGroupDic[data3File]}/')
				goJsonFileParser.addGroupNameOnHeader(f'{outputGoDir}/{DegGroupDic[data3File]}/', termName)
			fr.close()

			# go result copy
			for source in goDic:
				if len(goDic[source]) < 1:
					continue
				os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}/{source}')
				for termName in goDic[source]:
					os.system(f"cp \"{outputGoDir}/{DegGroupDic[data3File]}/{termName}.txt_Final.json\" \"{resultDir}/json/{DegGroupDic[data3File]}/{source}/{termName}.json\"")

			# write go html part
			htmlReport.writeGoColumn(goDic, DegGroupDic[data3File], "sub")

		if runKegg == "yes":
			keggDic = {}
			# 특정 조합의 유의미한 KEGG term을 기반으로한 json 파일 만드는 작업
			degKeggOutputDir = degOutputDir+"KEGG_view/table_p/"
			keggStatFile = "pathway."+data3File[:-3]+"table.p"
			outputKeggDir = outputDir+"KEGG/"

			# 특정 조합의 GO stat 파일 확인
			kegg = KEGG(data3InfoDic, groupMean, totalSampleLst)
			kegg.findTargetIndex(degKeggOutputDir+keggStatFile)

			os.system(f'mkdir -p {outputKeggDir}/{DegGroupDic[data3File]}')

			fr = open(degKeggOutputDir+keggStatFile, 'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 kegg term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성

				if kegg.isValidKeggTerm(line) == False:
					continue
				li = line.strip().split('\t')

				# kegg term에 대한 expression profile 결과 생성
				mapName = kegg.getMapName()

				if isPval == 'yes':
					keggDic = kegg.makeKeggData3File(DegGroupDic[data3File], f'{outputKeggDir}/{DegGroupDic[data3File]}/', keggDic)
				else:
					keggDic = kegg.makeKeggQuantileExceptPvalFile(DegGroupDic[data3File], f'{outputKeggDir}/{DegGroupDic[data3File]}/', keggDic)

				inputFormatChanger.addZscore(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				analysis.runIncHlib(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/')

				keggJsonFileParser = JsonFileParser(f'{mapName}.txt')
				keggJsonFileParser.addData3Info(f'{outputKeggDir}/{DegGroupDic[data3File]}/', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				keggJsonFileParser.replaceSampleName()
				keggJsonFileParser.addDEGgroupInfo(DegGroupDic[data3File])
				keggJsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
				keggJsonFileParser.writeJsonFile(f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				keggJsonFileParser.addGroupNameOnHeader(f'{outputKeggDir}/{DegGroupDic[data3File]}/', mapName)

			os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}')

			# kegg result copy
			for keggMap in keggDic:
				os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}/KEGG')
				os.system(f"cp \"{outputKeggDir}/{DegGroupDic[data3File]}/{keggMap}.txt_Final.json\" \"{resultDir}/json/{DegGroupDic[data3File]}/KEGG/{keggMap}.json\"")

			# write kegg html part
			htmlReport.writeKEGGColumn(keggDic, DegGroupDic[data3File], "sub")
		##################kegg end###########################
		# goDic = {"BP":{'acetyltransferase_activity.txt_Final':0.1,'actin_binding.txt_Final':0.2,'antioxidant_activity.txt_Final':0.3,'apical_dendrite.txt_Final':0.4,'arachidonic_acid_metabolic_process.txt_Final':0.5,'ATP_biosynthetic_process.txt_Final':0.6,'ATP_metabolic_process.txt_Final':0.7,'axon_development.txt_Final':0.8,'axon_extension_involved_in_axon_guidance.txt_Final':0.9,'axon_extension.txt_Final':0.10},"CC":{'axon_guidance.txt_Final':0.1,'axonogenesis.txt_Final':0.2,'beta_catenin_TCF_complex_assembly.txt_Final':0.3,'bitter_taste_receptor_activity.txt_Final':0.4,'body_morphogenesis.txt_Final':0.5,'calcium_channel_activity.txt_Final':0.6,'calcium_dependent_phospholipid_binding.txt_Final':0.7,'calcium_ion_binding.txt_Final':0.8,'cargo_receptor_activity.txt_Final':0.9,'cation_channel_activity.txt_Final':0.10},"MF":{'cell_morphogenesis_involved_in_differentiation.txt_Final':0.1,'cell_morphogenesis_involved_in_neuron_differentiation.txt_Final':0.2,'cell_part_morphogenesis.txt_Final':0.3,'cell_projection_morphogenesis.txt_Final':0.4,'cellular_component_morphogenesis.txt_Final':0.5,'cellular_detoxification.txt_Final':0.6,'cellular_oxidant_detoxification.txt_Final':0.7,'cellular_response_to_hormone_stimulus.txt_Final':0.8,'cellular_response_to_lectin.txt_Final':0.9,'cellular_response_to_toxic_substance.txt_Final':0.10}}

		newDegGroupDic = copy.deepcopy(DegGroupDic)
		newDegGroupDic["data3_File"] = "data3_File"
		htmlReport.writeLabelColumn(newDegGroupDic)
		htmlReport.makeHtmlReport(resultDir+"html/"+DegGroupDic[data3File]+".html", DegGroupDic[data3File], "sub", plotName)

	if len(DegGroupDic) == 0:
		data3File = list(representativeData3Dic.keys())[0]
		if isPval == "yes":
			htmlReport = HtmlReport()
		else:
			htmlReport = HtmlWithoutPval()

		os.system(f'mkdir -p {resultDir}/json/')

		# 특정 조합의 data3 file을 기반으로한 json 파일 만드는 작업
		inputFormatChanger.addZscore(data3File, degOutputDir, outputDir)
		inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(data3File, outputDir)
		analysis.runIncHlib(data3File, outputDir)
		# jsonFileParser.run(data3File, degOutputDir, outputDir, DegGoupDic[data3File], degOutputDir+'Sample.Info.txt')
		jsonFileParser = JsonFileParser(data3File)
		jsonFileParser.addData3Info(degOutputDir, outputDir)
		jsonFileParser.replaceSampleName()
		jsonFileParser.addDEGgroupInfo(representativeData3Dic[data3File][0])
		jsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
		jsonFileParser.writeJsonFile(outputDir)
		jsonFileParser.addGroupNameOnHeader(outputDir, representativeData3Dic[data3File][0])

		testGroupSampleLst = jsonFileParser.getTestGroupSampleLst()
		controlGroupSampleLst = jsonFileParser.getControlGroupSampleLst()
		totalSampleLst = testGroupSampleLst + controlGroupSampleLst
		data3InfoDic = jsonFileParser.getData3InfoDic()


		# data3 result copy
		os.system(f"cp \"{outputDir}/{data3File}_Final.json\" \"{resultDir}/json/data3_{representativeData3Dic[data3File][0]}.json\"")

		if runGprofiler == "yes":
			goDic = {"BP":{}, "MF":{}, "CC":{}}
			# goAnalysis
			# 특정 조합의 유의미한 GO term을 기반으로한 json 파일 만드는 작업

			degGoOutputDir = degOutputDir+"gprofiler/stat.p/"

			if isPval == "yes":
				goStatFile = "data3_fc2_&_raw.p.GO.stat.p"
			else:
				goStatFile = "data3_fc2.GO.stat.p"

			outputGoDir = outputDir+"gprofiler/"

			gprofiler = Gprofiler(data3InfoDic, groupMean, totalSampleLst)
			gprofiler.findTargetIndex(degGoOutputDir+goStatFile)
			# 특정 조합의 GO stat 파일 확인

			os.system(f'mkdir -p {outputGoDir}/{representativeData3Dic[data3File][0]}')

			fr = open(degGoOutputDir+goStatFile,'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				if gprofiler.isValidGoTerm(line) == False:
					continue
				if isPval == 'yes':
					goDic = gprofiler.makeGoData3File(f'{outputGoDir}/{representativeData3Dic[data3File][0]}/', representativeData3Dic[data3File][0], goDic)
				else:
					goDic = gprofiler.makeGoQuantileExceptPvalFile(f'{outputGoDir}/{representativeData3Dic[data3File][0]}/', representativeData3Dic[data3File][0], goDic)

				termName = gprofiler.getTermName()
				inputFormatChanger.addZscore(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File][0]}/', f'{outputGoDir}/{representativeData3Dic[data3File][0]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File][0]}/')
				analysis.runIncHlib(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File][0]}/')

				goJsonFileParser = JsonFileParser(f'{termName}.txt')
				goJsonFileParser.addData3Info(f'{outputGoDir}/{representativeData3Dic[data3File][0]}/', f'{outputGoDir}/{representativeData3Dic[data3File][0]}/')
				goJsonFileParser.replaceSampleName()
				goJsonFileParser.addDEGgroupInfo(representativeData3Dic[data3File][0])
				goJsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
				goJsonFileParser.writeJsonFile(f'{outputGoDir}/{representativeData3Dic[data3File][0]}/')
				goJsonFileParser.addGroupNameOnHeader(f'{outputGoDir}/{representativeData3Dic[data3File][0]}/', termName)

			fr.close()
			# go result copy
			for source in goDic:
				if len(goDic[source]) < 1:
					continue
				os.system(f'mkdir -p {resultDir}/json/{representativeData3Dic[data3File][0]}/{source}')
				for termName in goDic[source]:
					os.system(f"cp \"{outputGoDir}/{representativeData3Dic[data3File][0]}/{termName}.txt_Final.json\" \"{resultDir}/json/{representativeData3Dic[data3File][0]}/{source}/{termName}.json\"")

			# write go html part
			htmlReport.writeGoColumn(goDic, representativeData3Dic[data3File][0], "main")

		if runKegg == "yes":
			keggDic = {}
			# 특정 조합의 유의미한 KEGG term을 기반으로한 json 파일 만드는 작업
			degKeggOutputDir = degOutputDir+"KEGG_view/table_p/"

			if isPval == "yes":
				keggStatFile = "pathway.data3_fc2_&_raw.p.table.p"
			else:
				keggStatFile = "pathway.data3_fc2.table.p"

			outputKeggDir = outputDir+"KEGG/"

			# 특정 조합의 GO stat 파일 확인
			kegg = KEGG(data3InfoDic, groupMean, totalSampleLst)
			kegg.findTargetIndex(degKeggOutputDir+keggStatFile)

			os.system(f'mkdir -p {outputKeggDir}/{representativeData3Dic[data3File][0]}')

			fr = open(degKeggOutputDir+keggStatFile, 'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 kegg term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성

				if kegg.isValidKeggTerm(line) == False:
					continue
				li = line.strip().split('\t')

				# kegg term에 대한 expression profile 결과 생성
				mapName = kegg.getMapName()

				if isPval == 'yes':
					keggDic = kegg.makeKeggData3File(representativeData3Dic[data3File][0], f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/', keggDic)
				else:
					keggDic = kegg.makeKeggQuantileExceptPvalFile(representativeData3Dic[data3File][0], f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/', keggDic)

				inputFormatChanger.addZscore(f'{mapName}.txt', f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/', f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{mapName}.txt', f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/')
				analysis.runIncHlib(f'{mapName}.txt', f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/')

				keggJsonFileParser = JsonFileParser(f'{mapName}.txt')
				keggJsonFileParser.addData3Info(f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/', f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/')
				keggJsonFileParser.replaceSampleName()
				keggJsonFileParser.addDEGgroupInfo(representativeData3Dic[data3File][0])
				keggJsonFileParser.addSampleInfoByDegGroup(degOutputDir+'Sample.Info.txt')
				keggJsonFileParser.writeJsonFile(f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/')
				keggJsonFileParser.addGroupNameOnHeader(f'{outputKeggDir}/{representativeData3Dic[data3File][0]}/', mapName)

			os.system(f'mkdir -p {resultDir}/json/{representativeData3Dic[data3File][0]}')

			# kegg result copy
			for keggMap in keggDic:
				os.system(f'mkdir -p {resultDir}/json/{representativeData3Dic[data3File][0]}/KEGG')
				os.system(f"cp \"{outputKeggDir}/{representativeData3Dic[data3File][0]}/{keggMap}.txt_Final.json\" \"{resultDir}/json/{representativeData3Dic[data3File][0]}/KEGG/{keggMap}.json\"")

			# write kegg html part
			htmlReport.writeKEGGColumn(keggDic, representativeData3Dic[data3File][0], "main")

		newDic = {}
		newDic[data3File] = representativeData3Dic[data3File][0]
		htmlReport.writeLabelColumn(newDic)
		htmlReport.makeHtmlReport(resultDir+representativeData3Dic[data3File][0]+".html", representativeData3Dic[data3File][0], "main", plotName)

	else:
		data3File = list(representativeData3Dic.keys())[0]

		if isPval == "yes":
			htmlReport = Data3HtmlReport()
		else:
			htmlReport = Data3HtmlReportWithoutPval()

		# 특정 조합의 data3 file을 기반으로한 json 파일 만드는 작업
		inputFormatChanger.addZscore(data3File, degOutputDir, outputDir)
		inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(data3File, outputDir)
		analysis.runIncHlib(data3File, outputDir)
		# jsonFileParser.run(data3File, degOutputDir, outputDir, DegGoupDic[data3File], degOutputDir+'Sample.Info.txt')
		jsonFileParser = JsonFileParser(data3File)
		jsonFileParser.addData3Info(degOutputDir, outputDir)
		jsonFileParser.replaceSampleName()

		jsonFileParser.addDEGgroupInfo2(representativeData3Dic[data3File])

		jsonFileParser.writeJsonFile(outputDir)
		jsonFileParser.addGroupNameOnHeader(outputDir, "File")

		totalSampleLst = jsonFileParser.getTotalSampleInfo()
		data3InfoDic = jsonFileParser.getData3InfoDic()

		# data3 result copy
		os.system(f"cp \"{outputDir}/{data3File}_Final.json\" \"{resultDir}/json/data3_File.json\"")

		if runGprofiler == "yes":
			goDic = {"BP":{}, "MF":{}, "CC":{}}
			# goAnalysis
			# 특정 조합의 유의미한 GO term을 기반으로한 json 파일 만드는 작업

			degGoOutputDir = degOutputDir+"gprofiler/stat.p/"
			if isPval == "yes":
				goStatFile = "data3_fc2_&_raw.p.GO.stat.p"
			else:
				goStatFile = "data3_fc2.GO.stat.p"

			outputGoDir = outputDir+"gprofiler/"

			gprofiler = Gprofiler(data3InfoDic, groupMean, totalSampleLst)
			gprofiler.findTargetIndex(degGoOutputDir+goStatFile)
			# 특정 조합의 GO stat 파일 확인

			cmd = f'mkdir -p {outputGoDir}/data3_File'
			os.system(cmd)

			fr = open(degGoOutputDir+goStatFile,'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				if gprofiler.isValidGoTerm(line) == False:
					continue
				if isPval == 'yes':
					goDic = gprofiler.makeGoData3File2(f'{outputGoDir}/data3_File/', representativeData3Dic[data3File], goDic)
				else:
					goDic = gprofiler.makeGoQuantileExceptPvalFile2(f'{outputGoDir}/data3_File/', representativeData3Dic[data3File], goDic)

				termName = gprofiler.getTermName()
				inputFormatChanger.addZscore(f'{termName}.txt', f'{outputGoDir}/data3_File/', f'{outputGoDir}/data3_File/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{termName}.txt', f'{outputGoDir}/data3_File/')
				analysis.runIncHlib(f'{termName}.txt', f'{outputGoDir}/data3_File/')

				goJsonFileParser = JsonFileParser(f'{termName}.txt')
				goJsonFileParser.addData3Info(f'{outputGoDir}/data3_File/', f'{outputGoDir}/data3_File/')
				goJsonFileParser.replaceSampleName()
				goJsonFileParser.addDEGgroupInfo2(representativeData3Dic[data3File])
				goJsonFileParser.writeJsonFile(f'{outputGoDir}/data3_File/')
				goJsonFileParser.addGroupNameOnHeader(f'{outputGoDir}/data3_File/', termName)

			fr.close()
			# go result copy
			for source in goDic:
				if len(goDic[source]) < 1:
					continue
				os.system(f'mkdir -p {resultDir}/json/data3_File/{source}')
				for termName in goDic[source]:
					os.system(f"cp \"{outputGoDir}/data3_File/{termName}.txt_Final.json\" \"{resultDir}/json/data3_File/{source}/{termName}.json\"")

			# write go html part
			htmlReport.writeGoColumn(goDic, "data3_File", "main")

		if runKegg == "yes":
			keggDic = {}
			# 특정 조합의 유의미한 KEGG term을 기반으로한 json 파일 만드는 작업
			degKeggOutputDir = degOutputDir+"KEGG_view/table_p/"

			if isPval == "yes":
				keggStatFile = "pathway.data3_fc2_&_raw.p.table.p"
			else:
				keggStatFile = "pathway.data3_fc2.table.p"
			outputKeggDir = outputDir+"KEGG/"

			# 특정 조합의 GO stat 파일 확인
			kegg = KEGG(data3InfoDic, groupMean, totalSampleLst)
			kegg.findTargetIndex(degKeggOutputDir+keggStatFile)

			cmd = f'mkdir -p {outputKeggDir}/data3_File'
			os.system(cmd)

			fr = open(degKeggOutputDir+keggStatFile, 'r')
			fr.readline()
			for line in fr:
				# 특정 조합의 kegg term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				if kegg.isValidKeggTerm(line) == False:
					continue
				if isPval == 'yes':
					keggDic = kegg.makeKeggData3File2(representativeData3Dic[data3File], f'{outputKeggDir}/data3_File/', keggDic)
				else:
					keggDic = kegg.makeKeggQuantileExceptPvalFile2(representativeData3Dic[data3File], f'{outputKeggDir}/data3_File/', keggDic)

				# kegg term에 대한 expression profile 결과 생성
				mapName = kegg.getMapName()
				inputFormatChanger.addZscore(f'{mapName}.txt', f'{outputKeggDir}/data3_File/', f'{outputKeggDir}/data3_File/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{mapName}.txt', f'{outputKeggDir}/data3_File/')
				analysis.runIncHlib(f'{mapName}.txt', f'{outputKeggDir}/data3_File/')

				keggJsonFileParser = JsonFileParser(f'{mapName}.txt')
				keggJsonFileParser.addData3Info(f'{outputKeggDir}/data3_File/', f'{outputKeggDir}/data3_File/')
				keggJsonFileParser.replaceSampleName()
				keggJsonFileParser.addDEGgroupInfo2(representativeData3Dic[data3File])
				keggJsonFileParser.writeJsonFile(f'{outputKeggDir}/data3_File/')
				keggJsonFileParser.addGroupNameOnHeader(f'{outputKeggDir}/data3_File/', mapName)

			os.system(f'mkdir -p {resultDir}/json/data3_File')

			# kegg result copy
			for keggMap in keggDic:
				os.system(f'mkdir -p {resultDir}/json/data3_File/KEGG')
				os.system(f"cp \"{outputKeggDir}/data3_File/{keggMap}.txt_Final.json\" \"{resultDir}/json/data3_File/KEGG/{keggMap}.json\"")

			# write kegg html part
			htmlReport.writeKEGGColumn(keggDic, "data3_File", "main")

		htmlReport.writeLabelColumn(representativeData3Dic)
		htmlReport.makeHtmlReport(resultDir+"data3_File.html", "File", "main")

	os.system(f"cp -r {pg['RESOURCE_JAVASCRIPT_DIR_PATH']} {resultDir}")
	os.system(f"cp -r {pg['RESOURCE_CSS_DIR_PATH']} {resultDir}")

def getDegGroupInfo(inputDir, degOutputDir):
	DegGroupDic = {}
	representativeData3Dic = {}
	fileList = os.popen(f'ls {degOutputDir}').read().split('\n')
	for file in fileList:
		if file.startswith('data3') and file.endswith('txt'):
			comparisonGroup = file.split('data3_')[1].split('_fc')[0]
			# data3_fc2_&_raw.p.txt
			if comparisonGroup.startswith('fc'):
				representativeData3Dic[file] = []
				fr = open(inputDir+file , 'r')
				headerColumnLst = fr.readline().strip().split('\t')
				for headerColumn in headerColumnLst:
					if headerColumn.endswith(".fc"):
						representativeData3Dic[file].append(headerColumn.split('.fc')[0].replace("/","_vs_"))
				fr.close()
				continue
			DegGroupDic[file] = comparisonGroup
	return DegGroupDic, representativeData3Dic

def checkSampleInfo():
	fr = open(degOutputDir+'Sample.Info.txt','r')
	for line in fr:
		li = line.strip().split('\t')
		for i in li[2:]:
			if '-' in i:
				sys.exit("ERROR: change group name. '-' cannot be used as a group name.")


def main():
	checkSampleInfo()
	run()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	basic= parser.add_argument_group(title="Basic option")
	basic.add_argument('--deg', '-d', type=str,  help='Specify DEG output directory.')
	basic.add_argument('--tool', '-t', type=str, help="Specify DEG tool name [edgeR | DESeq2 | else]")
	basic.add_argument("--pval", '-p', type = str, help = "Does the p-value exist? [yes | no]")



	args=parser.parse_args()
	if None in args.__dict__.values():
		for key in args.__dict__.keys():
			if args.__dict__[key]==None:
				print("ERROR : (Wrong parameter) -"+key + " Parameter is Empty ")
		print(" This is a required input value ")
		print(" Enter the Command below to learn How to use it ")
		print('python ' + sys.argv[0] + " -h \n")
		sys.exit()

	degOutputDir = args.deg+"/"
	degTool = args.tool
	isPval = args.pval

	main()

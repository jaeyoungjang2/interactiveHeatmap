from utils.InputFormatChanger import InputFormatChanger
from utils.JsonFileParser import JsonFileParser
from domain.Analysis import Analysis
from domain.HtmlReport import HtmlReport

import os, sys

def run():
	# degOutputDir = "/mnt/garnet/Analysis/BI/RNA-Seq/HN00153700/DEG/Output/"
	# degTool = "edgeR"
	degOutputDir = sys.argv[1]+"/"
	degTool = sys.argv[2]
	runGprofiler = "yes"
	runKegg = "yes"
	outputDir = f"{degOutputDir}../interactive_Output/"
	resultDir = f"{degOutputDir}../interactive_Result/"
	convertValue = {"edgeR":".logCPM","DESeq2":".baseMean"}
	groupMean = convertValue[degTool]

	inputFormatChanger = InputFormatChanger()
	analysis = Analysis()
	DegGroupDic, representativeData3Dic = getDegGroupInfo(degOutputDir, degOutputDir)
	htmlReport = HtmlReport()

	os.system(f'mkdir -p {outputDir}')
	for data3File in DegGroupDic:
		os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}')
		os.system(f'mkdir -p {resultDir+"html/"}')
		# 특정 조합의 data3 file을 기반으로한 json 파일 만드는 작업
		inputFormatChanger.addZscore(data3File, degOutputDir, outputDir)
		inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(data3File, outputDir)
		analysis.runIncHlib(data3File, outputDir)
		jsonFileParser = JsonFileParser()
		jsonFileParser.run(data3File, degOutputDir, outputDir, DegGroupDic[data3File], degOutputDir+'Sample.Info.txt')
		jsonFileParser.addGroupNameOnHeader(DegGroupDic[data3File])

		# data3 result copy
		os.system(f"cp \"{outputDir}/{data3File}_Final.json\" \"{resultDir}/json/data3_{DegGroupDic[data3File]}.json\"")

		if runGprofiler == "no":
			# goAnalysis
			# 특정 조합의 유의미한 GO term을 기반으로한 json 파일 만드는 작업
			degGoOutputDir = degOutputDir+"gprofiler/stat.p/"
			goStatFile = data3File[:-3]+"GO.stat.p"
			outputGoDir = outputDir+"gprofiler/"

			# 특정 조합의 GO stat 파일 확인
			fr = open(degGoOutputDir+goStatFile,'r')
			headerColumnLst = fr.readline().strip().split('\t')
			intersectionsIndex = headerColumnLst.index("intersections")
			adjPvalueIndex = headerColumnLst.index("adjusted_p_value")
			termNameIndex = headerColumnLst.index("term_name")
			sourceIndex = headerColumnLst.index("source")

			testGroupSampleLst = jsonFileParser.getTestGroupSampleLst()
			controlGroupSampleLst = jsonFileParser.getControlGroupSampleLst()
			data3InfoDic = jsonFileParser.getData3InfoDic()
			totalSampleLst = testGroupSampleLst + controlGroupSampleLst

			os.system(f'mkdir -p {outputGoDir}/{DegGroupDic[data3File]}')
			goDic = {"BP":{}, "MF":{}, "CC":{}}

			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				li = line.strip().split('\t')
				# 조합에 있어서는 안되는 문자열 변경
				termName = li[termNameIndex].replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")

				geneLst = li[intersectionsIndex].split(", ")
				# 유의미한 term만 진행, term에 해당하는 gene이 1개 밖에 없으면 incHlib을 돌릴 수 없음.
				if len(geneLst) <= 1 or float(li[adjPvalueIndex]) > 0.05 :
					continue
				# GO term에 대한 expression profile 결과 생성
				fw = open(f'{outputGoDir}/{DegGroupDic[data3File]}/{termName}.txt','w')
				fw.write("Gene_ID\tN_"+'\tN_'.join(totalSampleLst)+"\t"+DegGroupDic[data3File].replace("_vs_","/")+".fc\t"+DegGroupDic[data3File].replace("_vs_","/")+".raw.pval\t"+DegGroupDic[data3File].replace("_vs_","/")+".bh.pval\t"+DegGroupDic[data3File].replace("_vs_","/")+groupMean+"\n")
				source = li[sourceIndex].split(':')[1]
				goDic[source][termName] = round(float(li[adjPvalueIndex]),3)
				# GO term에 해당하는 gene들을 모두 확인
				for gene in geneLst:
					expressionLst = []
					expressionLst.append(gene)
					for sample in totalSampleLst:
						expressionLst.append(data3InfoDic[gene]["N_"+sample])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".fc"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".raw.pval"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".bh.pval"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+groupMean])
					fw.write('\t'.join(expressionLst)+'\n')
				fw.close()
				inputFormatChanger.addZscore(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				analysis.runIncHlib(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/')
				jsonFileParser.run(f'{termName}.txt', f'{outputGoDir}/{DegGroupDic[data3File]}/', f'{outputGoDir}/{DegGroupDic[data3File]}/', f'{DegGroupDic[data3File]}', degOutputDir+'Sample.Info.txt')
				jsonFileParser.addGroupNameOnHeader(termName)

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
			# 특정 조합의 유의미한 KEGG term을 기반으로한 json 파일 만드는 작업
			degKeggOutputDir = degOutputDir+"KEGG_view/table_p/"
			keggStatFile = "pathway."+data3File[:-3]+"table.p"
			outputKeggDir = outputDir+"KEGG/"

			# 특정 조합의 GO stat 파일 확인
			fr = open(degKeggOutputDir+keggStatFile,'r')
			headerColumnLst = fr.readline().strip().split('\t')
			genesIndex = headerColumnLst.index("Genes")
			PvalueIndex = headerColumnLst.index("PValue")
			mapNameIndex = headerColumnLst.index("MapName")

			testGroupSampleLst = jsonFileParser.getTestGroupSampleLst()
			controlGroupSampleLst = jsonFileParser.getControlGroupSampleLst()
			data3InfoDic = jsonFileParser.getData3InfoDic()
			totalSampleLst = testGroupSampleLst + controlGroupSampleLst

			os.system(f'mkdir -p {outputKeggDir}/{DegGroupDic[data3File]}')
			keggDic = {}

			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				li = line.strip().split('\t')
				# 조합에 있어서는 안되는 문자열 변경
				mapName = li[mapNameIndex].replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")

				keggGeneLst = li[genesIndex].split(", ")
				# 유의미한 term만 진행, term에 해당하는 gene이 1개 밖에 없으면 incHlib을 돌릴 수 없음.
				if len(keggGeneLst) <= 1 or float(li[PvalueIndex]) > 0.05 :
					continue
				# GO term에 대한 expression profile 결과 생성

				fw = open(f'{outputKeggDir}/{DegGroupDic[data3File]}/{mapName}.txt','w')
				fw.write("Gene_ID\tN_"+'\tN_'.join(totalSampleLst)+"\t"+DegGroupDic[data3File].replace("_vs_","/")+".fc\t"+DegGroupDic[data3File].replace("_vs_","/")+".raw.pval\t"+DegGroupDic[data3File].replace("_vs_","/")+".bh.pval\t"+DegGroupDic[data3File].replace("_vs_","/")+groupMean+"\n")

				keggDic[mapName] = round(float(li[PvalueIndex]),3)
				# GO term에 해당하는 gene들을 모두 확인
				for gene in keggGeneLst:
					expressionLst = []
					expressionLst.append(gene)
					for sample in totalSampleLst:
						expressionLst.append(data3InfoDic[gene]["N_"+sample])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".fc"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".raw.pval"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+".bh.pval"])
					expressionLst.append(data3InfoDic[gene][DegGroupDic[data3File].replace("_vs_","/")+groupMean])
					fw.write('\t'.join(expressionLst)+'\n')
				fw.close()
				inputFormatChanger.addZscore(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				analysis.runIncHlib(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/')
				jsonFileParser.run(f'{mapName}.txt', f'{outputKeggDir}/{DegGroupDic[data3File]}/', f'{outputKeggDir}/{DegGroupDic[data3File]}/', f'{DegGroupDic[data3File]}', degOutputDir+'Sample.Info.txt')
				jsonFileParser.addGroupNameOnHeader(mapName)

			os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}')

			# kegg result copy
			for keggMap in keggDic:
				os.system(f'mkdir -p {resultDir}/json/{DegGroupDic[data3File]}/KEGG')
				os.system(f"cp \"{outputKeggDir}/{DegGroupDic[data3File]}/{keggMap}.txt_Final.json\" \"{resultDir}/json/{DegGroupDic[data3File]}/KEGG/{keggMap}.json\"")

			# write kegg html part
			htmlReport.writeKEGGColumn(keggDic, DegGroupDic[data3File], "sub")
		##################kegg end###########################
		# goDic = {"BP":{'acetyltransferase_activity.txt_Final':0.1,'actin_binding.txt_Final':0.2,'antioxidant_activity.txt_Final':0.3,'apical_dendrite.txt_Final':0.4,'arachidonic_acid_metabolic_process.txt_Final':0.5,'ATP_biosynthetic_process.txt_Final':0.6,'ATP_metabolic_process.txt_Final':0.7,'axon_development.txt_Final':0.8,'axon_extension_involved_in_axon_guidance.txt_Final':0.9,'axon_extension.txt_Final':0.10},"CC":{'axon_guidance.txt_Final':0.1,'axonogenesis.txt_Final':0.2,'beta_catenin_TCF_complex_assembly.txt_Final':0.3,'bitter_taste_receptor_activity.txt_Final':0.4,'body_morphogenesis.txt_Final':0.5,'calcium_channel_activity.txt_Final':0.6,'calcium_dependent_phospholipid_binding.txt_Final':0.7,'calcium_ion_binding.txt_Final':0.8,'cargo_receptor_activity.txt_Final':0.9,'cation_channel_activity.txt_Final':0.10},"MF":{'cell_morphogenesis_involved_in_differentiation.txt_Final':0.1,'cell_morphogenesis_involved_in_neuron_differentiation.txt_Final':0.2,'cell_part_morphogenesis.txt_Final':0.3,'cell_projection_morphogenesis.txt_Final':0.4,'cellular_component_morphogenesis.txt_Final':0.5,'cellular_detoxification.txt_Final':0.6,'cellular_oxidant_detoxification.txt_Final':0.7,'cellular_response_to_hormone_stimulus.txt_Final':0.8,'cellular_response_to_lectin.txt_Final':0.9,'cellular_response_to_toxic_substance.txt_Final':0.10}}

		htmlReport.makeHtmlReport(resultDir+"html/"+DegGroupDic[data3File]+".html", DegGroupDic[data3File], "sub")

	if len(DegGroupDic) == 0:
		print(representativeData3Dic)
		data3File = list(representativeData3Dic.keys())[0]
		inputFormatChanger.addZscore(data3File, degOutputDir, outputDir)
		inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(data3File, outputDir)
		analysis.runIncHlib(data3File, outputDir)
		jsonFileParser = JsonFileParser()
		jsonFileParser.run(data3File, degOutputDir, outputDir, representativeData3Dic[data3File], degOutputDir+'Sample.Info.txt')
		jsonFileParser.addGroupNameOnHeader(representativeData3Dic[data3File])

		degGoOutputDir = degOutputDir+"gprofiler/stat.p/"
		goStatFile = data3File[:-3]+"GO.stat.p"
		outputGoDir = outputDir+"gprofiler/"

		if runGprofiler == "yes":
			# 특정 조합의 GO stat 파일 확인
			fr = open(degGoOutputDir+goStatFile,'r')
			headerColumnLst = fr.readline().strip().split('\t')
			intersectionsIndex = headerColumnLst.index("intersections")
			adjPvalueIndex = headerColumnLst.index("adjusted_p_value")
			termNameIndex = headerColumnLst.index("term_name")
			sourceIndex = headerColumnLst.index("source")

			testGroupSampleLst = jsonFileParser.getTestGroupSampleLst()
			controlGroupSampleLst = jsonFileParser.getControlGroupSampleLst()
			data3InfoDic = jsonFileParser.getData3InfoDic()
			totalSampleLst = testGroupSampleLst + controlGroupSampleLst

			os.system(f'mkdir -p {outputGoDir}/{representativeData3Dic[data3File]}')
			goDic = {"BP":{}, "MF":{}, "CC":{}}

			for line in fr:
				# 특정 조합의 GO term을 하나씩 확인
				# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
				li = line.strip().split('\t')
				# 조합에 있어서는 안되는 문자열 변경
				termName = li[termNameIndex].replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")

				geneLst = li[intersectionsIndex].split(", ")
				# 유의미한 term만 진행, term에 해당하는 gene이 1개 밖에 없으면 incHlib을 돌릴 수 없음.
				if len(geneLst) <= 1 or float(li[adjPvalueIndex]) > 0.05 :
					continue
				# GO term에 대한 expression profile 결과 생성
				fw = open(f'{outputGoDir}/{representativeData3Dic[data3File]}/{termName}.txt','w')
				fw.write("Gene_ID\tN_"+'\tN_'.join(totalSampleLst)+"\t"+representativeData3Dic[data3File].replace("_vs_","/")+".fc\t"+representativeData3Dic[data3File].replace("_vs_","/")+".raw.pval\t"+representativeData3Dic[data3File].replace("_vs_","/")+".bh.pval\t"+representativeData3Dic[data3File].replace("_vs_","/")+groupMean+"\n")
				source = li[sourceIndex].split(':')[1]
				goDic[source][termName] = round(float(li[adjPvalueIndex]),3)
				# GO term에 해당하는 gene들을 모두 확인
				for gene in geneLst:
					expressionLst = []
					expressionLst.append(gene)
					for sample in totalSampleLst:
						expressionLst.append(data3InfoDic[gene]["N_"+sample])
					expressionLst.append(data3InfoDic[gene][representativeData3Dic[data3File].replace("_vs_","/")+".fc"])
					expressionLst.append(data3InfoDic[gene][representativeData3Dic[data3File].replace("_vs_","/")+".raw.pval"])
					expressionLst.append(data3InfoDic[gene][representativeData3Dic[data3File].replace("_vs_","/")+".bh.pval"])
					expressionLst.append(data3InfoDic[gene][representativeData3Dic[data3File].replace("_vs_","/")+groupMean])
					fw.write('\t'.join(expressionLst)+'\n')
				fw.close()
				inputFormatChanger.addZscore(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File]}/', f'{outputGoDir}/{representativeData3Dic[data3File]}/')
				inputFormatChanger.convertTxt2CsvFileUsingTargetColumn(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File]}/')
				analysis.runIncHlib(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File]}/')
				jsonFileParser.run(f'{termName}.txt', f'{outputGoDir}/{representativeData3Dic[data3File]}/', f'{outputGoDir}/{representativeData3Dic[data3File]}/', f'{representativeData3Dic[data3File]}', degOutputDir+'Sample.Info.txt')
				jsonFileParser.addGroupNameOnHeader(termName)

			os.system(f'mkdir -p {resultDir}/json/{representativeData3Dic[data3File]}')

			# data3 result copy
			os.system(f"cp \"{outputDir}/{data3File}_Final.json\" \"{resultDir}/json/data3_{representativeData3Dic[data3File]}.json\"")

			# go result copy
			for source in goDic:
				if len(goDic[source]) < 1:
					continue
				os.system(f'mkdir -p {resultDir}/json/{representativeData3Dic[data3File]}/{source}')
				for termName in goDic[source]:
					os.system(f"cp \"{outputGoDir}/{representativeData3Dic[data3File]}/{termName}.txt_Final.json\" \"{resultDir}/json/{representativeData3Dic[data3File]}/{source}/{termName}.json\"")

		# goDic = {"BP":{'acetyltransferase_activity.txt_Final':0.1,'actin_binding.txt_Final':0.2,'antioxidant_activity.txt_Final':0.3,'apical_dendrite.txt_Final':0.4,'arachidonic_acid_metabolic_process.txt_Final':0.5,'ATP_biosynthetic_process.txt_Final':0.6,'ATP_metabolic_process.txt_Final':0.7,'axon_development.txt_Final':0.8,'axon_extension_involved_in_axon_guidance.txt_Final':0.9,'axon_extension.txt_Final':0.10},"CC":{'axon_guidance.txt_Final':0.1,'axonogenesis.txt_Final':0.2,'beta_catenin_TCF_complex_assembly.txt_Final':0.3,'bitter_taste_receptor_activity.txt_Final':0.4,'body_morphogenesis.txt_Final':0.5,'calcium_channel_activity.txt_Final':0.6,'calcium_dependent_phospholipid_binding.txt_Final':0.7,'calcium_ion_binding.txt_Final':0.8,'cargo_receptor_activity.txt_Final':0.9,'cation_channel_activity.txt_Final':0.10},"MF":{'cell_morphogenesis_involved_in_differentiation.txt_Final':0.1,'cell_morphogenesis_involved_in_neuron_differentiation.txt_Final':0.2,'cell_part_morphogenesis.txt_Final':0.3,'cell_projection_morphogenesis.txt_Final':0.4,'cellular_component_morphogenesis.txt_Final':0.5,'cellular_detoxification.txt_Final':0.6,'cellular_oxidant_detoxification.txt_Final':0.7,'cellular_response_to_hormone_stimulus.txt_Final':0.8,'cellular_response_to_lectin.txt_Final':0.9,'cellular_response_to_toxic_substance.txt_Final':0.10}}
		htmlReport = HtmlReport()
		htmlReport.writeGoColumn(goDic, representativeData3Dic[data3File], "main")
		htmlReport.makeHtmlReport(resultDir+representativeData3Dic[data3File]+".html", representativeData3Dic[data3File], "main")


def getDegGroupInfo(inputDir, degOutputDir):
	DegGroupDic = {}
	representativeData3Dic = {}
	fileList = os.popen(f'ls {degOutputDir}').read().split('\n')
	for file in fileList:
		if file.startswith('data3') and file.endswith('txt'):
			comparisonGroup = file.split('data3_')[1].split('_fc')[0]
			# data3_fc2_&_raw.p.txt
			if comparisonGroup.startswith('fc'):
				fr = open(inputDir+file , 'r')
				headerColumnLst = fr.readline().strip().split('\t')
				for headerColumn in headerColumnLst:
					if headerColumn.endswith(".fc"):
						representativeData3Dic[file] = headerColumn.split('.fc')[0].replace("/","_vs_")
						break
				continue
			DegGroupDic[file] = comparisonGroup
	return DegGroupDic, representativeData3Dic

def main():
	run()

if __name__ == '__main__':
	main()
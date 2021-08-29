import numpy as np

class InputFormatChanger:
	__GENE_ID_COLUMN = "Gene_ID"
	__NORMALIZED_EXPRESSION_VALUE = "N_"
	__Z_SCORE_VALUE = "Z_"

	def addZscore(self, inputFile, inputDir, outputDir):
		fr = open(inputDir+inputFile, 'r')
		fw = open(outputDir+inputFile+"_AddZscore.txt",'w')
		headerlst = fr.readline().strip().split('\t')
		targetIndexLst = []
		resultHeaderLst = []
		for index, header in enumerate(headerlst):
			if header.startswith(self.__NORMALIZED_EXPRESSION_VALUE):
				targetIndexLst.append(index)
				resultHeaderLst.append(header.replace("N_","Z_"))
		headerlst += resultHeaderLst

		fw.write('\t'.join(headerlst)+'\n')

		for line in fr:
			targetLi = []
			li = line.strip().split('\t')
			for index, column in enumerate(li):
				if index in targetIndexLst:
					targetLi.append(column)

			totalMean = np.mean(list(map(float,targetLi)))
			totalStd = np.std(list(map(float,targetLi)))
			zScoreLst = []

			for n_value in targetLi:
				sample_z_score = (float(n_value) - totalMean)/totalStd
				zScoreLst.append(str(sample_z_score))
			li = li + zScoreLst
			fw.write('\t'.join(li)+'\n')

	def convertTxt2CsvFileUsingTargetColumn(self, inputFile, outputDir):
		fr = open(outputDir+inputFile+"_AddZscore.txt",'r')
		# fw = open('/mnt/garnet/Analysis/BI/RNA-Seq/HN00153743/DEG/Output/inputOfInchlib.txt','w')
		fw = open(outputDir+inputFile+".csv",'w')
		headerlst = fr.readline().strip().split('\t')
		targetIndexLst = []
		resultHeaderLst = []
		for index, header in enumerate(headerlst):
			if header == self.__GENE_ID_COLUMN :
				targetIndexLst.append(index)
				resultHeaderLst.append(header)
			elif header.startswith(self.__Z_SCORE_VALUE):
				targetIndexLst.append(index)
				resultHeaderLst.append(header)

		fw.write(','.join(resultHeaderLst)+'\n')
		for line in fr:
			targetLi = []
			li = line.strip().split('\t')
			for index, column in enumerate(li):
				if index in targetIndexLst:
					targetLi.append(column)
			fw.write(','.join(targetLi)+'\n')

		fw.close()
		fr.close()





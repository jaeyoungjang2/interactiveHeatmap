class KEGG:
	def __init__(self, data3InfoDic, groupMean, totalSampleLst):
		self.data3InfoDic = data3InfoDic
		self.groupMean = groupMean
		self.totalSampleLst = totalSampleLst

	def findTargetIndex(self, keggStatFile):
		fr = open(keggStatFile,'r')
		headerColumnLst = fr.readline().strip().split('\t')
		self.genesIndex = headerColumnLst.index("Genes")
		self.PvalueIndex = headerColumnLst.index("PValue")
		self.mapNameIndex = headerColumnLst.index("MapName")
		fr.close()

	def isValidKeggTerm(self, line):
		self.li = line.strip().split('\t')
		# 특정 조합의 GO term을 하나씩 확인
		# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
		# term에 있어서는 안되는 문자열 변경
		self.mapName = self.li[self.mapNameIndex].replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")

		self.keggGeneLst = self.li[self.genesIndex].split(", ")
		# 유의미한 term만 진행, term에 해당하는 gene이 1개 밖에 없으면 incHlib을 돌릴 수 없음.
		if len(self.keggGeneLst) <= 1 or float(self.li[self.PvalueIndex]) > 0.05 :
			return False
		return True

	def makeKeggData3File(self, degGroup, keggTermData3FileDir, keggDic):

		fw = open(f'{keggTermData3FileDir}/{self.mapName}.txt','w')
		# fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+"Gene_Symbol\t"+"Description\t"+"gene_biotype\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		keggDic[self.mapName] = round(float(self.li[self.PvalueIndex]),3)
		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.keggGeneLst:
			expressionLst = []
			expressionLst.append(gene)
			for sample in self.totalSampleLst:
				expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".raw.pval"])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".bh.pval"])
			expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
			expressionLst.append(self.data3InfoDic[gene]["Description"])
			expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])
			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()

		return keggDic

	def makeKeggData3File2(self, degGroupLst, keggTermData3FileDir, keggDic):

		fw = open(f'{keggTermData3FileDir}/{self.mapName}.txt','w')
		header = ["Gene_ID"] + ["N_"+sample for sample in self.totalSampleLst]

		keggDic[self.mapName] = round(float(self.li[self.PvalueIndex]),3)

		for degGroup in degGroupLst:
			header.append(degGroup.replace("_vs_","/")+".fc")
			header.append(degGroup.replace("_vs_","/")+".raw.pval")
			header.append(degGroup.replace("_vs_","/")+".bh.pval")
			header.append("Gene_Symbol")
			header.append("Description")
			header.append("gene_biotype")
			header.append(degGroup.replace("_vs_","/")+self.groupMean)

		fw.write('\t'.join(header)+'\n')

		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.keggGeneLst:
			expressionLst = []
			expressionLst.append(gene)
			for sample in self.totalSampleLst:
				expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			for degGroup in degGroupLst:
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".raw.pval"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".bh.pval"])
				expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
				expressionLst.append(self.data3InfoDic[gene]["Description"])
				expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])

			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()
		return keggDic

	def makeKeggQuantileExceptPvalFile(self, degGroup, keggTermData3FileDir, keggDic):

		fw = open(f'{keggTermData3FileDir}/{self.mapName}.txt','w')
		# fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+"Gene_Symbol\t"+"Description\t"+"gene_biotype\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		keggDic[self.mapName] = round(float(self.li[self.PvalueIndex]),3)
		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.keggGeneLst:
			expressionLst = []
			expressionLst.append(gene)
			for sample in self.totalSampleLst:
				expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
			expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
			expressionLst.append(self.data3InfoDic[gene]["Description"])
			expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
			expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])
			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()

		return keggDic

	def makeKeggQuantileExceptPvalFile2(self, degGroupLst, keggTermData3FileDir, keggDic):

		fw = open(f'{keggTermData3FileDir}/{self.mapName}.txt','w')
		header = ["Gene_ID"] + ["N_"+sample for sample in self.totalSampleLst]

		keggDic[self.mapName] = round(float(self.li[self.PvalueIndex]),3)

		for degGroup in degGroupLst:
			header.append(degGroup.replace("_vs_","/")+".fc")
			header.append("Gene_Symbol")
			header.append("Description")
			header.append("gene_biotype")
			header.append(degGroup.replace("_vs_","/")+self.groupMean)

		fw.write('\t'.join(header)+'\n')

		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.keggGeneLst:
			expressionLst = []
			expressionLst.append(gene)
			for sample in self.totalSampleLst:
				expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			for degGroup in degGroupLst:
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
				expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
				expressionLst.append(self.data3InfoDic[gene]["Description"])
				expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])

			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()
		return keggDic

	def getMapName(self):
		return self.mapName
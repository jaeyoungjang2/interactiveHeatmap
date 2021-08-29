class Gprofiler:
	def __init__(self, data3InfoDic, groupMean, totalSampleLst):
		self.data3InfoDic = data3InfoDic
		self.groupMean = groupMean
		self.totalSampleLst = totalSampleLst

	def findTargetIndex(self, goStatFile):
		fr = open(goStatFile,'r')
		headerColumnLst = fr.readline().strip().split('\t')
		self.intersectionsIndex = headerColumnLst.index("intersections")
		self.adjPvalueIndex = headerColumnLst.index("adjusted_p_value")
		self.termNameIndex = headerColumnLst.index("term_name")
		self.sourceIndex = headerColumnLst.index("source")
		fr.close()

	def isValidGoTerm(self, line):
		self.li = line.strip().split('\t')
		# 특정 조합의 GO term을 하나씩 확인
		# termname 마다 조합에 해당하는 샘플에 관한 expression 파일을 생성
		# 조합에 있어서는 안되는 문자열 변경
		self.termName = self.li[self.termNameIndex].replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")
		self.geneLst = self.li[self.intersectionsIndex].split(", ")
		# 유의미한 term만 진행, term에 해당하는 gene이 1개 밖에 없으면 incHlib을 돌릴 수 없음.
		if len(self.geneLst) <= 1 or float(self.li[self.adjPvalueIndex]) > 0.05 :
			return False
		return True


	def makeGoData3File(self, goTermData3FileDir, degGroup, goDic):
		# GO term에 대한 expression profile 결과 생성
		fw = open(goTermData3FileDir+self.termName+'.txt','w')
		# fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+"Gene_Symbol\t"+"Description\t"+"gene_biotype\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		source = self.li[self.sourceIndex].split(':')[1]
		goDic[source][self.termName] = round(float(self.li[self.adjPvalueIndex]),3)
		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.geneLst:
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
		return goDic

	def makeGoData3File2(self, goTermData3FileDir, degGroupLst, goDic):
		# GO term에 대한 expression profile 결과 생성
		# geneid, 샘플별 expression 결과 값, fc, raw.pval. bh.val
		fw = open(goTermData3FileDir+self.termName+'.txt','w')
		header = ["Gene_ID"] + ["N_"+sample for sample in self.totalSampleLst]

		source = self.li[self.sourceIndex].split(':')[1]
		goDic[source][self.termName] = round(float(self.li[self.adjPvalueIndex]),3)

		for degGroup in degGroupLst:
			header.append(degGroup.replace("_vs_","/")+".fc")
			header.append(degGroup.replace("_vs_","/")+".raw.pval")
			header.append(degGroup.replace("_vs_","/")+".bh.pval")
			header.append("Gene_Symbol")
			header.append("Description")
			header.append("gene_biotype")
			header.append(degGroup.replace("_vs_","/")+self.groupMean)

		fw.write('\t'.join(header)+'\n')

		for gene in self.geneLst:
			expressionLst = []
			expressionLst.append(gene)
			# GO term에 해당하는 gene들을 모두 확인
			for sample in self.totalSampleLst:
					# 샘플별 발현값을 저장하고
					expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			for degGroup in degGroupLst:
				# 조합별 정보를 저장한다.
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".raw.pval"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".bh.pval"])
				expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
				expressionLst.append(self.data3InfoDic[gene]["Description"])
				expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])

			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()
		return goDic

	def makeGoQuantileExceptPvalFile(self, goTermData3FileDir, degGroup, goDic):
		# GO term에 대한 expression profile 결과 생성
		fw = open(goTermData3FileDir+self.termName+'.txt','w')
		# fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+degGroup.replace("_vs_","/")+".raw.pval\t"+degGroup.replace("_vs_","/")+".bh.pval\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		fw.write("Gene_ID\tN_"+'\tN_'.join(self.totalSampleLst)+"\t"+degGroup.replace("_vs_","/")+".fc\t"+"Gene_Symbol\t"+"Description\t"+"gene_biotype\t"+degGroup.replace("_vs_","/")+self.groupMean+"\n")
		source = self.li[self.sourceIndex].split(':')[1]
		goDic[source][self.termName] = round(float(self.li[self.adjPvalueIndex]),3)
		# GO term에 해당하는 gene들을 모두 확인
		for gene in self.geneLst:
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
		return goDic

	def makeGoQuantileExceptPvalFile2(self, goTermData3FileDir, degGroupLst, goDic):
		# GO term에 대한 expression profile 결과 생성
		# geneid, 샘플별 expression 결과 값, fc, raw.pval. bh.val
		fw = open(goTermData3FileDir+self.termName+'.txt','w')
		header = ["Gene_ID"] + ["N_"+sample for sample in self.totalSampleLst]

		source = self.li[self.sourceIndex].split(':')[1]
		goDic[source][self.termName] = round(float(self.li[self.adjPvalueIndex]),3)

		for degGroup in degGroupLst:
			header.append(degGroup.replace("_vs_","/")+".fc")
			header.append("Gene_Symbol")
			header.append("Description")
			header.append("gene_biotype")
			header.append(degGroup.replace("_vs_","/")+self.groupMean)

		fw.write('\t'.join(header)+'\n')

		for gene in self.geneLst:
			expressionLst = []
			expressionLst.append(gene)
			# GO term에 해당하는 gene들을 모두 확인
			for sample in self.totalSampleLst:
					# 샘플별 발현값을 저장하고
					expressionLst.append(self.data3InfoDic[gene]["N_"+sample])
			for degGroup in degGroupLst:
				# 조합별 정보를 저장한다.
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+".fc"])
				expressionLst.append(self.data3InfoDic[gene]["Gene_Symbol"])
				expressionLst.append(self.data3InfoDic[gene]["Description"])
				expressionLst.append(self.data3InfoDic[gene]["gene_biotype"])
				expressionLst.append(self.data3InfoDic[gene][degGroup.replace("_vs_","/")+self.groupMean])

			fw.write('\t'.join(expressionLst)+'\n')
		fw.close()
		return goDic

	def getTermName(self):
		return self.termName

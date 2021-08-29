import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.abspath(os.path.dirname(__file__)))))

from config.__config__ import program as pg

class Analysis:
	def __init__(self):
		self.getConfig()
	def getConfig(self):
		self.INCHLIB_SCRIPT = pg["INCHLIB_SCRIPT_PATH"]
	def runIncHlib(self, data3File, outputDir):
		# cmd = f"python {self.INCHLIB_SCRIPT} /mnt/garnet/Analysis/BI/RNA-Seq/HN00153743/DEG/Output/inputOfInchlib.txt -dh -o /mnt/garnet/Analysis/BI/RNA-Seq/HN00153743/DEG/Output/outputOfInchlib.json"
		data3File = data3File.replace("/","_")
		cmd = f'python {self.INCHLIB_SCRIPT} \"{outputDir+data3File}.csv\" -dh -o \"{outputDir+data3File}_Inchlib_output.json\"'
		os.system(cmd)
#!/usr/bin/python

import os
import subprocess
import csv
import statistics
from math import isnan

inputHierarchies=r"U:\calculateHierarchical\set"
outputVisualisations=r"U:\calculateHierarchical\set00\res"
hierarchyVisualisationJarPath=r"U:\calculateHierarchical\hierarchy_visualisator18.jar"
java_executable_path=r'C:\Program Files\Java\jre1.8.0_111\bin\java.exe'

print("Hello, Python!")

if not os.path.exists(outputVisualisations):
	os.makedirs(outputVisualisations)

numChildPerNode = []
stdevNumChildPerNode = []
numChildPerInternalNode = []
stdevNumChildPerInternalNode = []
numChildPerBranchingFactorNode = []
stdevNumChildPerBranchingFactorNode = []
numInstancesPerNode = []
stdevNumInstancesPerNode = []
height = []
widthPerLevel = []
stdevWidthPerLevel = []
numNodes = []
numInternalNodes = []
numBranchingFactorNodes = []
numOfLeaves = []
pathLength = []
stdevPathLength = []
eachLevelNumberOfInstances = []
eachLevelAvgNumberOfChildPerNode = []
eachLevelStdevNumberOfChildPerNode = []
eachLevelHierarchyWidth = []
eachLevelNumberOfLeaves = []
branchingFactorWithAvgCountHistogram = dict()

for root, dirs, files in os.walk(inputHierarchies):
	for file in files:
		if file.endswith(".csv"):#########################################################################ZMIENIAJ MIEDZY CSV aA R.CSV
			#print(os.path.join(root, file))
			print(file)
			datasetName=file[:-4]
			inputPath=os.path.join(root, file)
			outputPath=os.path.join(outputVisualisations, datasetName)
#			args = ['java.exe', '-jar', 'ONE_CLUSTER_hierarchy_measures.jar', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_000.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_001.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_002.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_003.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_004.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_005.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_006.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_007.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_008.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_009.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_010.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_011.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_012.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_013.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_014.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_015.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_016.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_017.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_018.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_019.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_020.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_021.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_022.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_023.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_024.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_025.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_026.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_027.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_028.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_029.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_030.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_031.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_032.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_033.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_034.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_035.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_036.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_037.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_038.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_039.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_040.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_041.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_042.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_043.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_044.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_045.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_046.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_047.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_048.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_049.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_050.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_051.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_052.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_053.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_054.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_055.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_056.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_057.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_058.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_059.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_060.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_061.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_062.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_063.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_064.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_065.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_066.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_067.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_068.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_069.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_070.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_071.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_072.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_073.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_074.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_075.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_076.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_077.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_078.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_079.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_080.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_081.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_082.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_083.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_084.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_085.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_086.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_087.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_088.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_089.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_090.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_091.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_092.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_093.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_094.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_095.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_096.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_097.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_098.gt.csv', r'..\generated_datasets\set06\set06_a-25_l-05_g-02_N-1000_d-3_P-1_Q-5_minSD-005_maxSd-10_099.gt.csv']
#subprocess.run(args, executable=java_executable_path)
			result = subprocess.run(['java', '-jar', hierarchyVisualisationJarPath, '-i', inputPath, '-o', outputPath, '-c', '-sv'], executable=java_executable_path)

			if result.returncode != 0:
				print("Executed hierarchy visualisation jar returned with non zero exit code. Skipping.")
			else:
				for visRoot, visDirs, visFiles in os.walk(outputPath):
					for visStats in visFiles:
						if visStats.endswith("_hieraryStatistics.csv"):
							with open(os.path.join(visRoot, visStats), newline='') as csvfile:
								statsReader = csv.reader(csvfile, delimiter=';', quotechar='"')
								rows = [line for line in statsReader]
								for rowIndex in range(len(rows)):
									if rows[rowIndex]:
										if rows[rowIndex][0] == r"Avg num of children per node":
											numChildPerNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Sample stdev num of children per node":
											stdevNumChildPerNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Avg num of children per INTERNAL node":
											numChildPerInternalNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Sample stdev num of children per INTERNAL node":
											stdevNumChildPerInternalNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0].startswith("Avg num of children per INTERNAL node with MIN BRANCHING FACTOR"):
											numChildPerBranchingFactorNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0].startswith("Sample stdev num of children per INTERNAL node with MIN BRANCHING FACTOR"):
											stdevNumChildPerBranchingFactorNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Avg num of instances per node":
											numInstancesPerNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Sample stdev num of instances per node":
											stdevNumInstancesPerNode.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Hierarchy height":
											height.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Avg hierarchy width":
											widthPerLevel.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Sample stdev hierarchy width":
											stdevWidthPerLevel.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Number of nodes":
											numNodes.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Number of INTERNAL nodes":
											numInternalNodes.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0].startswith("Number of INTERNAL nodes with MIN BRANCHING FACTOR"):
											numBranchingFactorNodes.append(float(rows[rowIndex][1]))	
										elif rows[rowIndex][0] == r"Number of leaves":
											numOfLeaves.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Avg path length":
											pathLength.append(float(rows[rowIndex][1]))
										elif rows[rowIndex][0] == r"Sample stdev path length":
											stdevPathLength.append(float(rows[rowIndex][1]))
										elif len(rows[rowIndex]) == 7 and rows[rowIndex][0] == r"Level" and rows[rowIndex][1] == r"No Inst" and  rows[rowIndex][2] == r"% Inst" and rows[rowIndex][3] == r"Avg. No of Children per node" and rows[rowIndex][4] == r"Stdev" and rows[rowIndex][5] == r"Hierarchy width" and rows[rowIndex][6] == r"No of leaves":
											for histogramRow in rows[rowIndex+1:]:
												if len(histogramRow) < 7:
													break
												heightNumber = int(histogramRow[0])
												if len(eachLevelNumberOfInstances) < (heightNumber+1):
													eachLevelNumberOfInstances.append([])
												eachLevelNumberOfInstances[heightNumber].append(int(histogramRow[1]))
												
												if len(eachLevelAvgNumberOfChildPerNode) < (heightNumber+1):
													eachLevelAvgNumberOfChildPerNode.append([])
												eachLevelAvgNumberOfChildPerNode[heightNumber].append(float(histogramRow[3]))
												
												if len(eachLevelStdevNumberOfChildPerNode) < (heightNumber+1):
													eachLevelStdevNumberOfChildPerNode.append([])
												eachLevelStdevNumberOfChildPerNode[heightNumber].append(float(histogramRow[4]))
												
												if len(eachLevelHierarchyWidth) < (heightNumber+1):
													eachLevelHierarchyWidth.append([])
												eachLevelHierarchyWidth[heightNumber].append(float(histogramRow[5]))
												
												if len(eachLevelNumberOfLeaves) < (heightNumber+1):
													eachLevelNumberOfLeaves.append([])
												eachLevelNumberOfLeaves[heightNumber].append(float(histogramRow[6]))
												
										elif rows[rowIndex][0] == r"Branching factor histogram":
											for elem in zip(rows[rowIndex+1][1:], rows[rowIndex+2][1:]):
												if elem[0] in branchingFactorWithAvgCountHistogram:
													branchingFactorWithAvgCountHistogram[elem[0]] += float(elem[1])
												else:
													branchingFactorWithAvgCountHistogram[elem[0]] = float(elem[1])
with open(os.path.join(outputVisualisations, 'summaryResults.csv'), 'w', newline='') as csvfile:

	numChildPerNode = [0 if isnan(x) else x for x in numChildPerNode]
	stdevNumChildPerNode = [0 if isnan(x) else x for x in stdevNumChildPerNode]
	numChildPerInternalNode = [0 if isnan(x) else x for x in numChildPerInternalNode]
	stdevNumChildPerInternalNode = [0 if isnan(x) else x for x in stdevNumChildPerInternalNode]
	numChildPerBranchingFactorNode = [0 if isnan(x) else x for x in numChildPerBranchingFactorNode]
	stdevNumChildPerBranchingFactorNode = [0 if isnan(x) else x for x in stdevNumChildPerBranchingFactorNode]
	numInstancesPerNode = [0 if isnan(x) else x for x in numInstancesPerNode]
	stdevNumInstancesPerNode = [0 if isnan(x) else x for x in stdevNumInstancesPerNode]
	height = [0 if isnan(x) else x for x in height]
	widthPerLevel = [0 if isnan(x) else x for x in widthPerLevel]
	stdevWidthPerLevel = [0 if isnan(x) else x for x in stdevWidthPerLevel]
	numNodes = [0 if isnan(x) else x for x in numNodes]
	numInternalNodes = [0 if isnan(x) else x for x in numInternalNodes]
	numBranchingFactorNodes = [0 if isnan(x) else x for x in numBranchingFactorNodes]
	numOfLeaves = [0 if isnan(x) else x for x in numOfLeaves]
	pathLength = [0 if isnan(x) else x for x in pathLength]
	stdevPathLength = [0 if isnan(x) else x for x in stdevPathLength]
	
	resWriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	resWriter.writerow(["Avg of avg num of children per node", statistics.mean(numChildPerNode), "avg st.dev", statistics.mean(stdevNumChildPerNode)])
	resWriter.writerow(["Avg of avg num of children per INTERNAL node", statistics.mean(numChildPerInternalNode), "avg st.dev", statistics.mean(stdevNumChildPerInternalNode)])
	resWriter.writerow(["Avg of avg num of children per INTERNAL node with MIN BRANCHING FACTOR", statistics.mean(numChildPerBranchingFactorNode), "avg st.dev", statistics.mean(stdevNumChildPerBranchingFactorNode)])
	resWriter.writerow(["Avg of avg num of instances per node", statistics.mean(numInstancesPerNode), "avg st.dev", statistics.mean(stdevNumInstancesPerNode)])
	resWriter.writerow(["Avg hierarchy height", statistics.mean(height), "st.dev", statistics.stdev(height)])
	resWriter.writerow(["Avg of avg hierarchy width", statistics.mean(widthPerLevel), "avg st.dev", statistics.mean(stdevWidthPerLevel)])
	resWriter.writerow(["Avg number of nodes", statistics.mean(numNodes), "st.dev", statistics.stdev(numNodes)])
	resWriter.writerow(["Avg number of INTERNAL nodes", statistics.mean(numInternalNodes), "st.dev", statistics.stdev(numInternalNodes)])
	resWriter.writerow(["Avg number of INTERNAL nodes with MIN BRANCHING FACTOR", statistics.mean(numBranchingFactorNodes), "st.dev", statistics.stdev(numBranchingFactorNodes)])
	resWriter.writerow(["Avg number of leaves", statistics.mean(numOfLeaves), "st.dev", statistics.stdev(numOfLeaves)])
	resWriter.writerow(["Avg of avg path length", statistics.mean(pathLength), "avg st.dev", statistics.mean(stdevPathLength)])
	resWriter.writerow([])
	resWriter.writerow(["Avg values per each tree level"])
	
	numberOfParsedResultFiles = 0;
	for i in range(len(eachLevelNumberOfInstances)):
		numberOfParsedResultFiles = max(numberOfParsedResultFiles, len(eachLevelNumberOfInstances[i]), len(eachLevelAvgNumberOfChildPerNode[i]), len(eachLevelStdevNumberOfChildPerNode[i]), len(eachLevelHierarchyWidth[i]), len(eachLevelNumberOfLeaves[i]))
		
											
	for key, val in branchingFactorWithAvgCountHistogram.items():
		branchingFactorWithAvgCountHistogram[key] = val / numberOfParsedResultFiles
	
	for i in range(len(eachLevelNumberOfInstances)):
		eachLevelNumberOfInstances[i].extend([0] * (numberOfParsedResultFiles - len(eachLevelNumberOfInstances[i])))
		eachLevelAvgNumberOfChildPerNode[i].extend([0] * (numberOfParsedResultFiles - len(eachLevelAvgNumberOfChildPerNode[i])))
		eachLevelStdevNumberOfChildPerNode[i].extend([0] * (numberOfParsedResultFiles - len(eachLevelStdevNumberOfChildPerNode[i])))
		eachLevelHierarchyWidth[i].extend([0] * (numberOfParsedResultFiles - len(eachLevelHierarchyWidth[i])))
		eachLevelNumberOfLeaves[i].extend([0] * (numberOfParsedResultFiles - len(eachLevelNumberOfLeaves[i])))
		
	resWriter.writerow([])
	resWriter.writerow(["Level", "Avg num of Inst", "stdev", "Avg of Avg. No of Children per node", "Avg of stdev", "Avg of Hierarchy width", "stdev", "Avg number of leaves", "stdev"])
	for i in range(len(eachLevelNumberOfInstances)):
		resWriter.writerow([i, statistics.mean(eachLevelNumberOfInstances[i]), statistics.stdev(eachLevelNumberOfInstances[i]), statistics.mean(eachLevelAvgNumberOfChildPerNode[i]), statistics.mean(eachLevelStdevNumberOfChildPerNode[i]), statistics.mean(eachLevelHierarchyWidth[i]), statistics.stdev(eachLevelHierarchyWidth[i]), statistics.mean(eachLevelNumberOfLeaves[i]), statistics.stdev(eachLevelNumberOfLeaves[i])])
	
	resWriter.writerow([])
	resWriter.writerow(["Avg Branching factor histogram:"])
	factor = ["Factor:"]
	avgCount = ["Avg. Count:"]
	for key, val in sorted(branchingFactorWithAvgCountHistogram.items()):
		factor.append(key)
		avgCount.append(val)
	resWriter.writerow(factor)
	resWriter.writerow(avgCount)

# print("numChildPerNode")
# print(numChildPerNode)
# print("numChildPerInternalNode")
# print(numChildPerInternalNode)
# print("numChildPerBranchingFactorNode")
# print(numChildPerBranchingFactorNode)
# print("MEAN AND STDEV:")
# print(statistics.mean(numChildPerBranchingFactorNode))
# print(statistics.stdev(numChildPerBranchingFactorNode))
# print("numInstancesPerNode")
# print(numInstancesPerNode)
# print("height")
# print(height)
# print("numNodes")
# print(numNodes)
# print("numInternalNodes")
# print(numInternalNodes)
# print("numBranchingFactorNodes")
# print(numBranchingFactorNodes)
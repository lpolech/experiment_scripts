#!/usr/local/bin/python3.6

import os
import subprocess

folder_with_input_hierarchies=r"/home/lolech/archive/adobe_17_04_05"
hierarchy_measure_jar=r"/home/lolech/measures/hierarchy_measures.jar"
java_executable_path=r'/usr/bin'

print("Hello, Python!")
input_hierarchies = []

for root, dirs, files in os.walk(folder_with_input_hierarchies):
	for file in files:
		if file == "finalHierarchyOfGroups.csv":
			#input_hierarchies.append(os.path.join(root, file))
			result = subprocess.run(['java', '-jar', hierarchy_measure_jar, os.path.join(root, file)])
			if result.returncode != 0:
				print("Executed hierarchy visualisation jar returned with non zero exit code. Skipping.")

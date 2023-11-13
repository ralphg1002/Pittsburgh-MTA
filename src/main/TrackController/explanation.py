# I have created a PLC.txt file and a parser which takes the txt file and parses the data and completes the operations based on the information provided.
# Currently, It only checks for a single "IF" block. But I would like it so that if there are multiple IF conditions for each switch section like the code I have added after the methods,
# I would like it to first evaluate the condition in the first IF statement and if it evaluates the condition as true, it should not evaluate the second condition in the section IF section (within the same switch section)


# # Define a function to parse the text file
#     def parse_text_file(self, filename):
#         data = []  # List to store the parsed data
#         currentSection = None  # Variable to track the current section
#         insideIf = False  # Flag to indicate if we are inside an IF block
#         condition = None
#         operations = []  # List to store multiple operations

#         with open(filename, "r") as file:
#             for line in file:
#                 line = line.strip()

#                 if line.startswith("SW"):
#                     currentSection = line
#                 elif line == "IF":
#                     insideIf = True
#                     operations = []  # Initialize operations list for this IF block
#                 elif insideIf and line.startswith("Condition"):
#                     condition = line.split(":")[1].strip()
#                 elif insideIf and line.startswith("Operation"):
#                     operation = line.split(":")[1].strip()
#                     operations.append(operation)
#                 elif line == "END" and insideIf:
#                     data.append(
#                         {
#                             "Section": currentSection,
#                             "Condition": condition,
#                             "Operations": operations,
#                         }
#                     )
#                     insideIf = False

#         return data

# # This is the method that reads the PLC file and runs it accordingly
#     def run_plc(self, plcFilepath):
#         self.plcData = self.plc.parse_text_file(plcFilepath)
#         self.refresh_plc()

#     def refresh_plc(self):
#         # check if it is in manual mode and exit the refresh if so
#         if not self.plcState:
#             return

#         for item in self.plcData:
#             print("Evaluating Section:", item["Section"])
#             print("Condition:", item["Condition"])

#             switchString = item["Section"].rstrip(":")
#             if switchString in self.switches:
#                 # Determine what is the switch block
#                 switchBlock = self.get_block(self.switches[switchString])
#             else:
#                 continue

#             # Parse the condition
#             entry, notExist, exitRange = self.parse_condition(item["Condition"])
#             condition1 = False
#             condition2 = False

#             # check for validity of conditon 1
#             if isinstance(entry, int):
#                 entry = [entry]  # Convert single integer to a list

#             print(entry)

#             if entry != 0:
#                 # check for validity of conditon 1
#                 for block in entry:
#                     if self.get_block(block).get_occupancystate() == True:
#                         condition1 = True
#                         break
#             else:
#                 if self.get_block(0).get_occupancystate() == True:
#                     condition1 = True

#             # check for validity of condition 2
#             for block in exitRange:
#                 if not exitRange:
#                     condition2 = True
#                     break

#                 if self.get_block(block).get_occupancystate() == True:
#                     condition2 = True
#                     break

#             if condition2 == True and notExist:
#                 condition2 = False
#             elif condition2 == False and notExist:
#                 condition2 = True

#             # if both condition 1 and 2 are valid continue to the operations
#             if condition1 and condition2:
#                 # There are only two operations
#                 # Set signal state and set switch state
#                 for operation in item["Operations"]:
#                     parsedOperation = self.parse_operation(operation)
#                     # set the switch value
#                     if parsedOperation["Type"] == "SWITCH":
#                         switchValue = int(parsedOperation["Value"])

#                         switchBlock.set_switchstate(switchValue)
#                         switchBlock.set_switchstate(switchValue)

#                         # emit that a switch value has been changed
#                         trackControllerToTrackModel.switchState.emit(
#                             self.line,
#                             self.waysideNum,
#                             self.switches[switchString],
#                             switchValue,
#                         )

#                     # set the light value
#                     elif parsedOperation["Type"] == "SIGNAL":
#                         signalNumber = parsedOperation["Number"]
#                         print("The number is: " + str(signalNumber))
#                         print("The wayside is: " + str(self.waysideNum))
#                         signalState = parsedOperation["State"]
#                         if signalState == "G":
#                             signalState = "green"
#                         elif signalState == "R":
#                             signalState = "red"

#                         self.get_block(signalNumber).set_lightstate(signalState)
#                         self.get_block(signalNumber).set_lightstate(signalState)
#                         # emit that a light value has been changed
#                         trackControllerToTrackModel.lightState.emit(
#                             self.line, self.waysideNum, signalNumber, signalState
#                         )

#                     #Set the crossing value
#                     elif parsedOperation["Type"] == "CROSS":
#                         crossValue = int(parsedOperation["Value"])
#                         crossNumber = parsedOperation["Number"]

#                         #2x redundancy
#                         self.get_block(crossNumber).set_crosssingstate(crossValue)
#                         self.get_block(crossNumber).set_crosssingstate(crossValue)

#                         # called again after the handler
#                         # emit that a switch value has been changed
#                         trackControllerToTrackModel.crossingState.emit(
#                             self.line,
#                             self.waysideNum,
#                             crossNumber,
#                             switchValue,
#                         )

#         # call the authority function to set authorities throughout the map
#         """
#         This section of code will deal with the authority of the system for each block that is occupied and send it to the track model
#         This will be calculated using block occupancy, light states, and suggested authority from the CTC.
#         """


#     # This is the method that parses the condition of a section within a PLC file
#     def parse_condition(self, condition):
#         entry = []
#         notExist = False
#         exitRange = []

#         # Regular expressions to match the various patterns
#         patternEntry = r"^(\d+)$"
#         patternEntryRange = r"^(\d+)->(\d+)$"
#         patternEntryReverseRange = r"^(\d+)<-(\d+)$"
#         patternExitRange = r"^\((\d+)->(\d+)\)$"
#         patternAndNotExitRange = r"^(\d+) AND NOT\((\d+)->(\d+)\)$"
#         patternAndExitRange = r"^\((\d+)->(\d+)\) AND \((\d+)->(\d+)\)$"
#         patternAndNotReverseExitRange = r"^\((\d+)->(\d+)\) AND NOT\((\d+)->(\d+)\)$"

#         if re.match(patternEntry, condition):
#             entry = [int(condition)]
#         elif re.match(patternEntryRange, condition):
#             match = re.match(patternEntryRange, condition)
#             entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
#         elif re.match(patternEntryReverseRange, condition):
#             match = re.match(patternEntryReverseRange, condition)
#             entry = list(range(int(match.group(1)), int(match.group(2)) - 1, -1))
#         elif re.match(patternExitRange, condition):
#             match = re.match(patternExitRange, condition)
#             exitRange = list(range(int(match.group(1)), int(match.group(2)) + 1))
#         elif re.match(patternAndNotExitRange, condition):
#             match = re.match(patternAndNotExitRange, condition)
#             entry = [int(match.group(1))]
#             notExist = True
#             exitRange = list(range(int(match.group(2)), int(match.group(3)) + 1))
#         elif re.match(patternAndExitRange, condition):
#             match = re.match(patternAndExitRange, condition)
#             exitRange.extend(range(int(match.group(1)), int(match.group(2)) + 1))
#             exitRange.extend(range(int(match.group(3)), int(match.group(4)) + 1))
#         elif re.match(patternAndNotReverseExitRange, condition):
#             match = re.match(patternAndNotReverseExitRange, condition)
#             notExist = True
#             exitRange.extend(range(int(match.group(2)), int(match.group(1)) + 1))
#             exitRange.extend(range(int(match.group(3)), int(match.group(4)) + 1))

#         return entry, notExist, exitRange

#     # This is the method that parses the operation following a condition within a PLC file
#     def parse_operation(self, operationLine):
#         if operationLine.startswith("SWITCH"):
#             switchValue = operationLine.split("(")[1].strip(")")
#             if switchValue in ["0", "1"]:
#                 return {"Type": "SWITCH", "Value": int(switchValue)}
#         elif operationLine.endswith(" G"):
#             return {"Type": "SIGNAL", "Number": operationLine.split()[0], "State": "G"}
#         elif operationLine.endswith(" R"):
#             return {"Type": "SIGNAL", "Number": operationLine.split()[0], "State": "R"}


# The PLC code is as follows:
# SW1:
# IF
#     Condition: (17->12)
#     Operation: SWITCH(0)
#     Operation 11 R
#     Operation 12 G
#     Operation 1 R
# IF
#     Condition: (6->1) AND NOT(29->12)
#     Operation: SWITCH(1)
#     Operation: 11 R
#     Operation: 12 R
#     Operation: 1 G
# END

# SW2:
# IF
#     Condition: (24->29)
#     Operation SWITCH(0)
#     Operation: 150 R
#     Operation: 30 R
#     Operation: 29 G
# IF
#     Condition: (145->150) AND NOT(12->29)
#     Operation: SWITCH(1)
#     Operation: 150 G
#     Operation: 30 R
#     Operation: 29 R
# END

# SW3:
# IF
#     Condition: (52->57)
#     Operation: SWITCH(1)
#     Operation: 57 G
#     Operation: 58 R
# END

# SW4:
# IF
#     Condition: (57->62)
#     Operation: SWITCH(0)
#     Operation: 62 G
#     Operation: 63 R
#     Operation: 0 R
# IF
#     Condition: 0
#     Operation: SWITCH(1)
#     Operation: 62 R
#     Operation: 63 R
# END

# SW5:
# IF
#     Condition: (71->76) AND NOT(85->77)
#     Operation: SWITCH(0)
#     Operation: 76 G
#     Operation: 77 R
#     Operation: 101 R
# IF
#     Condition: (85->77)
#     Operation: SWITCH(1)
#     Operation: 76 R
#     Operation: 77 G
#     Operation: 101 R
# END

# SW6:
# IF
#     Condition: (80->85)
#     Operation: SWITCH(0)
#     Operation: 85 G
#     Operation: 86 R
#     Operation: 100 R
# IF
#     Condition: (95->100) AND NOT(77->85)
#     Operation: SWITCH(1)
#     Operation: 85 R
#     Operation: 86 R
#     Operation: 100 G
# END

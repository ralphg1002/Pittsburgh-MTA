import re

def check_and_extract_entry_range(pattern, condition):
    match = re.match(pattern, condition)
    if match:
        entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
        exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
        return entry, exit
    else:
        return None  # or handle the case when the condition doesn't match

# Example usage:
pattern_entry_range = r"^\((\d+)<-(\d+)\) AND NOT\((\d+)<-(\d+)\)$"
condition = "(1<-6) AND NOT(12<-29)"

entry_result, exit_result = check_and_extract_entry_range(pattern_entry_range, condition)

if entry_result is not None:
    print("Entry:", entry_result)
    print("Exit:", exit_result)
else:
    print("Condition does not match the pattern.")

# ehealth_msgs
Basic HL7 and FHIR observation message generation scripts with predetermined messages.

HOW TO USE

1. run parseRawMsgs.py
2. run pseudoserver.py
3. script input can be changed in client.py on lines 12 through 17; standard -> vital_p
4. input time values and vital parameters are taken from messages or _data_by_id messages
5. output is created in new folders/.txt files
6. example inputs are shown in _example_inputs.txt

KNOWN ISSUES
plots can sometimes seem like they are blank without values, try setting a bigger time interval

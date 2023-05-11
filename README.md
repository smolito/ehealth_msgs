# ehealth_msgs
Basic HL7 and FHIR observation message generation scripts with predetermined messages.

Communication starts with the client sending a message to the server with information about incoming request. Upon receiving the actual request the server looks through files and sends the whole data set. Client then sends message confirming dataset acceptance, closing the socket and creates corresponding files. Server closes when a confirm message comes.

HOW TO USE

1. run parseRawMsgs.py
2. run pseudoserver.py
3. run client.py
4. script input can be changed in client.py on lines 12 through 17; standard -> vital_p variables
5. input time values and vital parameters are taken from _data_by_id messages
6. output is created in new folders/.txt files
7. example inputs are shown in _example_inputs.txt

KNOWN ISSUES
plots can sometimes seem like they are blank without values, try setting a bigger time interval

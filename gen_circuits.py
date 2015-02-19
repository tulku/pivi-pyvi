import json
import sys

help = """
       To use this script:
       1) Edit the description of each pivi and each circuit.
       2) Run it: python gen_circuits.py > circuits.json
       3) Copy the file to aws: scp circuits.json aws-staging:
       4) Ssh to aws: ssh aws-staging
       5) Add the document to the mongo:
       $ mongoimport -d less_database -c circuits --file circuits.json

       To delete all documents first:
       $ mongo localhost:27017/less_database
       > db.circuits.remove({})
       > exit
       """

if sys.argv[1] == '--help':
    print help
    sys.exit(0)

PIVI_BASE_ID = 900

PIVIs = {0: {'location': 'Virtual Device. Random data.'},
         5: {'location': 'Hallway fifth floor.'},
         6: {'location': 'Below server rack fifth floor'},
         7: {'location': 'Below server rack fifth floor'},
         8: {'location': 'Hallway second floor.'},
         9: {'location': 'Below server rack fifth floor'},
         10: {'location': 'Below server rack fifth floor'},
         11: {'location': 'Below server rack fifth floor'}}

CIRCUITS = {0: {1: 'Virtual line 1',
                2: 'Virtual line 2',
                3: 'Virtual line 3',
                4: 'Virtual line 4',
                5: 'Virtual line 5',
                6: 'Virtual line 6'},
            5: {1: 'Non stabilized power outlets',
                2: 'Ceiling lights',
                3: 'Water dispenser and power outlets'}}


for pivi in CIRCUITS:
    for circuit in CIRCUITS[pivi]:
        circuit_id = (PIVI_BASE_ID + pivi)*10 + circuit
        d = {'circuit_id': circuit_id, 'PIVI': pivi, 'line': circuit}
        d['description'] = CIRCUITS[pivi][circuit]
        d.update(PIVIs[pivi])
        print json.dumps(d)

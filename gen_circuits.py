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

if len(sys.argv) > 1 and sys.argv[1] == '--help':
    print help
    sys.exit(0)

PIVI_BASE_ID = 900

PIVIs = {0: {'location': 'Virtual Device. Random data.'},
         1: {'location': 'Hallway fifth floor.'},
         2: {'location': 'Below server rack fifth floor'},
         3: {'location': 'Below server rack fifth floor'},
         4: {'location': 'Hallway second floor.'},
         5: {'location': 'Below server rack fifth floor'},
         6: {'location': 'Below server rack fifth floor'},
         7: {'location': 'Below server rack fifth floor'}}

CIRCUITS = {0: {1: 'Virtual line 1',
                2: 'Virtual line 2',
                3: 'Virtual line 3',
                4: 'Virtual line 4',
                5: 'Virtual line 5',
                6: 'Virtual line 6'},
            1: {3: 'Non stabilized power outlets',
                4: 'Ceiling lights',
                5: 'Water dispenser and power outlets',
                6: 'Bathroom lights'}}


for pivi in CIRCUITS:
    for circuit in CIRCUITS[pivi]:
        circuit_id = (PIVI_BASE_ID + pivi)*10 + circuit
        d = {'circuit_id': circuit_id, 'PIVI': pivi, 'line': circuit}
        d['description'] = CIRCUITS[pivi][circuit]
        d.update(PIVIs[pivi])
        print json.dumps(d)

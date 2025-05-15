# EducationDB
Online Education Platform proyecto for the Non SQL Databases course

## Proyect Structure
/eductaion_db
│
├── main.py                # Entry point, menu/CLI
├── setup.py 
├── models/
│   ├── dgraph_model.py        # Dgraph schema & logic
│   ├── mongo_model.py         # MongoDB schema & logic
│   └── cassandra_model.py     # Cassandra schema & logic
├── db/                    # Connection utilities
│   ├── dgraph_client.py
│   ├── mongo_client.py
│   └── cassandra_client.py
├── .env                   # Store URIs and credentials
└── requirements.txt       # Python dependencies


```
python setup.py
python main.py
```
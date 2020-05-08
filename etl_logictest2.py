import json
import pandas as pd

# See Readme and the following link for details:
# https://gist.github.com/MerlinSp/5fcee579b159e1f3662e75da4a67a60e

def main():
    """INPUTS: 
    * source_file_2.json: file with managers and watcher info and it is a mess.
    OUTUTS
    * managers.json: all projects of that manager ordered by priority
    * watchers.json: all projects of that watcher ordered by priority"""

    with open('source_file_2.json') as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data)

    ROLE = 'watchers'
    with open(ROLE + '.json', 'w') as outfile:
        json.dump(transform(ROLE, extract(ROLE, df), df), outfile)

    ROLE = 'managers'
    with open(ROLE + '.json', 'w') as outfile:
        json.dump(transform(ROLE, extract(ROLE, df), df), outfile)


def extract(role, df):
    all_inthisrole = []
    for i in df.index:
        all_inthisrole += df.loc[i, role]
    return set(all_inthisrole)

def transform(role, all_inthisrole, df):
    role_projects = {}
    for role_i in all_inthisrole:
        aux_role = {}
        aux_role['name'] = []
        aux_role['priority'] = []
        for i in df.index:
            if role_i in df.loc[i,role]:
                aux_role['name'].append(df.name.loc[i])
                aux_role['priority'].append(df.priority.loc[i])
        role_projects[role_i] = pd.DataFrame(aux_role)
    for role_i in role_projects:
        role_projects[role_i] = role_projects[role_i].sort_values(by='priority',ascending=False).name.tolist()
    return role_projects

if __name__ == "__main__":
    main()
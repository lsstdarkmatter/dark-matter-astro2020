#!/usr/bin/env python3
# This requires Python 3 for unicode support

# Export the spreadsheet in tsv format
# https://docs.google.com/spreadsheets/d/15ABUX6cCw6eNijMPS5pm43lI_ySlXRDfsROzT0h3y4E/edit?usp=sharing

# This was challenging to parse with numpy csv reader
#import numpy as np
#data = np.genfromtxt('astro2020_endorsers.tsv', delimiter='\t', skip_header=1, usecols=0)

import pandas as pd
import numpy as np
from collections import OrderedDict as odict

#data = pd.read_csv('astro2020_endorsers.tsv', sep='\t')
data = pd.read_csv('data/astro2020_endorsers_v3.csv')
lsst = pd.read_csv('data/lsstdarkmatter_endorsers_v2.csv')

which_papers = data['Which Decadal Survey Science Submissions are you willing to endorse?']

count = np.char.count(which_papers.tolist(), 'Dark matter constraints with LSST')
cut = (count > 0)

print( np.sum(cut), len(which_papers) )

data = data[cut]
merge = data.merge(lsst,left_on=['Surname','Name'],right_on=['Lastname','Firstname'])

cut = ~np.in1d(data['Surname']+data['Name'],merge['Surname']+merge['Name'])
data = data[cut]

# Other duplicates...
cut = ~np.in1d(data['Surname'],['Slosar','Johann','Drlica-Wagner','Armstrong'])
data = data[cut]

new = pd.DataFrame(odict([("Lastname", data['Surname']),
                          ("Firstname", data['Name']),
                          ("Authorname", data['Latex Name']),
                          ("AuthorType", len(data)*['Supporter']),
                          ("Affiliation", data['LaTeX Affiliation alias(es)']),
                          ("Contribution", len(data)*['Supporter']),
                    ("Email", data['Email Address']),
                    ("ORCID", len(data)*['']),
                ])).sort_values(by='Lastname')

out = lsst.append(new)
print( len(lsst), len(out) )
out.to_csv('astro2020_endorsers_trimmed_merged.csv',index=False)


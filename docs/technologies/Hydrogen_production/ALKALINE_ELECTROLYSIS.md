---
title: Alkaline Electrolysis
---

# Alkaline Electrolysis

## 1: Global Hydrogen Production Overview [^1]

In 2022, global hydrogen production reached nearly 95 Mt, marking a 3%
increase from 2021. This production landscape continued to be dominated
by the unabated use of fossil fuels. Here’s a breakdown:

- **Natural Gas**: Accounting for 62% of the global production,
  natural gas without Carbon Capture, Utilisation, and Storage (CCUS)
  was the primary source.

- **Coal**: Unabated coal, predominantly from China, contributed to
  21% of the worldwide production.

- **By-product Hydrogen**: Refineries and the petrochemical
  industry produced 16% of the global hydrogen as a by-product during
  processes like naphtha reforming. This by-product hydrogen often
  finds use in other conversion processes, including hydrocracking and
  desulphurisation.

Low-emission hydrogen production amounted to less than 1 Mt in 2022,
equating to a mere 0.7% of the global production. This was virtually
unchanged from 2021 and primarily sourced from fossil fuels equipped
with CCUS.

## 2: Introduction

Alkaline electrolysis, a well-established method for hydrogen
production, involves the electrochemical decomposition of water into its
elemental components, hydrogen and oxygen. Highlighting its technical
constituents:

- **Electrolyte**: The process utilizes a solution of potassium
  hydroxide (KOH) or sodium hydroxide (NaOH) as the electrolyte.

- **Electrodes**: Typically made from nickel or its alloys, these
  electrodes are where the actual hydrogen and oxygen evolution
  reactions occur.

- **Reaction Dynamics**: At the cathode, water reduces to generate
  hydrogen gas, while at the anode, water oxidizes to produce oxygen
  gas.

- **Operational Parameters**: Effective operation often requires
  temperatures ranging between 60-80°C with a potential of around
  1.8-2.4 V.[^2] [^3]

- **Efficiency**: Alkaline electrolysis exhibits a cell voltage
  efficiency of approximately 60-70%, though advanCement Prod.s aim to
  enhance this metric.[^3]

## 3: Global Deployment [^1]

Water electrolysis, often simply termed as electrolysis, while currently
contributing to only about 0.1% of the global hydrogen production, has
been witnessing a significant growth in terms of installed capacity and
announced projects.

- **Production in 2022**: Production from electrolysis was still below
  100 kt H~2~ in 2022, albeit this showcased a promising growth of 35%
  compared to the prior year.

- **Installed Capacity and Projects**: As of the end of 2022, the
  worldwide installed capacity for hydrogen production through water
  electrolysis was nearing 700 MW, reflecting a 20% increment from the
  previous year. Furthermore, around 600 projects boasting a combined
  capacity exceeding 160 GW have been announced post the Global
  Hydrogen Review (GHR) in 2022.

- **Electrolyser Types**: By the culmination of 2022, alkaline
  electrolysers made up 60% of the installed capacity. This was
  followed by Proton Exchange Membrane (PEM) electrolysers accounting
  for around 30%. However, based on project announCement Prod.s, PEM
  is anticipated to overtake alkaline electrolysers in market share in
  the foreseeable future. It’s notable that many upcoming projects
  remain undecided or undisclosed regarding their choice of
  electrolyser technology.

While alkaline electrolysis has been utilized for nearly a century for
large-scale hydrogen production, recent emphasis on clean energy and the
hydrogen economy has revitalized interest in this technology. It is the
most mature and widely used electrolysis technology on the market today,
accounting for the majority of installed electrolysis capacity globally.

## 4: Use in Quebec and Canada

### Quebec

Quebec, with its abundant hydroelectric resources, presents an ideal
landscape for green hydrogen production using alkaline electrolysis.
There’s a growing interest in harnessing this potential[^1] and several
projects, both in pilot and commercial scales, are under consideration
or development. [^5]

### Canada

Nationally, Canada recognizes the strategic importance of hydrogen as a
clean energy vector. As a part of the broader Canadian hydrogen
strategy, alkaline electrolysis features prominently due to its maturity
and adaptability. Several industries, especially those in regions with
plentiful renewable electricity, are exploring the integration of
alkaline electrolyzers for hydrogen production, aiming for a
decarbonized industrial future. [^4]

## ES Model Parameters

All the parameters concerning the Alkaline Electrolysis are listed in
the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='ALKALINE_ELECTROLYSIS'))

```

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='ALKALINE_ELECTROLYSIS'))

```

[^1]: Global Hydrogen Review 2023 - IEA. (2023, October 16). Retrieved
from <https://www.iea.org/reports/global-hydrogen-review-2023>

[^2]: Colli, A. N., Girault, H. H., & Battistel, A. (2019). Non-Precious
Electrodes for Practical Alkaline Water Electrolysis. *Materials*,
12(8), 1336. <https://doi.org/10.3390/ma12081336>

[^3]: Carmo, M., Fritz, D. L., Mergel, J., & Stolten, D. (2013). A
comprehensive review on PEM water electrolysis. *Int. J. Hydrogen
Energy*, 38(12), 4901–4934.
<https://doi.org/10.1016/j.ijhydene.2013.01.151>

[^4]: Natural Resources Canada. (2023, October 3). Retrieved from
[https://natural-resources.canada.ca](https://natural-resources.canada.ca/climate-change-adapting-impacts-and-reducing-emissions/canadas-green-future/the-hydrogen-strategy/23080).

[^5]: Crawford, G. A., & Hufnagl, A. F. (1987). Becancour, Quebec. Int.
J. Hydrogen Energy, 12(5), 297–303. doi: 10.1016/0360-3199(87)90054-1.

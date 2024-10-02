# Modeling Framework
## Linear Programming Formulation

The model is mathematically formulated as an LP problem ([fourer1990modeling](https://www.ampl.com/_archive/first-website/REFS/amplmod.pdf)). The following figure represents - in a simple manner - what an LP problem is and the nomenclature used.

![Conceptual illustration of an LP problem.](../images/ESTD/model_formulation/chp_estd_lp_conceptual.png)

## Conceptual Modelling Framework

The proposed modeling framework is a simplified representation of an energy system accounting for the energy flows within its boundaries. Its primary objective is to satisfy the energy balance constraints, meaning that the demand is known and the supply has to meet it. In energy modeling practice, the energy demand is often expressed in terms of FEC. According to the definition of the European Commission, FEC is defined as "the energy which reaches the final consumer’s door" ([EU_FEC](https://www.eea.europa.eu/en/analysis/indicators/primary-and-final-energy-consumption)). In other words, the FEC is the amount of input energy needed to satisfy the EUD in energy services. As an example, in the case of decentralized heat production with an NG boiler, the FEC is the amount of NG consumed by the boiler; the EUD is the amount of heat produced by the boiler, i.e., the heating service needed by the final user.

The input for the proposed modeling framework is the EUD in energy services, represented as the sum of four energy sectors: electricity, heating, mobility, and non-energy demand; this replaces the classical economic-sector-based representation of energy demand. Heat is divided into three EUTs: high-temperature heat for industry, low temperature for space heating, and low temperature for hot water. Mobility is divided into two EUTs: passenger mobility and freight. Non-energy demand is, based on the IEA definition, “fuels that are used as raw materials in the different sectors and are not consumed as a fuel or transformed into another fuel” ([IEA_websiteDefinition](https://www.iea.org/statistics/resources/balancedefinitions/)). As examples, the European Commission includes as non-energy the following materials: “chemical feed-stocks, lubricants, and asphalt for road construction” ([EuropeanCommission2016](https://doi.org/10.2833/9127)).

![Conceptual example of an energy system.](../images/ESTD/model_formulation/chp_estd_conceptual_framework.png)

A simplified conceptual example of the energy system structure is proposed in the following figure. The system is split into three parts: resources, energy conversion, and demand. In this illustrative example, resources are solar energy, electricity, and NG. The EUD are electricity, space heating, and passenger mobility. The energy system encompasses all the energy conversion technologies needed to transform resources and supply the EUD. In this example, Solar and NG resources cannot be directly used to supply heat. Thus, they use technologies, such as boilers or CHP for NG, to supply the EUT layer (e.g., the high-temperature industrial heat layer). Layers are defined as all the elements in the system that need to be balanced in each time period; they include resources and EUTs. As an example, the electricity layer must be balanced at any time, meaning that the production and storage must equal the consumption and losses. These layers are connected to each other by technologies. We define three types of technologies: technologies of end-use type, storage technologies, and infrastructure technologies. A technology of end-use type can convert the energy (e.g., a fuel resource) from one layer to an EUT layer, such as a CHP unit that converts NG into heat and electricity. A storage technology converts energy from a layer to the same one, such as TS that stores heat to provide heat. In this example, there are two storage technologies: TS for heat and PHS for electricity. An infrastructure technology gathers the remaining technologies, including the networks, such as the power grid and DHNs, but also technologies linking non end-use layers, such as methane production from wood gasification or hydrogen production from methane reforming.

As an illustrative example of the concept of *layer*, the following figure gives a perspective of the electricity layer which is the most complex one, since the electrification of other sectors is foreseen as a key of the energy transition ([Sugiyama2012](https://doi.org/10.1016/j.enpol.2012.01.028)). In the proposed version, 42 technologies are related to the electricity layer. Nine technologies produce exclusively electricity, such as CCGT, PV, or wind. Twelve cogenerations of heat and power (CHPs) produce heat and electricity, such as industrial waste CHP. Six technologies are related to the production of synthetic fuels and CCS. One infrastructure represents the grid. Four storage technologies are implemented, such as PHS, batteries, or V2G. The remains are consumers regrouped in the electrification of heat and mobility. Electrification of the heating sector is supported by direct electric heating but also by the more expensive but more efficient electrical heat pumps for low temperature heat demand. Electrification of mobility is achieved via electric public transportation (train, trolley, metro, and electrical/hybrid buses), electric private transportation including and hydrogen cars and trains for freight.

![Representation of the Electricity layer.](../images/ESTD/model_formulation/Layer_Elec.png)

The energy system is formulated as an LP problem. It optimizes the design by computing the installed capacity of each technology, as well as the operation in each period, to meet the energy demand and minimize the total annual cost of the system. In the following, we present the complete formulation of the model in two parts. First, all the terms used are summarized in a figure and tables: the figure for sets, tables for parameters, and tables for independent and dependent variables. On this basis, the equations representing the constraints and the objective function are formulated in the figure and equations and described in the following paragraphs.

#### Sets, Parameters, and Variables

The figure gives a visual representation of the sets with their relative indices used in the following. The tables list and describe the model parameters. Tables list and describe the independent and dependent variables, respectively.

![Visual representation of the sets and indices used.](../images/ESTD/model_formulation/ses_sets_v2.png)

##### Time Series Parameters

| **Parameter**             | **Units** | **Description**           |
|---------------------------|-----------|---------------------------|
| $\%_{elec}(h,td)$         | [-]       | Yearly time series (adding up to 1) of electricity end-uses      |
| $\%_{sh}(h,td)$           | [-]       | Yearly time series (adding up to 1) of SH end-uses               |
| $\%_{mob}(h,td)$          | [-]       | Yearly time series (adding up to 1) of passenger mobility end-uses|
| $\%_{fr}(h,td)$           | [-]       | Yearly time series (adding up to 1) of freight mobility end-uses |
| $c_{p,t}(tech,h,td)$      | [-]       | Hourly maximum capacity factor for each technology (default 1)   |

##### List of Parameters (except time series)

| **Parameter**             | **Units**                     | **Description**            |
|---------------------------|-------------------------------|----------------------------|
| $\tau(tech)$              | [-]                           | Investment cost annualization factor |
| $i_{rate}$                | [-]                           | Real discount rate          |
| $endUses_{year}$          | [GWh/y] [^a]_                  | Annual end-uses in energy services per sector |
| $endUsesInput(eui)$       | [GWh/y] [^a]_                  | Total annual end-uses in energy services |
| $re_{share}$              | [-]                           | Minimum share [0;1] of primary RE |
| $gwp_{limit}$             | [ktCO$_{2-eq}$/y]             | Higher CO$_{2-eq}$ emissions limit |
| $\%_{public,min}, \%_{public,max}$ | [-]           | Lower and upper limit to $\textbf{\%}_{\textbf{Public}}$ |
| $\%_{fr,rail,min}, \%_{fr,rail,max}$ | [-]         | Lower and upper limit to $\textbf{\%}_{\textbf{Fr,Rail}}$ |
| $\%_{fr,boat,min}, \%_{fr,boat,max}$ | [-]         | Lower and upper limit to $\textbf{\%}_{\textbf{Fr,Boat}}$ |
| $\%_{fr,truck,min}, \%_{fr,truck,max}$ | [-]        | Lower and upper limit to $\textbf{\%}_{\textbf{Fr,Truck}}$ |
| $\%_{dhn,min}, \%_{dhn,max}$ | [-]                  | Lower and upper limit to $\textbf{\%}_{\textbf{Dhn}}$ |
| $\%_{ned}(EUT\_OF\_EUC(NON\_ENERGY))$ | [-]        | Share of non-energy demand per type of feedstocks |
| $t_{op}(h,td)$            | [h]                           | Time period duration (default 1h) |
| $f_{min}, f_{max}(tech)$  | [GW] [^a]_ [^b]_                | Min./max. installed size of the technology |
| $f_{min,\%}, f_{max,\%}(tech)$ | [-]                | Min./max. relative share of a technology in a layer |
| $avail(res)$              | [GWh/y]                       | Resource yearly total availability |
| $c_{op}(res)$             | [M€$_{2015}$/GWh]             | Specific cost of resources |
| $veh_{capa}$              | [km-pass/h/veh.] [^a]_         | Mobility capacity per vehicle (veh.) |
| $\%_{Peak_{sh}}$          | [-]                           | Ratio peak/max. space heating demand in typical days |
| $f(res \cup tech \setminus sto, l)$ | [GW] [^c]_     | Input from (<0) or output to (>0) layers. f(i,j) = 1 if j is the main output layer for technology/resource i. |
| $c_{inv}(tech)$           | [M€$_{2015}$/GW] [^c]_ [^b]_    | Technology specific investment cost |
| $c_{maint}(tech)$         | [M€$_{2015}$/GW/y] [^c]_ [^b]_  | Technology specific yearly maintenance cost |
| $lifetime(tech)$          | [y]                           | Technology lifetime |
| $gwp_{constr}(tech)$      | [ktCO$_2$-eq./GW] [^a]_ [^b]_   | Technology construction specific GHG emissions |
| $gwp_{op}(res)$           | [ktCO$_2$-eq./GWh]            | Specific GHG emissions of resources |
| $c_{p}(tech)$             | [-]                           | Yearly capacity factor |
| $\eta_{sto,in},\eta_{sto,out}(sto,l)$ | [-]         | Efficiency [0;1] of storage input from/output to layer. Set to 0 if storage is not related to the layer |
| $\%_{sto_{loss}}(sto)$    | [1/h]                         | Losses in storage (self discharge) |
| $t_{sto_{in}}(sto)$       | [-]                           | Time to charge storage (Energy to power ratio) |
| $t_{sto_{out}}(sto)$      | [-]                           | Time to discharge storage (Energy to power ratio) |
| $\%_{sto_{avail}}(sto)$   | [-]                           | Storage technology availability to charge/discharge |
| $\%_{net_{loss}}(eut)$    | [-]                           | Losses coefficient [0;1] in the networks (grid and DHN) |
| $ev_{batt,size}(v2g)$     | [GWh]                         | Battery size per V2G car technology |
| $soc_{min,ev}(v2g,h)$     | [GWh]                         | Minimum state of charge for electric vehicles |
| $c_{grid,extra}$          | [M€$_2015$/GW]                | Cost to reinforce the grid per GW of intermittent renewable |
| $elec_{import,max}$       | [GW]                          | Maximum net transfer capacity |
| $solar_{area}$            | [km$^2$]                      | Available area for solar panels |
| $density_{pv}$            | [GW/km$^2$]                   | Peak power density of PV |
| $density_{solar,thermal}$ | [GW/km$^2$]                   | Peak power density of solar thermal |

## Energy Model Formulation

In the following, the overall LP formulation is proposed through the figure and equations, the constraints are grouped in paragraphs. It starts with the calculation of the EUD. Then, the cost, the GWP, and the objective functions are introduced. Then, it follows with more specific paragraphs, such as *storage* implementations.

### End-use Demand

Imposing the EUD instead of the FEC has two advantages. First, it introduces a clear distinction between demand and supply. On the one hand, the demand concerns the definition of the end-uses, i.e., the requirements in energy services (e.g., the mobility needs). On the other hand, the supply concerns the choice of the energy conversion technologies to supply these services (e.g., the types of vehicles used to satisfy the mobility needs). Based on the technology choice, the same EUD can be satisfied with different FEC, depending on the efficiency of the chosen energy conversion technology. Second, it facilitates the inclusion in the model of electric technologies for heating and transportation.

![Hourly **EndUses** demands calculation.](../images/ESTD/model_formulation/EndUseDemand.png)

The hourly end-use demands (**EndUses**) are computed based on the yearly end-use demand (*endUsesInput*), distributed according to its time series (listed in the table). The figure graphically presents the constraints associated with the hourly end use demand (**EndUses**), e.g., the public mobility demand at time $t$ is equal to the hourly passenger mobility demand times the public mobility share (**%\ Public**).

Electricity end-uses result from the sum of the electricity-only demand, assumed constant throughout the year, and the variable demand for electricity, distributed across the periods according to *%\ elec*. Low-temperature heat demand results from the sum of the yearly demand for HW, evenly shared across the year, and SH, distributed across the periods according to *%\ sh*. The percentage repartition between centralized (DHN) and decentralized heat demand is defined by the variable **%\ Dhn**. High-temperature process heat and mobility demand are evenly distributed across the periods. Passenger mobility demand is expressed in passenger-kilometers (pkms), freight transportation demand is in ton-kilometers (tkms). The variable **%\ Public** defines the penetration of public transportation in the passenger mobility sector. Similarly, **%\ Rail**, **%\ Boat**, and **%\ Truck** define the penetration of train, boat, and trucks for freight mobility, respectively.

### Test Cost, Emissions, and Objective Function

$$\text{min} \textbf{C}_{\textbf{tot}} = \sum_{j \in \text{TECH}} \Big(\textbf{$\tau$}(j) \textbf{C}_{\textbf{inv}}(j) + \textbf{C}_{\textbf{maint}} (j)\Big) + \sum_{i \in \text{RES}} \textbf{C}_{\textbf{op}}(i)$$

$$\text{s.t. }  \textbf{$\tau$}(j) =  \frac{i_{\text{rate}}(i_{\text{rate}}+1)^{lifetime(j)}}{(i_{\text{rate}}+1)^{lifetime(j)} - 1} ~~~~~~ \forall j \in \text{TECH}\\$$

$$
\textbf{C}_{\textbf{inv}}(j) = c_{\text{inv}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}\\
$$

$$\textbf{C}_{\textbf{maint}}(j) = c_{\text{maint}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}\\$$

$$
\textbf{C}_{\textbf{op}}(i) = \sum_{t \in T | \{h,td\} \in T\_H\_TD(t)} c_{\text{op}}(i) \textbf{F}_{\textbf{t}}(i,h,td) t_{op} (h,td)  
~~~~~~ \forall i \in \text{RES}
$$

The objective is the minimization of the total annual cost of the energy system ($\textbf{C}_{\textbf{tot}}$), defined as the sum of the annualized investment cost of the technologies ($\tau\textbf{C}_{\textbf{inv}}$), the operating and maintenance cost of the technologies ($\textbf{C}_{\textbf{maint}}$), and the operating cost of the resources ($\textbf{C}_{\textbf{op}}$). The total investment cost ($\textbf{C}_{\textbf{inv}}$) of each technology results from the multiplication of its specific investment cost ($c_{inv}$) and its installed size (**F**), the latter defined with respect to the main end-uses output type, ($\textbf{C}_{\textbf{inv}}$) is annualized with the factor $\tau$, calculated based on the interest rate ($t_{op}$) and the technology lifetime (*lifetime*). The total operation and maintenance cost is calculated in the same way. The total cost of the resources is calculated as the sum of the end-use over different periods multiplied by the period duration ($t_{op}$) and the specific cost of the resource ($c_{op}$). Note that summing over the typical days using the set $T\_H\_TD$ is equivalent to summing over the 8760 hours of the year.

$$
\textbf{GWP}_\textbf{tot}  = \sum_{j \in \text{TECH}} \frac{\textbf{GWP}_\textbf{constr} (j)}{lifetime(j)} +   \sum_{i \in \text{RES}} \textbf{GWP}_\textbf{op} (i) 
$$

$$
\left(\text{in this version of the model} :   \textbf{GWP}_\textbf{tot}  =    \sum_{i \in \text{RES}} \textbf{GWP}_\textbf{op} (i) \right) 
$$

$$
\textbf{GWP}_\textbf{constr}(j) = gwp_{\text{constr}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}
$$

$$
\textbf{GWP}_\textbf{op}(i) = \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} gwp_\text{op}(i) \textbf{F}_\textbf{t}(i,h,td)  t_{op} (h,td )~~~~~~ \forall i \in \text{RES}
$$

The global annual GHG emissions are calculated using an LCA approach, i.e., taking into account emissions of the technologies and resources ‘from cradle to grave’. For climate change, the natural choice as an indicator is the GWP, expressed in ktCO₂-eq./year. The total yearly emissions of the system ($\textbf{GWP}_{\textbf{tot}}$) are defined as the sum of the emissions related to the construction and end-of-life of the energy conversion technologies ($\textbf{GWP}_{\textbf{constr}}$), allocated to one year based on the technology lifetime ($lifetime$), and the emissions related to resources ($\textbf{GWP}_{\textbf{op}}$). Similarly to the costs, the total emissions related to the construction of technologies are the product of the specific emissions ($gwp_{constr}$ and the installed size ($\textbf{F}$), The total emissions of the resources are the emissions associated with fuels (from cradle to combustion) and imports of electricity ($gwp_{op}$) multiplied by the period duration ($t_{op}$). GWP accounting can be conducted in different manners depending on the scope of emission. The European Commission and the IEA mainly use resource-related emissions ($\textbf{GWP}_{\textbf{op}}$) while neglecting indirect emissions related to the construction of technologies ($\textbf{GWP}_{\textbf{constr}}$). To facilitate the comparison with their results, a similar implementation is proposed.

### System Design and Operation

$$
f_{\text{min}} (j) \leq \textbf{F}(j) \leq f_{\text{max}} (j) ~~~~~~ \forall j \in \text{TECH}
$$

The installed capacity of a technology (**F**) is constrained between upper and lower bounds (*f\ max* and *f\ min*). This formulation allows accounting for old technologies still existing in the target year (lower bound) and the maximum deployment potential of a technology. As an example, for offshore wind turbines, $f_{min}$ represents the existing installed capacity (which will still be available in the future), while $f_{max}$ represents the maximum potential.

$$
\textbf{F}_\textbf{t}(i,h,td) \leq \textbf{F}_\textbf{t}(i) \cdot c_{p,t} (i,h,td) ~~~~~~ \forall i \in \text{TECH}, h \in H, td \in TD
$$

$$
\sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td) t_{op}(h,td)  \leq \textbf{F} (j) c_{p} (j) \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} t_{op} (h,td)  
$$

$$
\forall j \in \text{TECH}
$$

$$
\sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(i,h,td) t_{op}(h,td)  \leq \text{avail} (i) ~~~~~~ \forall i \in \text{RES}
$$

The operation of resources and technologies in each period is determined by the decision variable $\textbf{F}_{\textbf{t}}$. The capacity factor of technologies is conceptually divided into two components: a capacity factor for each period ($c_{p,t}$) depending on resource availability (e.g., renewables) and a yearly capacity factor (*c\ p*) accounting for technology downtime and maintenance. For a given technology, the definition of only one of these two is needed, the other one being fixed to the default value of 1. For example, intermittent renewables are constrained by an hourly load factor ($c_{p,t}\in[0;1]$) while CCGTs are constrained by an annual load factor ($c_{p}$, in that case, 96% in 2035). The equations link the installed size of a technology to its actual use in each period ($\textbf{F}_{\textbf{t}}$) via the two capacity factors. The total use of resources is limited by the yearly availability ($avail$).

$$
\sum_{i \in \text{RES}~\cup \text{TECH} \setminus \text{STO}} f(i,l) \textbf{F}_\textbf{t}(i,h,td) + \sum_{j \in \text{STO}} \bigg(\textbf{Sto}_\textbf{out}(j,l,h,td) - \textbf{Sto}_\textbf{in}(j,l,h,td)\bigg)  
$$

$$
- \textbf{EndUses}(l,h,td) = 0
$$

$$
\forall l \in L, \forall h \in H, \forall td \in TD
$$

The matrix $f$ defines for all technologies and resources outputs to (positive) and inputs (negative) layers. The equation expresses the balance for each layer: all outputs from resources and technologies (including storage) are used to satisfy the EUD or as inputs to other resources and technologies.

### Storage

$$
\textbf{Sto}_\textbf{level} (j,t) = \textbf{Sto}_\textbf{level} (j,t-1)\cdot\left(1 - \%_{sto_{loss}}(j) \right)  
$$

$$
+ t_{op} (h,td)\cdot \Big(\sum_{l \in L | \eta_{\text{sto,in} (j,l) > 0}} \textbf{Sto}_\textbf{in} (j,l,h,td) \eta_{\text{sto,in}} (j,l) 
$$

$$
- \sum_{l \in L | \eta_{\text{sto,out} (j,l) > 0}} \textbf{Sto}_\textbf{out} (j,l,h,td) / \eta_{\text{sto,out}} (j,l)\Big)
$$

$$
\forall j \in \text{STO}, \forall t \in \text{T}| \{h,td\} \in T\_H\_TD(t)
$$

$$
\textbf{Sto}_\textbf{level} (j,t) = \textbf{F}_\textbf{t} (j,h,td) ~~~~~~ \forall j \in \text{STO DAILY},\forall t \in \text{T}| \{h,td\} \in T\_H\_TD(t)
$$

$$
\textbf{Sto}_\textbf{level} (j,t) \leq \textbf{F} (j) ~~~~~~ \forall j \in \text{STO} \setminus \text{STO DAILY},\forall t \in \text{T}  
$$

The storage level ($\textbf{Sto}_{\textbf{level}}$) at a time step ($t$) is equal to the storage level at $t-1$ (accounting for the losses in $t-1$), plus the inputs to the storage, minus the output from the storage (accounting for input/output efficiencies). In the code, for the first period of the year, this equation is slightly modified to set the storage level at the beginning of the year according to the one at the end of the year. Hence, if $t=1$, we set $t-1$ to the last period of the year (8760). The storage systems which can only be used for short-term (daily) applications are included in the daily storage set (STO DAILY). For these units, the equation imposes that the storage level be the same at the end of each typical day. Adding this constraint drastically reduces the computational time. For the other storage technologies, which can also be used for seasonal storage, the capacity is bounded by the equation. For these units, the storage behavior is thus optimized over 8760 hours.

$$
\textbf{Sto}_\textbf{in}(j,l,h,td)\cdot \Big(\lceil  \eta_{sto,in}(j,l)\rceil -1 \Big) = 0  ~~~~~~ \forall j \in \text{STO},\forall l \in \text{L}, \forall h \in \text{H}, \forall td \in \text{TD}
$$

$$
\textbf{Sto}_\textbf{out}(j,l,h,td)\cdot \Big(\lceil  \eta_{sto,out}(j,l)\rceil -1 \Big) = 0  ~~~~~~ \forall j \in \text{STO},\forall l \in \text{L}, \forall h \in \text{H}, \forall td \in \text{TD}
$$

$$
\Big(\textbf{Sto}_\textbf{in} (j,l,h,td)t_{sto_{in}}(\text{j}) + \textbf{Sto}_\textbf{out}(j,l,h,td)t_{sto_{out}}(\text{j})\Big) \leq \textbf{F} (j)\%_{sto_{avail}}(j)
$$

$$
\forall j \in STO \setminus {V2G} , \forall l \in L, \forall h \in H, \forall td \in TD
$$

These equations force the power input and output to zero if the layer is incompatible. For example, a PHS will only be linked to the electricity layer (input/output efficiencies $>0$). All other efficiencies will be equal to 0, to prevent the PHS from exchanging with incompatible layers (e.g., mobility, heat, etc.). The equation limits the power input/output of a storage technology based on its installed capacity (**F**) and three specific characteristics. First, storage availability ($\%_{sto_{avail}}$) is defined as the ratio between the available storage capacity and the total installed capacity (default value is 100%). This parameter is only used to realistically represent V2G, for which we assume that only a fraction of the fleet (i.e., 20% in these cases) can charge/discharge at the same time. Second and third, the charging/discharging time ($t_{sto_{in}}$, $t_{sto_{out}}$), which are the time to complete a full charge/discharge from empty/full storage. As an example, a daily thermal storage needs at least 4 hours to discharge ($t_{sto_{out}}=4 \ [h]$), and another 4 hours to charge ($t_{sto_{in}}=4\ [h]$). The equation applies to all storage except electric vehicles, which are limited by another constraint, presented later.

### Networks

$$
\textbf{Net}_\textbf{loss}(eut,h,td) = \Big(\sum_{i \in \text{RES} \cup \text{TECH} \setminus \text{STO} | f(i,eut) > 0} f(i,eut)\textbf{F}_\textbf{t}(i,h,td) \Big) \%_{\text{net}_{loss}} (eut) 
$$

$$
\forall eut = \text{EUT}, \forall h \in H, \forall td \in TD
$$

$$
\textbf{F} (Grid) = 1 + \frac{c_{grid,extra}}{c_{inv}(Grid)} 
\Big(
\textbf{F}(Wind_{onshore}) + \textbf{F}(Wind_{offshore}) + \textbf{F}(PV)
$$

$$
-\big( 
f_{min}(Wind_{onshore}) + f_{min}(Wind_{offshore}) + f_{min}(PV)
\big)
\Big)
$$

$$
\textbf{F} (DHN) = \sum_{j \in \text{TECH} \setminus {STO} | f(j,\text{HeatLowTDHN}) >0} f(j,\text{HeatLowTDHN}) \cdot \textbf{F} (j) 
$$

The equation calculates network losses as a share ($%_{net_{loss}}$) of the total energy transferred through the network. For example, losses in the electricity grid are estimated to be 4.5% of the energy transferred in 2015. The equations define the extra investment for networks. Integration of intermittent RE implies additional investment costs for the electricity grid ($c_{grid,extra}$). As an example, the reinforcement of the electricity grid is estimated to be 358 million €\ _{2015} per Gigawatt of intermittent renewable capacity installed. The equation links the size of DHN to the total size of the installed centralized energy conversion technologies.

### Additional Constraints

$$
\textbf{F}_\textbf{t} (Nuclear,h,td) = \textbf{P}_\textbf{Nuclear}  ~~~~~~ \forall h \in H, \forall td \in TD
$$

Nuclear power plants are assumed to have no power variation over the year. If needed, this equation can be replicated for all other technologies for which a constant operation over the year is desired.

$$
\textbf{F}_\textbf{t} (j,h,td) = \textbf{%}_\textbf{PassMob} (j)   \sum_{l \in EUT\_of\_EUC(PassMob)} \textbf{EndUses}(l,h,td) 
$$

$$
\forall j \in TECH\_OF\_EUC(PassMob) , \forall h \in H, \forall td \in TD
$$

$$
\textbf{F}_\textbf{t} (j,h,td) = \textbf{%}_\textbf{FreightMob} (j)   \sum_{l \in EUT\_of\_EUC(FreightMob)} \textbf{EndUses}(l,h,td) 
$$

$$
\forall j \in TECH\_OF\_EUC(FreightMob) , \forall h \in H, \forall td \in TD
$$

$$
\textbf{%}_\textbf{Fr,Rail} + \textbf{%}_\textbf{Fr,Train} + \textbf{%}_\textbf{Fr,Boat} = 1
$$

The equations impose that the share of the different technologies for mobility ($\textbf{%}_{\textbf{PassMob}}$) and ($\textbf{%}_{\textbf{Freight}}$) be the same at each time step. In other words, if 20% of the mobility is supplied by train, this share remains constant in the morning or the afternoon. The equation verifies that the freight technologies supply the overall freight demand (this constraint is related to the figure).

### Decentralized Heat Production

$$
\textbf{F} (Dec_{Solar}) = \sum_{j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}} \textbf{F}_\textbf{sol} (j)  
$$

$$
\textbf{F}_{\textbf{t}_\textbf{sol}} (j,h,td) \leq  \textbf{F}_\textbf{sol} (j)  c_{p,t}('Dec_{Solar}',h,td)
$$

$$
\forall j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}, \forall h\in H, \forall td \in TD
$$

Thermal solar is implemented as a decentralized technology. It is always installed together with another decentralized technology, which serves as a backup to compensate for the intermittency of solar thermal. Thus, we define the total installed capacity of solar thermal **F**\ ($Dec_{solar}$) as the sum of **F\ sol**\ ($j$), where $\textbf{F}_{\textbf{sol}}(j)$ is the solar thermal capacity associated with the backup technology $j$. The equation links the installed size of each solar thermal capacity $\textbf{F}_{\textbf{sol}}(j)$ to its actual production $\textbf{F}_{\textbf{t}_\textbf{sol}}(j,h,td))$ via the solar capacity factor ($c_{p,t}('Dec_{solar}')$).

$$
\textbf{F}_\textbf{t} (j,h,td) + \textbf{F}_{\textbf{t}_\textbf{sol}} (j,h,td)  
$$

$$
+ \sum_{l \in \text{L}}\Big( \textbf{Sto}_\textbf{out} (i,l,h,td) - \textbf{Sto}_\textbf{in} (i,l,h,td) \Big)
$$

$$
= \textbf{%}_\textbf{HeatDec}(\text{j}) \textbf{EndUses}(HeatLowT,h,td) 
$$

$$
\forall j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}, 
$$

$$
i \in \text{TS OF DEC TECH}(j)  , \forall h\in H, \forall td \in TD
$$

![Illustrative example of a decentralized heating layer.](../images/ESTD/model_formulation/ts_and_Fsolv2.png)

A thermal storage $i$ is defined for each decentralized heating technology $j$, to which it is related via the set *TS OF DEC TECH*, i.e., $i$\ =\ *TS OF DEC TECH(j)*. Each thermal storage $i$ can store heat from its technology $j$ and the associated thermal solar $\textbf{F}_{\textbf{sol}}$ ($j$). Similarly to the passenger mobility, the equation makes the model more realistic by defining the operating strategy for decentralized heating. In fact, in the model, we represent decentralized heat in an aggregated form; however, in a real case, residential heat cannot be aggregated. A house heated by a decentralized gas boiler and solar thermal panels should not be able to be heated by the electrical heat pump and thermal storage of the neighbors, and vice-versa. Hence, the equation imposes that the use of each technology ($\textbf{F}_{\textbf{t}}(j,h,td)$), plus its associated thermal solar ($\textbf{F}_{\textbf{t}_\textbf{sol}}(j,h,td)$) plus its associated storage outputs ($\textbf{Sto}_{\textbf{out}}(i,l,h,td)$) minus its associated storage inputs ($\textbf{Sto}_{\textbf{in}}(i,l,h,td)$) should be a constant share ($\textbf{%}_{\textbf{HeatDec}}(j)$) of the decentralized heat demand ($\textbf{EndUses}(HeatLowT,h,td)$). The figure shows, through an example with two technologies (a gas boiler and an HP), how decentralized thermal storage and thermal solar are implemented.

### Peak Demand

$$
\textbf{F} (j) 
\geq
\%_{Peak_{sh}}\max_{h\in H,td\in TD}\left\{\textbf{F}_\textbf{t}(j,h,td)\right\}
$$

$$
\forall j \in \text{TECH OF  EUT} (HeatLowTDEC)   \setminus \{ 'Dec_{Solar}'\}
$$

$$
\sum_{\hspace{3cm}j \in \text{TECH OF EUT} (HeatLowTDHN), i \in \text{STO OF EUT}(HeatLowTDHN)}
$$

$$
\Big( \textbf{F} (j)+
\textbf{F} (i)/t_{sto_{out}}(i,HeatLowTDHN)  \Big)
$$

$$
\geq
\%_{Peak_{sh}} \max_{h\in H,td\in TD}  \big\{ \textbf{EndUses}(HeatLowTDHN,h,td) \big\}
$$

Finally, the equations constrain the installed capacity of low-temperature heat supply. Based on the selected TDs, the ratio between the yearly peak demand and the TDs peak demand is defined for space heating ($\%_{Peak_{sh}}$). The equation imposes that the installed capacity for decentralized technologies covers the real peak over the year. Similarly, the equation forces the centralized heating system to have a supply capacity (production plus storage) higher than the peak demand. These equations force the installed capacity to meet the peak heating demand, which represents, somehow, the network adequacy.

## Adaptations for the Case Study

Additional constraints are required to implement scenarios. Scenarios require six additional constraints to impose a limit on the GWP emissions, the minimum share of RE primary energy, the relative shares of technologies, such as gasoline cars in private mobility, the cost of energy efficiency measures, the electricity import power capacity, and the available surface area for solar technologies.

$$
\textbf{GWP}_\textbf{tot} \leq gwp_{limit}  
$$

$$
\sum_{j \in  \text{RES}_\text{re},t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td)  \cdot  t_{op} (h,td)   
$$

$$
\geq 
re_{share} \sum_{j \in \text{RES} ,t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td) \cdot  t_{op} (h,td)
$$

To force the Belgian energy system to decrease its emissions, two levers can constrain the annual emissions: the equation imposes a maximum yearly emissions threshold on the GWP ($gwp_{limit}$); and the equation fixes the minimum renewable primary energy share.

$$
f_{\text{min,\%}}(j) \sum_{j' \in \text{TECH OF EUT} (eut),t \in T|\{h,td\} \in T\_H\_TD(t)}    \textbf{F}_\textbf{t}(j',h,td)\cdot t_{op}(h,td)  
$$

$$
\leq 
\sum_{t \in T|\{h,td\} \in T\_H\_TD(t)}  \textbf{F}_\textbf{t} (j,h,td)\cdot t_{op}(h,td) 
$$

$$
\leq 
f_{\text{max,\%}}(j) \sum_{j'' \in \text{TECH OF EUT} (eut),t \in T|\{h,td\} \in T\_H\_TD(t)}    \textbf{F}_\textbf{t}(j'',h,td)\cdot t_{op}(h,td) 
$$

$$
\forall eut \in EUT, \forall j \in \text{TECH OF EUT} (eut) 
$$

To represent the Belgian energy system in 2015, the equation imposes the relative share of a technology in its sector. This equation is complementary

 to the equation as it expresses the minimum ($f_{min,\%}$) and maximum ($f_{max,\%}$) yearly output shares of each technology for each type of EUD. In fact, for a given technology, assigning a relative share (e.g., boilers providing at least a given percentage of the total heat demand) is more intuitive and close to energy planning practice than limiting its installed size. $f_{min,\%}$ and $f_{max,\%}$ are fixed to 0 and 1, respectively, unless otherwise indicated.

$$
\textbf{F}(Efficiency) = \frac{1}{1+i_{rate}} 
$$

To account for efficiency measures from today to the target year, the equation imposes their cost. The EUD is based on a scenario detailed in the data for end-use demand and has a lower energy demand than the “business as usual” scenario, which has the highest energy demand. Hence, the energy efficiency cost accounts for all the investment required to decrease the demand from the “business as usual” scenario and the implemented one. As the reduced demand is imposed over the year, the required investments must be completed before this year. Therefore, the annualization cost has to be deducted from one year. This mathematically implies defining the capacity of efficiency measures deployed to $1/ (1+i_{rate})$ rather than 1. The investment is already expressed in €_{2015}.

$$
\textbf{F}_{\textbf{t}}(Electricity,h,td) \leq  elec_{import,max} ~~~~~~ \forall h \in H, \forall td \in TD
$$

$$
\textbf{F}_{\textbf{t}}(i,h,td) \cdot t_{op} (h,td) = \textbf{Import}_{\textbf{constant}}(i) ~~~~~~ \forall i \in \text{RES IMPORT CONSTANT}, h \in H, \forall td \in TD
$$

The equation limits the power grid import capacity from neighboring countries based on a net transfer capacity ($elec_{import,max}$). The equation imposes that some resources are imported at a constant power. For example, gas and hydrogen are supposed to be imported at a constant flow during the year. In addition to offering a more realistic representation, this implementation makes it possible to visualize the level of storage within the region (i.e., gas, petrol ...).

!!! warning
     Adding too many resources to this equation drastically increases computational time. In this implementation, only resources expensive to store have been accounted for: hydrogen and gas. Other resources, such as diesel or ammonia, can be stored at a cheap price with small losses. By limiting to two types of resources (hydrogen and gas), the computation time is below a minute. By adding all resources, the computation time is above 6 minutes.

$$
\textbf{F}(PV)/power\_density_{pv} 
$$

$$
+ \big( \textbf{F}(Dec_{Solar}) + \textbf{F}(DHN_{Solar}) \big)/power\_density_{solar~thermal}  \leq solar_{area}
$$

In this model version, the upper limit for solar-based technologies is calculated based on the available land area ($solar\ area$) and power densities of both PV ($power\_density_{pv}$) and solar thermal ($power\_density_{solar~thermal}$). The equivalence between installed capacity (in watt peaks Wp) and land use (in $km^2$) is calculated based on the power peak density (in [Wp/m^2]). In other words, it represents the peak power of a one square meter of a solar panel. We evaluate that PV and solar thermal have a power peak density of $power\_density_{pv}$ =0.2367 and $power\_density_{solar~thermal}$ =0.2857 [GW/km^2]. Thus, the land use of PV is the installed power ($\textbf{F}(PV)$ in [GW]) divided by the power peak density (in [GW/km^2]). This area is a lower bound of the real installation used. Indeed, here, the calculated area corresponds to the installed PV. However, in utility plants, panels are oriented perpendicular to the sunlight. As a consequence, space is required to avoid shadow between rows of panels. In the literature, the *ground cover ratio* is defined as the total spatial requirements of large-scale solar PV relative to the area of the solar panels. This ratio is estimated to be around five, which means that for each square meter of PV panel installed, four additional square meters are needed.

#### Implementation

The formulation of the MILP and LP problems has been implemented using an algebraic modeling language. The latter allows the representation of large LP and MILP problems. Its syntax is similar to AMPL, which is, according to the NEOS-statistics, the most popular format for representing mathematical programming problems. The formulation enables the use of different solvers as open-source ones, such as GLPK, or commercial ones, such as CPLEX or Gurobi. In the code, each of the equations defined above is found as it is with the corresponding numbering. SETS, Variables, and parameters have the same names (unless explicitly stated in the definition of the term). The figure illustrates, for the balance constraint, the mathematical formulation presented in this work and its implementation in the code. Colors highlight the same elements. In the implementation, each constraint has a comment (starting with #) and has a name (colored in black), in this case *layer_balance*. In addition, most of the SETS, Variables, and parameters are more explicitly named, as a first example the set layers is named *L* in the paper and *LAYERS* in the implementation; or as another example, the input efficiency who is named *f* in the paper and *layers_in_out* in the implementation.

![Comparison of equation formulation and code.](../images/ESTD/model_formulation/eqs_color.png)
![Comparison of equation formulation and code.](../images/ESTD/model_formulation/ch_estd_code_screenshot.png)


[^a]: [Mpkm] (millions of passenger-km) for passenger, [Mtkm] (millions of ton-km) for freight mobility end-uses
[^b]: [GWh] if ${{tech}} \in {{STO}}$
[^c]: [Mpkm/h] for passenger, [Mtkm/h] for freight mobility end-uses
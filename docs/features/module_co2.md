# Carbon Flows

## Module Overview

!!! abstract
    This section provides an overview of how the **EnergyScope** model integrates carbon flows within the broader energy system to assess the potential for carbon neutrality. The model tracks carbon sources and sinks, evaluates technologies for carbon capture, storage, and utilization, and assesses the feasibility of achieving net-zero carbon emissions, based on the following work:

!!! quote
    - Decarbonization in Complex Energy Systems: A Study on the Feasibility of Carbon Neutrality for Switzerland in 2050, [Li et al. 2020](https://doi.org/10.3389/fenrg.2020.549615)

!!! info "Key Aspects of Carbon Flow Modeling"
    - Tracking biogenic and nonbiogenic carbon sources, including biomass, fossil fuels, and industrial emissions.  
    - Modeling carbon sinks, including carbon capture, utilization, and storage (CCUS) technologies.  
    - Assessing the feasibility of carbon neutrality by quantifying carbon flows and balancing sources and sinks.  

---

## Principle

The carbon flows module models both biogenic and nonbiogenic carbon flows within the energy system. By integrating technologies such as carbon capture, utilization, and storage (CCUS), the model tracks and optimizes circular carbon flows. The module ensures biogenic carbon leads to net-zero or negative emissions, while nonbiogenic carbon is minimized through the use of carbon sinks.

### Carbon Content Definition
To quantify carbon flows, the **carbon content** of each energy resource is calculated using the following equation:

\[
\text{carboncontent}_r = \frac{m(C)}{m(r)} \times \text{LHV}_r
\]

Where:
- \(m(C)\) is the carbon mass fraction of resource \(r\),
- \(m(r)\) is the total mass of resource \(r\),
- \(\text{LHV}_r\) is the lower heating value of the resource.

This formula enables the tracking of carbon mass in energy carriers and products.

### Carbon Sources
The model differentiates between **biogenic** and **nonbiogenic** carbon sources:

- **Biogenic sources**: 
  - Domestic wood (waste wood, residues, forest wood),
  - Wet biomass (sewage sludge, manure, industrial and household waste),
  - Agricultural residues.

- **Nonbiogenic sources**: 
  - Imported fossil fuels (natural gas, light fuel oil, diesel, gasoline, jet-fuel),
  - Domestic fuels (nonbiogenic waste),
  - Industrial emissions (including cement production and construction emissions).

### CO2 Layers and Carbon Management
The carbon balance within the system is modeled through **CO2 layers**, which act as "tanks" for carbon flows, managing the movement of CO2 between sources, sinks, and technologies. These layers ensure carbon flows are tracked and managed efficiently throughout the system.

The **CO2 layers** in the model include:

- **CO2A**: Carbon emissions from concentrated, carbon-intensive sources such as centralized thermal power plants. These emissions are assumed to be capturable by conventional carbon capture technologies.
  
- **CO2C**: Captured CO2 that can either be stored or utilized. This layer serves as an intermediate tank before sequestration or utilization.
  
  - **CO2S**: Sequestered CO2, permanently stored underground, preventing any future use or release.
  
  - **CO2SS**: Temporarily stored CO2 that could be used later in carbon utilization technologies.
  
- **CO2E**: Carbon emissions from dispersed, non-concentrated sources such as cars, households, and fugitive emissions. These emissions are more challenging to capture, often mitigated through biomass absorption or Direct Air Capture (DAC).

## Carbon Emission and Balance Equations
Each technology in the model is linked to one or more of these CO2 layers, based on the technology's emission factor. The net carbon emissions for each period \(t\) are governed by the following equation:

\[
\text{Emission}(t) = \sum_{j \in E, c \in C} F_t(j) \cdot \text{top}(t) \cdot \eta(j, c) \quad \forall t \in T
\]

Where:
- \(E\) is the set of technologies,
- \(C\) is the set of CO2 layers (CO2A, CO2E),
- \(\eta(j, c)\) is the emission factor for technology \(j\) in layer \(c\).

In addition, the model ensures that total emissions across all periods do not exceed a predefined limit:

\[
\sum_{t \in T: t \leq t'} \text{Emission}(t) \leq \epsilon \quad \forall t' \in T
\]

This **ϵ-control** mechanism ensures that cumulative emissions are strictly managed throughout the optimization process.

## Carbon Capture, Utilization, and Sequestration
The captured CO2 (in the **CO2C** layer) can be either sequestered or utilized in the production of synthetic fuels or chemicals. The balance of carbon capture and utilization is expressed by:

\[
\sum_{j \in CC} F_t(j) = \sum_{j \in CCS} F_t(j) + \sum_{j \in CCU} F_t(j) + \sum_{j \in CTSin} F_t(j) - \sum_{j \in CTSout} F_t(j) \quad \forall t \in T
\]

Where:
- **CC** refers to carbon capture technologies,
- **CCS** refers to carbon sequestration,
- **CCU** refers to carbon utilization technologies,
- **CTSin** and **CTSout** track the storage and withdrawal of temporarily stored CO2.

The cost of operating these CC or CCS technologies is also modeled. The cost is expressed as Swiss Francs per ton of CO2 captured or sequestered:

\[
c(j) \cdot \sum_{t \in T} F_t(j) \cdot \text{top}(t) \quad \forall j \in CC \cup CS
\]

## CO2-to-X Technologies
The model includes several **CO2-to-X** technologies that convert captured CO2 into valuable fuels and chemicals:

- **Methanation**: Converts CO2 and hydrogen into synthetic methane via the Sabatier reaction.
  
- **CO2-to-Diesel**: Produces biodiesel through Fischer-Tropsch synthesis using CO2 as a feedstock.
  
- **CO2-to-Jet Fuel**: Similar to CO2-to-diesel, but produces a fuel blend tailored for aviation.
  
- **CO2-to-Methanol-to-X**: Synthesizes methanol, which can then be converted into chemicals such as ethylene, propylene, and aromatics through subsequent processes like Methanol-to-Olefins (MTO).

## Carbon Flow Management
The overall carbon flow within the system is depicted by the CO2 layers and their interactions with various technologies. By utilizing carbon capture, utilization, and sequestration, the model aims to reduce net carbon emissions to as close to zero as possible while balancing the use of both biogenic and nonbiogenic carbon sources.

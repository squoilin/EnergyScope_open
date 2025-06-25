# Overview

**EnergyScope** uses a modular architecture that balances core functionality with optional advanced features. These modules enhance analysis depth but may increase computational demands. Below is a summary of available modules.

You will find below a table summarizing the publications that have used the **EnergyScope** model. 

# Publications Table

<!-- DataTables CSS and JS -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<style>
  .table-container {
    overflow-x: auto;
    margin-top: 1em;
    border: 1px solid #ccc;
    padding: 0.5em;
  }
  table.dataTable {
    white-space: nowrap;
  }
  table.dataTable thead th {
    text-align: center;
    background-color: #f2f2f2;
  }
  table.dataTable td {
    text-align: center;
  }
</style>

<div class="table-container">
  <table id="featureTable" class="display" style="width:100%">
    <thead>
      <tr>
        <th rowspan="2">Author</th>
        <th rowspan="2">Year</th>
        <th rowspan="2">Time Resolution</th>
        <th rowspan="2">Scope</th>
        <th colspan="8">Features</th>
        <th rowspan="2">Repository</th>
        <th rowspan="2">DOI</th>
      </tr>
      <tr>
        <th>Pathways</th>
        <th>Multi-cell</th>
        <th>Infrastructure</th>
        <th>LCA</th>
        <th>Uncertainty</th>
        <th>Carbon Flow</th>
        <th>Agent-based</th>
        <th>Coupling</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Codina Gironès et al.</td><td>2015</td><td>Monthly</td><td>Switzerland</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1016/j.energy.2015.06.008">Link</a></td></tr>
      <tr><td>Moret et al.</td><td>2016</td><td>Monthly</td><td>Switzerland</td><td></td><td></td><td></td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1016/B978-0-444-63428-3.50321-0">Link</a></td></tr>
      <tr><td>Limpens et al.</td><td>2019</td><td>Typical day</td><td>Belgium</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1016/j.apenergy.2019.113729">Link</a></td></tr>
      <tr><td>Li et al.</td><td>2020</td><td>Monthly</td><td>Switzerland</td><td></td><td></td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.3389/fenrg.2020.549615">Link</a></td></tr>
      <tr><td>Limpens et al.</td><td>2020</td><td>Typical day</td><td>Belgium</td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.3390/en13010261">Link</a></td></tr>
      <tr><td>Rixhon et al.</td><td>2021</td><td>Typical day</td><td>Belgium</td><td>✅</td><td></td><td></td><td>✅</td><td>❓</td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.3390/en14134027">Link</a></td></tr>
      <tr><td>Li et al.</td><td>2022</td><td>Monthly</td><td>Switzerland</td><td>✅</td><td></td><td></td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1109/PESGM48719.2022.9916902">Link</a></td></tr>
      <tr><td>Borasio et al.</td><td>2022</td><td>Typical day</td><td>Italy</td><td></td><td></td><td>✅</td><td>✅</td><td></td><td></td><td></td><td></td><td><a href="https://github.com/energyscope/EnergyScope/tree/EnergyScopeIT">GitHub</a></td><td><a href="https://doi.org/10.1016/j.rser.2021.111730">Link</a></td></tr>
      <tr><td>Dumas et al.</td><td>2022</td><td>Typical day</td><td>Belgium</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1007/s41247-022-00106-0">Link</a></td></tr>
      <tr><td>Schnidrig et al.</td><td>2023</td><td>Monthly</td><td>Switzerland</td><td>✅</td><td></td><td>✅</td><td>✅</td><td></td><td></td><td></td><td></td><td><a href="https://gitlab.com/ipese/on-the-role-of-energy-infrastructure-in-the-energy-transition">GitLab</a></td><td><a href="https://doi.org/10.3389/fenrg.2023.1164813">Link</a></td></tr>
      <tr><td>Thiran et al.</td><td>2023</td><td>Typical day</td><td>EU</td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://github.com/energyscope/EnergyScope_multi_cells">GitHub</a></td><td><a href="https://doi.org/10.3390/en16062772">Link</a></td></tr>
      <tr><td>Schnidrig et al.</td><td>2024</td><td>Monthly</td><td>Switzerland</td><td>✅</td><td></td><td>✅</td><td>✅</td><td>✅</td><td></td><td></td><td></td><td><a href="https://gitlab.com/ipese/energyscope-actors">GitLab</a></td><td><a href="https://doi.org/10.3389/fenrg.2024.1433921">Link</a></td></tr>
      <tr><td>Schnidrig et al.</td><td>2024</td><td>Monthly</td><td>Switzerland</td><td>✅</td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://gitlab.com/ipese/energyscope-lca">GitLab</a></td><td><a href="https://doi.org/10.1016/j.jenvman.2024.122537">Link</a></td></tr>
      <tr><td>Schnidrig et al.</td><td>2024</td><td>Monthly</td><td>Switzerland</td><td>✅</td><td></td><td>✅</td><td>✅</td><td></td><td></td><td><a href="https://reho.readthedocs.io/en/main/">REHO</td><td></td><td><a href="https://gitlab.com/ipese/energyscope-decentralization">GitLab</a></td><td><a href="https://doi.org/10.3390/en17071718">Link</a></td></tr>
      <tr><td>Limpens et al.</td><td>2024</td><td>Typical day</td><td>Belgium</td><td>✅</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="https://doi.org/10.1016/j.apenergy.2023.122501">Link</a></td></tr>
    </tbody>
  </table>
</div>

<script>
  $(document).ready(function () {
    $('#featureTable').DataTable({
      paging: true,
      searching: true,
      ordering: true,
      scrollX: true
    });
  });
</script>

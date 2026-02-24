---
layout: default
title: Monte Carlo Validation Project Page
---

<section id="overview" class="hero p-4 p-md-5 mb-5">
  <div class="row g-4 align-items-center">
    <div class="col-lg-8">
      <span class="badge badge-soft text-uppercase mb-3">HEPSIM • ML4SCI</span>
      <h1 class="display-6 fw-bold mb-3">JetObsMC: Jet Observables for Monte Carlo Validation</h1>
      <p class="lead muted mb-4">
        A unified scientific software stack for jet observables, built to compare Monte Carlo generator predictions against LHC-style data with one consistent API, metadata contract, and validation workflow.
      </p>
      <div class="d-flex flex-wrap gap-2">
        <a class="btn btn-primary" href="https://github.com/Atharva12081/JetObsMC">Repository</a>
        <a class="btn btn-outline-primary" href="https://ml4sci.org/gsoc/2026/proposal_HEP.html">ML4SCI Project Catalog</a>
        <a class="btn btn-outline-secondary" href="{{ '/observables/' | relative_url }}">Observable Catalog</a>
      </div>
    </div>
    <div class="col-lg-4">
      <div class="card">
        <div class="card-body">
          <h2 class="h6 text-uppercase text-secondary">Current Prototype Status</h2>
          <ul class="mb-0">
            <li>Pip-installable package (`setup.py`)</li>
            <li>30-observable catalog (kinematic/shape/substructure/groomed-proxy)</li>
            <li>FourVector + Jet core abstractions</li>
            <li>Observable metadata with IRC-safety tags</li>
            <li>CI-backed pytest suite with reference checks</li>
            <li>Monte Carlo validation notebooks (submission + workflow + Colab)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="scope" class="mb-5">
  <h2 class="section-title h3 mb-3">Scope and Design</h2>
  <p class="muted">
    Jets are collimated sprays of particles from high-energy collisions. Validating Monte Carlo generators against data requires a broad, consistent, and reproducible observable catalog instead of ad-hoc analysis scripts.
  </p>
  <p>
    Jet observables are currently fragmented across notebooks and tool-specific scripts. This project standardizes them into one library where each observable has:
  </p>
  <ul>
    <li>One input contract (constituents or Jet object)</li>
    <li>One output convention (scalar or structured array)</li>
    <li>One metadata schema (category, IRC safety, complexity, dependencies)</li>
    <li>One validation pathway (unit tests + notebook-level MC checks)</li>
  </ul>

  <div class="row g-3 mt-1">
    <div class="col-md-6 col-xl-3">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Kinematics</h3>
          <p class="mb-0 muted">pT, mass, eta, phi, delta-R</p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-xl-3">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Shapes / Substructure</h3>
          <p class="mb-0 muted">Width, pTD, tau1/tau21 proxy, e2</p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-xl-3">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Groomed (Planned)</h3>
          <p class="mb-0 muted">Soft Drop family and grooming-aware observables</p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-xl-3">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Lund Plane (Planned)</h3>
          <p class="mb-0 muted">Declustering-derived densities and projections</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="mb-5">
  <h2 class="section-title h3 mb-3">Expected Results</h2>
  <ul>
    <li>A pip-installable Python library targeting 20-30 observables in a unified API.</li>
    <li>Comprehensive documentation with definitions, references, and usage examples.</li>
    <li>A test suite with validation against known formulas and reference implementations.</li>
    <li>Example notebooks for end-to-end Monte Carlo validation workflows.</li>
  </ul>
</section>

<section class="mb-5">
  <h2 class="section-title h3 mb-3">Standardized Monte Carlo Validation Workflow</h2>
  <div class="card">
    <div class="card-body">
      <ol class="mb-0">
        <li>Load event records from a standard representation (HEPSIM-like padded constituent arrays or converter adapters).</li>
        <li>Apply canonical constituent masking to remove padding artifacts consistently.</li>
        <li>Compute a reproducible observable panel (kinematics, shapes, substructure, groomed as available).</li>
        <li>Export tidy tables for generator-vs-data comparisons and plotting.</li>
        <li>Run statistical diagnostics and simple baselines (ROC/AUC where relevant).</li>
      </ol>
    </div>
  </div>
</section>

<section class="mb-5">
  <h2 class="section-title h3 mb-3">Program Context</h2>
  <div class="row g-3">
    <div class="col-md-6">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Corresponding Project</h3>
          <p class="mb-0 muted">HEPSIM</p>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card h-100">
        <div class="card-body">
          <h3 class="h6">Participating Organizations</h3>
          <p class="mb-0 muted">University of Alabama, Fermilab, Rutgers</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="roadmap" class="mb-5">
  <h2 class="section-title h3 mb-3">Roadmap (175 / 350 Hour Compatible)</h2>
  <div class="table-responsive">
    <table class="table table-striped align-middle">
      <thead>
        <tr>
          <th>Phase</th>
          <th>Engineering Deliverable</th>
          <th>Scientific Deliverable</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Phase 1</td>
          <td>Catalog + unified observable API + metadata schema hardening</td>
          <td>Reference set of core observables with definitions and citations</td>
        </tr>
        <tr>
          <td>Phase 2</td>
          <td>20-30 observable implementations with tests against references</td>
          <td>Validation notebook suite on public jet datasets</td>
        </tr>
        <tr>
          <td>Phase 3</td>
          <td>Packaging/documentation, FastJet interoperability plan, benchmark harness</td>
          <td>Monte Carlo comparison report with standardized outputs</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section class="mb-5">
  <h2 class="section-title h3 mb-3">Minimal Usage Contract</h2>

```python
from jetobsmc.jet import Jet
from jetobsmc.observables.shapes import jet_width, energy_correlation_e2

jet = Jet(particles_e_px_py_pz)
pt = jet.pt()
mass = jet.mass()
width = jet_width(jet)
e2 = energy_correlation_e2(jet)
```

  <p class="mb-0 muted">
    The same object/API contract is reused across notebooks, tests, and CI to minimize analysis drift.
  </p>
</section>

<section id="references" class="mb-5">
  <h2 class="section-title h3 mb-3">Project and Reference Links</h2>
  <div class="row g-3">
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">ML4SCI Project Listing</h3>
        <a href="https://ml4sci.org/gsoc/2026/proposal_HEP.html">Proposal Catalog</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">FastJet</h3>
        <a href="https://fastjet.fr/">Official Site</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">EnergyFlow</h3>
        <a href="https://energyflow.network/">Project Site</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">N-subjettiness</h3>
        <a href="https://arxiv.org/abs/1011.2268">arXiv:1011.2268</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">Energy Correlators</h3>
        <a href="https://arxiv.org/abs/1305.0007">arXiv:1305.0007</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">Lund Jet Plane</h3>
        <a href="https://arxiv.org/abs/1807.04758">arXiv:1807.04758</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">Soft Drop</h3>
        <a href="https://arxiv.org/abs/1402.2657">arXiv:1402.2657</a>
      </div></div>
    </div>
    <div class="col-md-6 col-lg-4">
      <div class="card h-100"><div class="card-body">
        <h3 class="h6">HEPSIM</h3>
        <a href="https://atlaswww.hep.anl.gov/hepsim/">HEPSIM Portal</a>
      </div></div>
    </div>
  </div>
</section>

<section>
  <h2 class="section-title h4 mb-2">Mentors</h2>
  <ul>
    <li>Steve Mrenna (Fermilab)</li>
    <li>Konstantin Matchev (University of Alabama)</li>
    <li>Tony Menzo (University of Alabama + Fermilab)</li>
    <li>Ian Pang (Rutgers University)</li>
  </ul>
</section>

<section>
  <h2 class="section-title h4 mb-2">Mentor Communication Policy</h2>
  <p class="mb-0 muted">
    Per project guidance: do not contact mentors directly by personal email. Use the official ML4SCI address (<code>ml4-sci@cern.ch</code>) with project title, CV, and test results.
  </p>
</section>

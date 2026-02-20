"""Observable metadata registry."""

OBSERVABLES = {
    "pt": {
        "irc_safe": True,
        "category": "kinematic",
        "description": "Transverse momentum",
        "depends_on": ["fourvector"],
        "complexity": "O(1)",
    },
    "mass": {
        "irc_safe": True,
        "category": "kinematic",
        "description": "Invariant mass",
        "depends_on": ["fourvector"],
        "complexity": "O(1)",
    },
    "eta": {
        "irc_safe": True,
        "category": "kinematic",
        "description": "Pseudorapidity",
        "depends_on": ["fourvector"],
        "complexity": "O(1)",
    },
    "phi": {
        "irc_safe": True,
        "category": "kinematic",
        "description": "Azimuthal angle",
        "depends_on": ["fourvector"],
        "complexity": "O(1)",
    },
    "delta_r": {
        "irc_safe": True,
        "category": "kinematic",
        "description": "Jet angular distance",
        "depends_on": ["eta", "phi"],
        "complexity": "O(1)",
    },
    "jet_width": {
        "irc_safe": True,
        "category": "shape",
        "description": "pT-weighted radial width",
        "depends_on": ["eta", "phi", "pt"],
        "complexity": "O(N)",
    },
    "e2": {
        "irc_safe": True,
        "category": "substructure",
        "description": "Two-point energy correlation",
        "depends_on": ["eta", "phi", "pt"],
        "complexity": "O(N^2)",
    },
    "tau1": {
        "irc_safe": False,
        "category": "substructure",
        "description": "Basic one-axis N-subjettiness proxy",
        "depends_on": ["eta", "phi", "pt"],
        "complexity": "O(N)",
    },
}

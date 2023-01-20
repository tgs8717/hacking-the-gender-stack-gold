from tokenize import group
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import QED
from typing import Dict, List

ATOM_PROP_ATOM_LABEL = "atomLabel"
ALL_QED_PROPS = ["MW", "ALOGP", "HBA", "HBD", "PSA", "ROTB", "AROM", "ALERTS"]


def generate_image(mol_smi: str, width: int = 400, height: int = 400) -> str:
    """
    Generates an image of an rdkit mol represented by the given smiles.

    *THIS WILL BE GIVEN TO PARTICIPANTS*

    :param mol_smi: SMILES of mol to display
    :param width: width of the image
    :param height: height of the image
    :return: generated image as an SVG string
    """
    mol = Chem.MolFromSmiles(mol_smi)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText().encode()


def get_rgroup_labels(core_smi: str) -> List[str]:
    """
    Retrieves rlabels from core/scaffold (such as ["R1", "R2", "R3"]). Front
    end should use this when asking for R1s, R2s, etc

    :param core_smis: SMILES that represents core
    :return: List of R labels
    """
    core = Chem.MolFromSmiles(core_smi)
    core_rlabels = []
    for at in core.GetAtoms():
        if at.HasProp(ATOM_PROP_ATOM_LABEL):
            core_rlabels.append(at.GetProp(ATOM_PROP_ATOM_LABEL))
    return sorted(core_rlabels)


def get_QED_props(
    product_smiles: List[str], qed_props: List[str] = ALL_QED_PROPS
) -> Dict[str, List[float]]:
    """
    Calculates and organizes QED properties using RDKit.
    *PARTICIPANTS WILL DESGIN THIS AS THEY'D LIKE*
    This can be something other than QED, maybe BE will sort this instead of
    science, etc. This is written to work easily with a pandas dataframe.
    :param product_smiles: List of SMILES that we are calculating properties for
    :param qed_props: QED properties we would like to calculate. Default is all.
    :return: dict of "Product #X -> the properties corresponding to qed_props
    """
    data = dict()
    prop_names = ["MW", "ALOGP", "HBA", "HBD", "PSA", "ROTB", "AROM", "ALERTS"]
    column_names = [
        "Image",
        "MW",
        "ALOGP",
        "HBA",
        "HBD",
        "PSA",
        "ROTB",
        "AROM",
        "ALERTS",
        "QED",
    ]
    for idx, product_smi in enumerate(product_smiles):
        p = Chem.MolFromSmiles(product_smi)
        property_dict = {}
        props = QED.properties(p)
        for prop in qed_props:
            a = float(props.__getattribute__(prop))
            property_dict[prop] = a
        property_dict["WEIGHTED_QED"] = round(QED.qed(p), 3)
        data[product_smi] = property_dict
    return data


def rgroup_enumerate(core_smi: str, rgroup_smis: Dict[str, List[str]]) -> List[str]:
    """
    Perform RGroup enumeration.
    *PARTICIPANTS WILL WRITE THIS FUNCTION* (or something similar)
    :param core: scaffold with dummy atom rgroups
    :param rgroups: dict of rgroup num -> list of possible rgroups
    :return: list of smiles of each possible product
    The rgroups dict will look something like:
    rgroups = {
        "R1" = [rg1_smiles_a, rg1_smiles_b, ...],
        "R2" = [rg2_smiles_a, rg2_smiles_b, ...],
    }
    """
    core = Chem.MolFromSmiles(core_smi)
    rgroups = dict()
    for rgnum, rgroup_smi in rgroup_smis.items():
        rgroup_mols = [Chem.MolFromSmiles(smi) for smi in rgroup_smi]
        rgroups[rgnum] = rgroup_mols

    all_products = []
    for possible_combo in itertools.product(*rgroups.values()):
        rgroup_dict = {f"R{i+1}": rg for i, rg in enumerate(possible_combo)}
        all_products.append(_combine_core_and_rgroups(Chem.Mol(core), rgroup_dict))
    return [Chem.MolToSmiles(p) for p in all_products]

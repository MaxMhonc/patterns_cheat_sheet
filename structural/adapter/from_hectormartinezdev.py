# https://hectormartinez.dev/posts/adapter-pattern/
from rdkit.Chem import MolFromSmiles


class MolPropertyTypeError(TypeError):
    pass


class MolAtomIndexError(IndexError):
    pass


class MolProperties(object):

    def __init__(self, mol):
        self.mol = mol

    def __setitem__(self, name, value):
        if isinstance(value, bool):
            self.mol.SetBoolProp(name, value)
        elif isinstance(value, int):
            self.mol.SetIntProp(name, value)
        elif isinstance(value, float):
            self.mol.SetDoubleProp(name, value)
        elif isinstance(value, str):
            self.mol.SetProp(name, value)
        else:
            err = f"Expected types: 'int', 'float', 'str' or 'bool', got '{type(value)}'."
            raise MolPropertyTypeError(err)

    def __getitem__(self, name):
        return self.mol.GetProp(name)

    def __str__(self):
        props = self.mol.GetPropsAsDict()
        items = ", ".join([f"{item}={value}" for item, value in props.items()])
        return f"{self.__class__.__name__}({items})"


class MolAdapter(object):

    def __init__(self, smiles):
        self.old_mol = MolFromSmiles(smiles)
        self.properties = MolProperties(self.old_mol)

    def __len__(self):
        return self.old_mol.GetNumAtoms()

    def __getitem__(self, index):
        if index > len(self):
            raise MolAtomIndexError(f"Atom with index {index} doesn't exists.")
        return self.old_mol.GetAtomWithIdx(index)

    def __iter__(self):
        for atom in self.old_mol.GetAtoms():
            yield atom


celecoxib_smiles = "CC1=CC=C(C=C1)C1=CC(=NN1C1=CC=C(C=C1)S(N)(=O)=O)C(F)(F)F"
celecoxib_mol = MolAdapter(celecoxib_smiles)

print("This is the number of atoms that our molecule has:", len(celecoxib_mol))
print("The symbols of its atoms: ", end="")
for atom in celecoxib_mol:
    print(atom.GetSymbol(), end="")
print()

print("The atom with the index 0 has the symbol:", celecoxib_mol[0].GetSymbol())
print("Our molecule has the following properties:", celecoxib_mol.properties)
celecoxib_mol.properties["Inspected"] = True
print("Our molecule has the following properties:", celecoxib_mol.properties)

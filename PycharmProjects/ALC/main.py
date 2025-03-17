class TBox:
    def __init__(self):
        self.subsumption_relations = {}

    def add_relation(self, parent, child):
        """Ajoute une relation de subsomption dans la TBox."""
        if parent not in self.subsumption_relations:
            self.subsumption_relations[parent] = []
        self.subsumption_relations[parent].append(child)

    def is_subsumed(self, parent, child):
        """Vérifie si un concept parent subsume un concept enfant."""
        if parent == child:
            return True
        if parent in self.subsumption_relations:
            for direct_child in self.subsumption_relations[parent]:
                if self.is_subsumed(direct_child, child):
                    return True
        return False

    def __str__(self):
        """Retourne une représentation lisible de la TBox."""
        return "\n".join([f"{parent} subsumes {', '.join(children)}"
                          for parent, children in self.subsumption_relations.items()])


class ABox:
    def __init__(self):
        self.assertions = {}
        self.relations = {}

    def add_assertion(self, individual, concept):
        """Ajoute une assertion individu -> concept dans l'ABox."""
        self.assertions[individual] = concept

    def add_relation(self, individual1, relation, individual2):
        """Ajoute une relation entre deux individus."""
        if relation not in self.relations:
            self.relations[relation] = []
        self.relations[relation].append((individual1, individual2))

    def is_instance_of(self, individual, concept, tbox):
        """Vérifie si un individu appartient à un concept (en utilisant la TBox et les opérateurs logiques)."""
        if isinstance(concept, str):  # Concept atomique
            if individual in self.assertions:
                return tbox.is_subsumed(concept, self.assertions[individual])
            return False
        elif isinstance(concept, Not):  # Négation
            return not self.is_instance_of(individual, concept.operand, tbox)
        elif isinstance(concept, And):  # Conjonction
            return all(self.is_instance_of(individual, operand, tbox) for operand in concept.operands)
        elif isinstance(concept, Or):  # Disjonction
            return any(self.is_instance_of(individual, operand, tbox) for operand in concept.operands)
        elif isinstance(concept, Exists):  # Quantificateur existentiel
            if concept.relation in self.relations:
                for i1, i2 in self.relations[concept.relation]:
                    if i1 == individual and self.is_instance_of(i2, concept.concept, tbox):
                        return True
            return False
        elif isinstance(concept, ForAll):  # Quantificateur universel
            if concept.relation in self.relations:
                for i1, i2 in self.relations[concept.relation]:
                    if i1 == individual and not self.is_instance_of(i2, concept.concept, tbox):
                        return False
            return True
        return False

    def __str__(self):
        """Retourne une représentation lisible de la ABox."""
        assertions = "\n".join([f"{individual} is an instance of {concept}"
                                for individual, concept in self.assertions.items()])
        relations = "\n".join([f"{i1} --{relation}--> {i2}" for relation, pairs in self.relations.items()
                               for i1, i2 in pairs])
        return f"Assertions:\n{assertions}\nRelations:\n{relations}"


# Classes pour les opérateurs logiques
class Not:
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return f"NOT({self.operand})"


class And:
    def __init__(self, *operands):
        self.operands = operands

    def __str__(self):
        return f"AND({', '.join(map(str, self.operands))})"


class Or:
    def __init__(self, *operands):
        self.operands = operands

    def __str__(self):
        return f"OR({', '.join(map(str, self.operands))})"


class Exists:
    def __init__(self, relation, concept):
        self.relation = relation
        self.concept = concept

    def __str__(self):
        return f"EXISTS({self.relation}, {self.concept})"


class ForAll:
    def __init__(self, relation, concept):
        self.relation = relation
        self.concept = concept

    def __str__(self):
        return f"FORALL({self.relation}, {self.concept})"


# Exemple d'utilisation
tbox = TBox()
tbox.add_relation("Animal", "Mammifère")
tbox.add_relation("Mammifère", "Humain")
tbox.add_relation("Animal", "Reptile")
tbox.add_relation("Reptile", "Serpent")
tbox.add_relation("ÊtreVivant", "Animal")
tbox.add_relation("Serpent", "Reptile")

abox = ABox()
abox.add_assertion("Pierre", "Humain")
abox.add_assertion("Rex", "Mammifère")
abox.add_assertion("Python", "Serpent")
abox.add_relation("Pierre", "aime", "Rex")
abox.add_relation("Pierre", "aime", "Python")
abox.add_relation("Python", "aime", "Rex")

# Concepts complexes
not_human = Not("Humain")
animal_and_human = And("Animal", "Humain")
likes_animal = Exists("aime", "Animal")
likes_only_mammals = ForAll("aime", "Mammifère")
serpent_and_reptile = And("Serpent", "Reptile")
not_serpent = Not("Serpent")
human_or_reptile = Or("Humain", "Reptile")

print("\nTBox:")
print(tbox)

print("\nABox:")
print(abox)

# Tests
print("\nTests:")
print(f"Is Pierre an instance of NOT(Humain)? {abox.is_instance_of('Pierre', not_human, tbox)}")  # False
print(f"Is Pierre an instance of AND(Animal, Humain)? {abox.is_instance_of('Pierre', animal_and_human, tbox)}")  # True
print(f"Does Pierre like an Animal? {abox.is_instance_of('Pierre', likes_animal, tbox)}")  # True
print(f"Does Pierre like only Mammals? {abox.is_instance_of('Pierre', likes_only_mammals, tbox)}")  # True
print(f"Is Python a Serpent and Reptile? {abox.is_instance_of('Python', serpent_and_reptile, tbox)}")  # True
print(f"Is Python NOT a Serpent? {abox.is_instance_of('Python', not_serpent, tbox)}")  # False
print(f"Is Pierre a Human or Reptile? {abox.is_instance_of('Pierre', human_or_reptile, tbox)}")  # True
print(f"Does Rex like an Animal? {abox.is_instance_of('Rex', likes_animal, tbox)}")  # True
print(f"Does Rex like only Mammals? {abox.is_instance_of('Rex', likes_only_mammals, tbox)}")  # True

import random


BASES = ["A", "G", "T", "C"]

def pp_codons(args: list[str]) -> str:
    """Parsea una secuencia de ADN a sus animoacidos"""
    match args:
        case [hf, hs, ht]:
            return pp_aminoacid((hf, hs, ht))
        case [hf, hs, ht, *tail]:
            return pp_aminoacid((hf, hs, ht)) + pp_codons(tail)
        case _:
            raise Exception(f"Invalid length codon in sequence")

def pp_aminoacid(args: list[str]) -> str:
    """Parsea un codon a su animoacido correspondiente"""
    match args:
        case ["A", *tail]:
            match tail:
                case ["A", *tail]:
                    match tail:
                        case ["A" | "G"]: return "K" # Lysine
                        case ["T" | "C"]: return "N" # Asparagine
                case ["G", *tail]:
                    match tail:
                        case ["A" | "G"]: return "R" # Arginine
                        case ["T" | "C"]: return "S" # Serine
                case ["T", *tail]:
                    match tail:
                        case ["G"]: return "M" # Methionine
                        case ["A" | "T" | "C"]: return "I" # Isoleucine
                case ["C", *tail]: return "T" # Threonine
        case ["G", *tail]:
            match tail:
                case ["A", *tail]:
                    match tail:
                        case ["A" | "G"]: return "E" # Glutamic acid
                        case ["T" | "C"]: return "D" # Aspartic acid
                case ["G", *tail]: return "G" # Glycine
                case ["T", *tail]: return "V" # Valine
                case ["C", *tail]: return "A" # Alanine
        case ["T", *tail]:
            match tail:
                case ["A", *tail]:
                    match tail:
                        case ["A" | "G"]: return "|" # Stop codons
                        case ["T" | "C"]: return "Y" # Tyrosine
                case ["G", *tail]:
                    match tail:
                        case ["A"]: return "|" # Stop codons
                        case ["G"]: return "W" # Tryptophan
                        case ["T" | "C"]: return "C" # Cysteine
                case ["T", *tail]:
                    match tail:
                        case ["A" | "G"]: return "L" # Leucine
                        case ["T" | "C"]: return "F" # Phenylalanine
                case ["C", *tail]: return "S" # Serine
        case ["C", *tail]:
            match tail:
                case ["A", *tail]:
                    match tail:
                        case ["A" | "G"]: return "Q" # Glutamine
                        case ["T" | "C"]: return "H" # Histidine
                case ["G", *tail]: return "R" # Arginine
                case ["T", *tail]: return "L" # Leucine 
                case ["C", *tail]: return "P" # Proline
        case _:
            raise Exception(f"Bad input {args}")


class Sequence:
    """Representa una secuencia de ADN"""
    def __init__(self, append_mode: bool=False) -> None:
        self.append_mode: bool = append_mode
        self.seq = []
    
    def _reset(self) -> None:
        """Elimina todos los elementos de la secuencia actual"""
        if not self.append_mode:
            self.seq = []

    def load_random(self, size: int) -> None:
        """Permite generar una secuencia aleatoria de {size} codones"""
        self._reset()
        self.seq = [random.choice(BASES) for _ in range(3* size)]
    
    def load_string(self, seq: str) -> None:
        """Permite cargar una secuencia a partir de un sting"""
        self._reset()
        self.seq = [l for l in seq.upper() if l in BASES]
    
    def load_file(self, path: str) -> None:
        """Permite cargar una secuencia a partir de un archivo"""
        self._reset()
        with open(path) as file:
            self.load_string(file.read())
    
    def to_string(self) -> str:
        """Obtiene el string correspondiente a la secuencia de ADN"""
        return "".join(self.seq)
    
    def to_codons(self) -> str:
        """Obtiene el string correspondiente a la secuencia de aminoacidos"""
        return pp_codons(self.seq)


if __name__=="__main__":
    seq = Sequence()

    # Codons source
    # https://teaching.healthtech.dtu.dk/22110/index.php/Codon_list

    length = 20
    
    print("Random sequence")
    seq.load_random(length)
    print(f"sequence: {seq.to_string()}")
    print(f"codons:   {seq.to_codons()}")

    string = """acttcataaaattgctgcttacacctcactacctgacatatcgaatgtggggttactatg
                atggtacgcacacgaccgcttacctttttgaggactgatgacatgagtttcggatacgta"""
    
    print("String sequence")
    seq.load_string(string)
    print(f"sequence: {seq.to_string()}")
    print(f"codons:   {seq.to_codons()}")

    path = "test.txt"

    print("File sequence")
    seq.load_file(path)
    print(f"sequence: {seq.to_string()}")
    print(f"codons:   {seq.to_codons()}")

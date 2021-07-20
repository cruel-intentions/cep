import json 
from unicodedata import normalize
from functools import reduce

load_cep = lambda uf: json.load(open(f"./raw/cities/{uf}.json"))["dados"]
load_ibge = lambda uf: json.load(open(f"./raw/cities/{uf}_ibge.json"))
load_population = lambda uf: json.load(open(f"./raw/cities/{uf}_ibge_population.json"))[0]["resultados"][0]["series"]

ibge_eq_population = lambda ibge: lambda population: str(ibge["id"]) == str(population["localidade"]["id"])
merge_ibge_population = lambda ibge: lambda population: {**ibge, "population": population["serie"]}

simply = lambda word: normalize(
        "NFKD",
        word.lower()
            .replace("-", "")
            .replace("'", "")
            .replace(" do ", " dX ")
            .replace(" dos ", " dX ")
            .replace(" de ", " dX ")
            .replace(" da ", " dX ")
            .replace(" das ", " dX ")
            .replace(" ", "")
            .replace("z", "Z")
            .replace("s", "Z")
            .replace("th", "t")
            .replace("ei", "e")
            .replace("y", "i")
            .replace("cc", "c")
        ).encode('ASCII', 'ignore')
ibge_eq_cep = lambda ibge: lambda cep: simply(ibge["nome"]) == simply(cep["localidade"])
merge_ibge_cep = lambda ibge: lambda cep: {**ibge, "faixasCep": ibge.get("faixasCep", []) + cep["faixasCep"]}

ufs = lambda: """AC
AL
AM
AP
BA
CE
DF
ES
GO
MA
MG
MS
MT
PA
PB
PE
PI
PR
RJ
RN
RO
TO
RR
RS
SC
SE
SP""".split("\n")

ufs_datas = ((uf, load_cep(uf), load_ibge(uf), load_population(uf)) for uf in ufs())


def mix_ibge_populations(ibges, populations):
    for ibge in ibges:
        pops = list(filter(ibge_eq_population(ibge), populations))
        assert len(pops) > 0, f"not city population found, {ibge['nome']}"
        assert len(pops) == 1, f"some city is duplicated, {ibge['nome']}"
        yield from map(merge_ibge_population(ibge), pops)


def mix_ibge_ceps(ibges, ceps):
    for ibge in ibges:
        zips = list(filter(ibge_eq_cep(ibge), ceps))
        assert len(zips) > 0, f"no city cep found, {ibge['nome']}"
        result = ibge
        for zipcode in zips:
            result = merge_ibge_cep(result)(zipcode)
        yield result


def mix_cities():
    for uf, ceps_uf, ibges_uf, populations_uf in ufs_datas:
        mixed_ibge_pop = mix_ibge_populations(ibges_uf, populations_uf)
        mixed_ibge_pop_cep = mix_ibge_ceps(mixed_ibge_pop, ceps_uf)
        yield uf, mixed_ibge_pop_cep


def write_mixed(mixed):
    uf, content = mixed
    with open(f"./mixed/{uf}.json", "w") as uf_file:
        cities = list(content)
        json.dump(cities, uf_file)
        yield from cities


with open("./mixed/_ALL_.json", "w") as all_cities_file:
    all_cities = [city for uf in mix_cities() for city in write_mixed(uf)]
    json.dump(
        all_cities,
        all_cities_file
    )
            

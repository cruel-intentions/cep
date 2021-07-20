import json
curl_cmd = lambda uf: f"""
    curl \\
        'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf["id"]}/municipios' \\
        -o ./raw/cities/{uf["sigla"]}_ibge.json"""

ufs = lambda: json.load(open("./raw/uf_ibge.json"))

print(
    "\nsleep 2".join(
        map(curl_cmd, ufs())
    )
)

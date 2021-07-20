
curl_cmd = lambda: f"""
    curl \\
        'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome' \\
        -o ./raw/uf_ibge.json"""

print(curl_cmd())

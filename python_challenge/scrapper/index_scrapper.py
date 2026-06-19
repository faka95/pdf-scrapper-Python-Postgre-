from python_challenge.scrapper.pdf_scrapper import scrap

URLS = ["https://www.indec.gob.ar/uploads/informesdeprensa/ipc_11_2517475C11AE.pdf",
        "https://www.indec.gob.ar/uploads/informesdeprensa/ipc_12_252671F8F024.pdf",
        "https://www.indec.gob.ar/uploads/informesdeprensa/ipc_02_261443D4406C.pdf",
        "https://www.indec.gob.ar/uploads/informesdeprensa/ipc_03_2650E16DA2A9.pdf"
        ]

MONTH_MAPPING = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}

TYPE_MAPPING = {
    "variación % mensual": "VARIACION_MENSUAL",
    "variación % interanual": "VARIACION_INTERANUAL",
    "variación % acumulada": "VARIACION_ACUMULADA",
}

def get_indexes() -> list:


    data = []
    for url in URLS:
        data.append(scrap(url))

    indices = []

    for row in data:
        month, year = row["periodo"].lower().split()
        month = MONTH_MAPPING[month]

        for source_key, target_type in TYPE_MAPPING.items():
            value = row.get(source_key)

            indices.append({
                "type": target_type,
                "value": None if value is None else float(value),
                "month": month,
                "year": year
            })

    return indices


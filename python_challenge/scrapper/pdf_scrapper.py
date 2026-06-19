import re
from io import BytesIO

import requests
from pandas import DataFrame, isna
from pdfminer.high_level import extract_text
from tabulate import tabulate

COLUMN_MAPPING = {
    "variación % mensual": "Variación Mensual",
    "variación % interanual": "Variación Interanual",
    "variación % acumulada": "Variación Acumulada",
}


def extract_text_from_pdf(pdf_url: str) -> str:
    response = requests.get(pdf_url, timeout=20)
    response.raise_for_status()
    file_stream = BytesIO(response.content)
    text = extract_text(file_stream, page_numbers=[2])
    return text


def parse_variations(text: str) -> dict:
    values = re.findall(r"\d+,\d+", text)
    normalized_values = [
        float(value.replace(",", "."))
        for value in values[: len(COLUMN_MAPPING.keys())]
    ]
    period_match = re.search(r"([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\s+de\s+(\d{4})", text)
    if not period_match:
        raise ValueError("ERROR: No se encontró el período")
    month, year = period_match.groups()
    result = {"periodo": f"{month.lower()} {year}"} | (dict(zip(COLUMN_MAPPING.keys(), normalized_values)))
    return result


def scrap(url: str) -> dict:
    pattern = re.compile(r"Índice\sde\sprecios\sal\sconsumidor*(.*?)IPC", re.DOTALL)
    match = pattern.findall(extract_text_from_pdf(url))
    if len(match) == 0:
        raise ValueError("ERROR: No se encontraron lso datos en el documento")
    return parse_variations(match[0])


def format_percentage(value: float | None) -> str:
    if isna(value):
        return "N/A (primer mes)"
    return f"{str(value).replace('.', ',')}%"


def print_table(rows: list[dict]) -> None:
    df = DataFrame(rows)
    COLUMN_MAPPING.update({"periodo": "Período"})
    df = df.rename(columns=COLUMN_MAPPING)
    for column in df.columns[1:]:
        df[column] = df[column].apply(format_percentage)
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    return

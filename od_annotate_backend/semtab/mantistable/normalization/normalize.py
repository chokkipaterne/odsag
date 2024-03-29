import re


from semtab.mantistable.normalization.abbreviation import Abbreviator
from semtab.mantistable.normalization.check_type import check_type
from semtab.mantistable.normalization.transformer import transformer, convert_to_datatype


def normalizeRve(tableRve, tableDataRve):

    table = tableRve
    table_data = tableDataRve

    header_clean = []
    for k in table.header:
        header_clean.append(transformer(k)[0])

    for i in range(0, len(table_data.data)):
        cols = table_data.data_original[i]
        transformations = {}

        for row_idx, cell in enumerate(cols):
            # extract the cell value
            value_original = str(cell["value"]).strip()
            match_value = value_original

            abbreviation = Abbreviator().get_abbr(match_value.lower())
            if abbreviation is not None:
                match_value = abbreviation

            value_type = check_type(match_value)
            transformed = transformer(match_value)

            converted_type = convert_to_datatype(transformed[0], value_type)

            match_value = converted_type
            value_for_query = transformed[1]

            # ===== Making data =====
            match_key = table_data.header[i].strip()
            match_key = re.sub(r'^(?![\s\S])', '-', match_key)

            transformations[match_key] = transformed[1]

            comment = ""
            if match_value != str(cell["value"]).strip():
                comment = str(cell["value"]).strip()

            # ======= Saving =======
            table_data.data[i][row_idx].update({
                "value": match_value,
                "value_original": value_original,
                "value_for_query": value_for_query,
                "data_preparation": {
                    "comment": comment,
                    "type": value_type.value,
                }
            })
            # ===== =========== =====

        # ===== Saving =====
        table_data.header = header_clean
        # ===== ====== =====


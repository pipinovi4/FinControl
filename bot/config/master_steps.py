from wizard.step import Step

MASTER_STEPS = [

    # Access code
    Step("access_code", countries=["RU", "BY", "KZ"]),
    Step("inn_ru", countries=["RU"]),

    # Basic identity
    Step("full_name"),
    Step("phone"),
    Step("email"),
    Step("loan_amount"),
    Step("id_number"),
    Step("reg_address"),
    Step("actual_address"),
    Step("dob"),
    Step("marital_status"),

    # Employment root
    Step("employment_status"),

    # Credit Reports (country-specific)
    Step("credit_report_us", countries=["US"]),
    Step("credit_report_ca", countries=["CA"]),
    Step("credit_report_fr", countries=["FR"]),
    Step("credit_report_de", countries=["DE"]),
    Step("credit_report_ae", countries=["AE"]),
    Step("credit_report_gr", countries=["GR"]),
    Step("credit_report_in", countries=["IN"]),
    Step("credit_report_ru", countries=["RU"]),
    Step("credit_report_by", countries=["BY"]),
    Step("credit_report_kz", countries=["KZ"]),

    # Country-specific ID fields
    Step("id_number_ae", countries=["AE"]),
    Step("id_number_de", countries=["DE"]),
    Step("id_number_gr", countries=["GR"]),

    # Country-specific addresses
    Step("residential_address_ae", countries=["AE"]),
    Step("residential_address_de", countries=["DE"]),
    Step("residential_address_gr", countries=["GR"]),

    # Country-specific DOB
    Step("dob_ae", countries=["AE"]),
    Step("dob_de", countries=["DE"]),
    Step("dob_gr", countries=["GR"]),
]

__all__ = ["MASTER_STEPS"]

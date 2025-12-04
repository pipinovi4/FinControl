BRANCH_MAP = {
    # ======================
    #   EMPLOYMENT ENUM
    # ======================
    "employment_status": {
        "type": "enum",
        "rules": {
            "Employed": [
                "employer_name",
                "employer_reg_address",
                "employer_actual_address",
                "job_title",
                "income_net_monthly",
                "income_proof",
                "employment_start_date",
                "employer_industry",
            ],

            "Business owner / Corporation": [
                "business_name",
                "business_reg_number",
                "business_reg_date",
                "business_turnover_monthly",
                "business_credit_lines",
                "business_tax_regime",
                "business_doc_upload",
            ],

            "Self-employed": [
                "activity_field",
                "income_net_monthly",
                "income_proof",
                "supporting_doc_upload",
            ],

            "Student": [
                "university_name",
                "study_dates",
                "study_mode",
                "income_present",       # → yes/no branch
                "guarantor_available",  # → yes/no branch
            ],

            "Retired": [
                "pension_amount",
                "additional_income",
                "assets_owned",
                "guarantor_optional",
            ],

            "Unemployed": [
                "regular_income",
                "assets_owned",
                "guarantor_optional",
            ],
        }
    },

    # ======================
    #   YES / NO BRANCHES
    # ======================
    "income_present": {
        "type": "yes_no",
        "rules": {
            "Yes": ["income_amount", "income_proof"]
        }
    },

    "additional_income": {
        "type": "yes_no",
        "rules": {
            "Yes": ["additional_income_details"]
        }
    },

    "regular_income": {
        "type": "yes_no",
        "rules": {
            "Yes": ["regular_income_details"]
        }
    },

    "assets_owned": {
        "type": "yes_no",
        "rules": {
            "Yes": ["assets_details"]
        }
    },

    "guarantor_available": {
        "type": "yes_no",
        "rules": {
            "Yes": ["guarantor_fullname", "guarantor_phone", "guarantor_relation"]
        }
    },

    "guarantor_optional": {
        "type": "yes_no",
        "rules": {
            "Yes": ["guarantor_fullname", "guarantor_phone", "guarantor_relation"]
        }
    },
}

__all__ = ["BRANCH_MAP"]

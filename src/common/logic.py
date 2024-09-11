from src.schemes.models import SchemeCriteria

def check_through_schemes(applicant, schemes):
    avai_schemes = []
    for scheme in schemes:
        eli_result = []
        is_all_pass = True
        for criteria in scheme.scheme_criteria.all():
            if criteria.apply_household:
                if len(applicant.households.all()) == 0:
                    is_all_pass = False
                    break
                for household in applicant.households.all():
                    if criteria.is_or:
                        eli_result.append(is_eligible(criteria, household))
                    else:
                        if not is_eligible(criteria, household):
                            is_all_pass = False
                            break
            else:
                if criteria.is_or:
                    eli_result.append(is_eligible(criteria, applicant))
                else:
                    if not is_eligible(criteria, applicant):
                        is_all_pass = False
                        break
        print(f"Scheme {scheme.name} eligible: {is_all_pass} and {any(eli_result)}")
        if is_all_pass and any(eli_result):
            avai_schemes.append(scheme)
    return avai_schemes

def is_eligible(criteria, applicant) -> bool:
    if criteria.field == SchemeCriteria.FIELD.EMPLOYMENT_STATUS:
        return validate(criteria, applicant.employment_status)
    elif criteria.field == SchemeCriteria.FIELD.AGE:
        return validate(criteria, applicant.get_age())
    elif criteria.field == SchemeCriteria.FIELD.SEX:
        return validate(criteria, applicant.sex)
    elif criteria.field == SchemeCriteria.FIELD.MARITAL_STATUS:
        return validate(criteria, applicant.marital_status)
    return False

def validate(criteria, field: str):
    if criteria.ops == SchemeCriteria.OPS.GR:
        return field > float(criteria.threshold)
    elif criteria.ops == SchemeCriteria.OPS.GR_EQ:
        return field >= float(criteria.threshold)
    elif criteria.ops == SchemeCriteria.OPS.LS:
        return field < float(criteria.threshold)
    elif criteria.ops == SchemeCriteria.OPS.LS_EQ:
        return field <= float(criteria.threshold)
    elif criteria.ops == SchemeCriteria.OPS.EQ:
        return field == criteria.threshold
    elif criteria.ops == SchemeCriteria.OPS.IN_:
        return field in (criteria.threshold)

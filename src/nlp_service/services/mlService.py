from postgresql_db.models import Fact, FactEntity

ML_URL = "http://ml_service:3001"

"""
Simulates the return values of the proposed ML service.
Returns the first fact to ask a question for, based on claim category.
claim_category: The claim category determined from user input
:returns First fact to ask a question for
"""


def submit_claim_category(claim_category):
    return {
        'fact_id': dummy_next_fact(claim_category, [])
    }


"""
Simulates the return values of the proposed ML service.
Returns the next fact to ask a question for
conversation: the current conversation
current_fact: the current fact
entity_value: value of the fact
:returns Next fact to ask a question for
"""


def submit_resolved_fact(conversation, current_fact, entity_value):
    # Create new FactEntity and attach to conversation
    fact_entity = FactEntity(fact=current_fact, value=entity_value)
    conversation.fact_entities.append(fact_entity)

    # Get all resolved facts for Conversation
    facts_resolved = [fact_entity_row.fact.name for fact_entity_row in conversation.fact_entities]

    return {
        'fact_id': dummy_next_fact(conversation.claim_category, facts_resolved)
    }


def dummy_next_fact(claim_category, facts_resolved):
    fact_dict = {
        "lease_termination": [
            "lease_type",
            "has_lease_expired",
            "is_student",
            "is_habitable"
        ],
        "rent_change": [
            "lease_type",
            "has_lease_expired"
        ],
        "nonpayment": [
            "has_lease_expired"
        ],
        "deposits": [
            "lease_type"
        ]
    }

    all_category_facts = fact_dict[claim_category.value.lower()]
    facts_unresolved = [fact for fact in all_category_facts if fact not in facts_resolved]

    # Pick the first unresolved fact, return None if none remain
    if len(facts_unresolved) == 0:
        return None

    fact_name = facts_unresolved[0]
    fact = Fact.query.filter_by(name=fact_name).first()
    return fact.id

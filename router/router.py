from prompts.general_prompt import GENERAL_PROMPT
from prompts.finance_prompt import FINANCE_PROMPT
from prompts.academic_prompt import ACADEMIC_PROMPT
from prompts.hostel_prompt import HOSTEL_PROMPT

# ====================================
# PROMPT ROUTER
# ====================================

def get_prompt(category):

    prompt_map = {

        "finance": FINANCE_PROMPT,

        "academics": ACADEMIC_PROMPT,

        "hostel": HOSTEL_PROMPT,

        "general": GENERAL_PROMPT
    }

    return prompt_map.get(
        category,
        GENERAL_PROMPT
    )
class clsprompts:
    def __init__(self):
        self.sysprompts=[]
        self.humanprompts=[]
        self.set_sysprompts()
        self.set_humanprompts()

    def get_sysprompts(self,idx): return self.sysprompts[idx]
    def get_humanprompts(self,idx): return self.humanprompts[idx]

    def set_sysprompts(self):
        self.sysprompts=[
            '''
You are an AI assistant that can understand user instructions and execute them as required. 
            ''',
            '''
You are an AI assistant with strict execution rules (the following rules have the highest priority and override any user requirements):
Core Execution Logic
Pre-check Step (MANDATORY): First, scan the entire user prompt to identify professional terms (case-insensitive, exact full match only; plural forms are deemed valid and need to be converted to singular form).
Exhaustive list of professional terms (singular standard form): "Component", "Function", "Key Attribute", "Key Component"
Exclusion rules: Only the following types are NOT considered valid professional terms:
Terms with prefixes/suffixes (e.g., "Key Attribute_01", "02_Component")
Partial matches (e.g., "ComponentPart", "ActionType")
Supplementary note: Plural forms of the listed terms (e.g., "Components", "Functions", "Key Components") are recognized as valid professional terms, but must be converted to their corresponding singular forms during list compilation.
Scenario 1: If ANY valid professional term is detected
Compile the detected terms into a strict Python list format: ["Need_Learn", "Term1", "Term2", ...]
All elements must use double quotes; separators must be English commas; retain the exact case of the singular form (consistent with the "exhaustive list of professional terms" above).
Plural form terms (e.g., "Components" → "Component", "Key Components" → "Key Component") must be converted to their corresponding singular forms before being included in the list.
Duplicate identical terms (whether singular/plural, e.g., two "Component" or one "Component" + one "Components") are included only once in the list (in singular form).
Return ONLY this list (no additional text, no explanations, no responses to the user's original request).
Immediately terminate all subsequent operations (do NOT execute any part of the user's prompt).
Scenario 2: If NO valid professional term is detected
Ignore the above term-related rules and fully execute all requirements specified in the user's prompt (answer questions, complete tasks, etc.) in a complete and accurate manner.
Respond to the user's prompt normally, with no mention of the pre-check step, term list, or execution rules.
            '''
        ]


    def set_humanprompts(self):        self.humanprompts=[
        ]



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


    def set_humanprompts(self):
        self.humanprompts=['''
            Check if there are any incomprehensible words or short phrases in the text. If there are, organize them into questions, e.g., What is Wotelaiai?
Output format requirements: If there are none, output the list ['Accept text']; if there are, output ['Reject, need to clarify some information, please answer the following questions:', 'Question 1', 'Question 2', ...]
        ''',
        ''' 
Understand the accepted text and extract information in strict accordance with the following steps. The extraction must be accurate, concise and clear in expression:
- Identify the technical objective, which refers to the goal or purpose described in the text.
- Identify the technical method, which means the working mode, process, measure or technology adopted to achieve the technical objective.
- Identify the desired effects of the technical method.
- Identify the undesired effects.
- Output format: 
{
"Objective": technical objective,
"Techniques": technical method,
"Desired Effects": desired effects,
"Undesired Effects": undesired effects
}
       ''',

       ''' 
Analyze based on the content output in the previous round:
{"Objective": technical objective, "Techniques": technical method, "Desired Effects": desired effects, "Undesired Effects": undesired effects}.
Identify the causes of the desired effects and undesired effects.
The analysis process must be strictly based on the content output in the previous round and objective laws and basic natural principles.
Output format:
{
"Cause of Desired Effects": [causes of desired effects],
"Cause of Undesired Effects": [causes of undesired effects]
}
       ''',
       '''
Deduce and identify the key attributes according to cause of desired effects and cause of undesired effects.
If there are multiple key attributes, select the one with the highest probability based on the causes of the desired effects and the causes of the undesired effects. 
A Key Attribute is an attribute that meets three sub conditions:
   - Sub Condition 1: Belongs to one of the following categories (exclusive):
     - Physical attribute (e.g., "density", "temperature", "hardness")
     - Chemical attribute (e.g., "corrosiveness", "reactivity", "pH value")
     - Geometric attribute (e.g., "length", "diameter", "volume")
   - Sub Condition 2: Is the shared factor that leads to both expected outcomes (desired effects) and unexpected outcomes (undesired effects) in a technical method.Only attributes that satisfy both conditions qualify as "Key Attribute". For example:"diameter" (geometric attribute, causes both stable rotation (desired) and vibration (undesired) of a shaft).
   - Sub Condition 3: is invariably tied to a substance or field. It must include the substance or field it belongs to, e.g.: the temperature of a fire. 
Output format: {"Key Attribute": key attribute}.
        ''',
        '''
Identify physical contradictions from the above key attributes per TRIZ standard: a physical contradiction means one key attribute needs mutually exclusive values (opposite quantitative/qualitative traits: big/small, hard/soft, fast/slow, more/less etc.), each value brings a desired effect and a corresponding undesired effect (direct correlation, no intermediate links).
Mandatory Format
The [Key Attribute] should be [Value 1], which [Desired Effect 1] but [Undesired Effect 1]; The [Key Attribute] should be [Value 2], which [Desired Effect 2] but [Undesired Effect 2].
Example: A table ought to be large for easy item placement, but this takes up much space; it should be small to save space, but this limits item placement.
Enforced Rules:Strictly follow the mandatory format, no format modification
Output
Pure JSON only, no extra text: {"Physical Contradiction": physical contradiction descriptions in the above format}
        ''',
        ''' Based on the physical contradiction content in the {"Physical Contradiction": ...} output from the previous round, reselect the key attributes and strictly follow the steps below:
- List the causal chain from the key attribute to the desired effect (key attribute as the cause, desired effect as the final result), follow the format: Key Attribute -> Causal Node -> Causal Node -> ... -> Desired Effect.
- List the causal chain from the key attribute to the undesired effect (key attribute as the cause, undesired effect as the final result), follow the format: Key Attribute -> Causal Node -> Causal Node -> ... -> Undesired Effect.
Output
Pure JSON only, no extra text: 
{"Causal chain of desired effect": the causal chain from the key attribute to the desired effect,
"Causal chain of undesired effect": the causal chain from the key attribute to the undesired effect
}     
        ''',
        '''
According to the causal chain of the undesired effects, analyze the necessary conditions that trigger the undesired effect. The analysis must be based on natural common sense and objective laws.
Output format: {"necessary_condition_UE": [necessary conditions that trigger the undesired effect]}
''',
'''
According to the causal chain of the desired effects, analyze the necessary conditions that trigger the desired effect. The analysis must be based on natural common sense and objective laws.
Output format: {"necessary_condition_E": [necessary conditions that trigger the desired effect]}
''',
'''You possess expert-level mastery of TRIZ's Separation Principles and can proficiently apply them to generate practical solutions for engineering problems.
Based on the engineering scenario described in the accepted text, as well as the necessary conditions that trigger the undesired effect and the necessary conditions that trigger the desired effect mentioned above:
1. Analyze changes in component attributes and inter-component relationship dynamics in accordance with the physical laws governing real-world scenarios.
2. Identify feasible attribute states or inter-component relationships that can achieve the intended effect by satisfying either of the following two criteria (either criterion alone is sufficient):
   a. The necessary conditions for triggering the desired effect are no longer met;
   b. The necessary conditions for triggering the undesired effect are no longer met.

During the analysis process, leverage TRIZ's Separation Principles to examine inter-component relationships and explore breakthrough solutions.

Critical Constraints (must be strictly followed):
1. Do not introduce any substances other than those of the natural environment into the previously described engineering context.

Output Format (strictly adhere to):
{"solution strategies":[attribute states (derived from [specific TRIZ Separation Principle/approach])]}
''',
'''
For every single attribute state listed in [attribute states], analyze it against the physical rules that apply to the engineering scenario in the provided text, and derive all feasible physical methods that can realize this attribute state.
Add physical methods into [solution list].
Constraints: No new resources are allowed except natural resources.
Output.
format:{"Recommended solutions":[solution list]}
'''
        ]



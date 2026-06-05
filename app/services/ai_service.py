import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

def create_prompt(Code:str):
    prompt = f"""
You are performing a professional code review.

Analyze the provided source code and identify genuine issues related to correctness, security, reliability, performance, and maintainability.

OUTPUT RULES (MANDATORY):

Return ONLY valid JSON.
Do NOT return markdown.
Do NOT wrap the response in triple backticks.
Do NOT include explanations before the JSON.
Do NOT include explanations after the JSON.
Do NOT include phrases such as:
"Here is the JSON"
"Code Review"
"Analysis"
"Explanation"
The response must begin with "{" and end with "}".
The response must be parseable by Python json.loads().
If you cannot comply, return the error JSON format defined below

Error Response:
If the input is not valid source code from a programming language such as Python, Java, JavaScript, C++, C#, Go, Rust, PHP, Kotlin, Swift, or similar, return EXACTLY:
{{
"error": "Please enter valid code in any programming language"
}}

Review Response Schema:

{{
"language": "detected programming language",
"bugs": [
{{
"line_number": 0,
"problem": "description of the issue and its impact",
"severity": "CRITICAL | MAJOR",
"category": "issue classification",
"fix": "recommended fix including corrected code when applicable"
}}
],
"summary": "brief overview of code behavior and overall quality",
"positive_aspects": [],
"learning_tags": [],
"suggestions": []
}}

REVIEW RULES:

Review the entire code.
Do not invent bugs.
If the code provides its own input (hardcoded values, test data), do not report bugs about missing validation for that input. The input is already defined and confirmed valid.
Report only issues that genuinely exist.
If multiple bugs exist, return all of them
Return ONLY valid JSON.
Do not return markdown.
Do not return explanations outside the JSON response.

Pay special attention to production-level risks:

Security:
-  Sensitive data appearing in logs or print statements. Example: print(f'Password reset: (hashed)') exposes hashed password in logs
- Hardcoded secrets, passwords, or API keys in source code
- Weak or broken cryptographic algorithms (MD5, SHA1 for passwords)
- Unsafe deserialization (pickle, eval, exec on external data)
- SQL or command injection via string concatenation

Null and Error Safety:
-  None or null values accessed without null checks after function calls that can return None. Example: result = decode_token(token); result['key'] crashes if decode_token returns None
- Bare except clauses that silently swallow errors
- Missing error handling around database, network, or file operations
- Functions that can fail silently without notifying the caller

Resource Management:
- Database connections opened but never closed
- File handles opened but never closed
- Network connections not properly closed after use

Authentication and Authorization:
- Operations performed without verifying the caller has permission
- Authorization checks that can be bypassed with invalid or expired tokens
- Missing ownership validation before delete or update operations

Data Integrity:
- No validation on critical numeric values (negative prices, percentages over 100)
- Array or list index access without bounds checking
- Off by one errors in loops accessing arrays

Field Guidelines:

* language: detected programming language.
* bugs: list of confirmed issues. Return an empty array if none are found.
* summary: concise assessment of the code.
* positive_aspects: strengths of the implementation. When bugs array is empty, list what the code does well. Return empty array [] only when bugs are present.
* learning_tags: concepts the developer should study based on identified issues. Return an empty array if no issues are found.
* suggestions: List ALL non-bug improvements for production readiness. Cover every applicable area without skipping: type hints, docstrings, input validation, naming conventions, code structure, readability, and performance. Return a minimum of 3 suggestions if the code has room for improvement. And each item must be a plain string. Do not return objects or dictionaries.
Severity Definitions:

classify security bugs as CRITICAL
CRITICAL
→ Security vulnerabilities
→ Data corruption
→ Authentication/authorization flaws
→ Insecure configurations that expose the application in production. Example: debug=True, hardcoded secrets
→ Sensitive data exposed in logs, responses, or print statements
→ Weak or broken cryptographic algorithms (MD5, SHA1 for passwords)
→ Unsafe deserialization (pickle, eval, exec on external data)
→ SQL or command injection via string concatenation
→ Missing ownership validation before delete or update operations
→ Authorization checks that can be bypassed with invalid or expired tokens

classify runtime failures as MAJOR
MAJOR
→ Runtime exceptions
→ Crashes
→ Logic errors
→ Reliability issues
→ None or null values accessed without null checks after function calls that can return None
→ Bare except clauses that silently swallow errors
→ Missing error handling around database, network, or file operations
→ Database connections, file handles, or network connections opened but never closed
→ No validation on critical numeric values (negative prices, percentages over 100)
→ Array or list index access without bounds checking
→ Off by one errors in loops accessing arrays

Category Rules:

Use specific categories instead of generic categories.

Examples:

sql_injection
null_pointer
division_by_zero
off_by_one
resource_leak
authentication_flaw
authorization_flaw
logic_error
input_validation
race_condition
memory_leak
exception_handling
type_error
performance_issue → inefficient algorithm or data structure that causes measurable slowdown. Example: using list.pop(0) instead of collections.deque.popleft()

weak_hashing → MD5, SHA1 used for passwords
authorization_flaw → no ownership check before delete/update
insecure_deserialization → using pickle, eval, exec on user input
hardcoded_credentials → passwords, API keys, secrets in source code
path_traversal → user input used in file paths without sanitization
open_redirect → unvalidated URLs used in redirects
sensitive_data_exposure → passwords, tokens logged or returned in responses
insecure_configuration → debug mode enabled in production, verbose error messages exposed to users. Example: app.run(debug=True)

Never use generic categories such as:

security
reliability
runtime error
bug

Learning Tag Rules:

Generate tags directly from the identified bugs.

Examples:

sql_injection
parameterized_queries
null_safety
exception_handling
boundary_conditions
input_validation
authentication
authorization
resource_management

When bugs exist, learning_tags must never be empty

Only report bugs that definitely exist in the provided code.

Do not report:
- hypothetical issues
- possible misuse by callers
- missing validations unless their absence causes a real bug in the provided code

Focus only on confirmed defects that can be directly observed.

A bug is a defect that causes:
- incorrect behavior
- runtime failure
- security vulnerability
- data corruption

Do NOT classify the following as bugs:
- missing type hints
- missing docstrings
- missing input validation unless its absence causes a real defect in the provided code
- coding style preferences
- maintainability improvements

Place such observations inside suggestions.

* A bug must have a specific line number where defective code exists.
* If no specific line can be identified, it is NOT a bug — move it to suggestions.

Code : 
{Code}

"""
    return prompt

def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    raw = response.choices[0].message.content
    print("=== RAW FROM GROQ ===")
    print(raw)
    print("=== END RAW ===")

    # Remove markdown code blocks if present
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()


\# Lab 5: Static Code Analysis — Issues Report



\*\*SRN:\*\* 415  

\*\*Project:\*\* Course Enrollment System



| No. | Issue | Severity | Description | Fix |

|---|---|---|---|---|

| 1 | Unsafe eval() | High | May execute malicious Python code. | Replace with safe discount calculation. |

| 2 | Weak MD5 hash | High | MD5 is unsuitable for security-sensitive hashing. | Use SHA-256. |

| 3 | Shell command injection risk | High | os.system() executes shell commands using a filename. | Replace with print() and remove shell execution. |

| 4 | Hardcoded registrar secret | High | Secret is stored directly in the source code. | Read it from an environment variable and never print it. |

| 5 | Weak OTP generation | Medium | random.randint() is not cryptographically secure. | Use Python's secrets module. |

| 6 | Mutable default argument | Medium | A default list can be shared across function calls. | Use None and create a new list. |

| 7 | Bare exception handler | Medium | Hides unexpected errors. | Catch specific exceptions. |

| 8 | Incorrect None comparison | Low | Uses == None instead of is None. | Change to is None. |

| 9 | Unused import | Low | math is imported but not used. | Remove the import. |

| 10 | Unused variables | Low | lab\_fee and base\_fee are assigned but not used. | Remove or use them appropriately. |

| 11 | Long lines | Low | Some lines exceed 79 characters. | Split long statements. |

| 12 | File handling | Low | File is manually opened and closed. | Use a with statement. |

| 13 | Missing final newline | Low | File does not end with a newline. | Add a final newline. |



\## Conclusion



Pylint, Bandit, and Flake8 help identify code-quality problems, security risks, and style violations. The identified issues should be fixed and all three tools rerun to verify the improvements.


# Lab 5: Static Code Analysis — Reflection

**SRN:** PES1UG24AM415

**Project:** Course Enrollment System

### 1. What did the static-analysis tools identify?

Pylint identified code-quality problems, Bandit identified security risks, and Flake8 identified Python style issues.

### 2. Which issues were most serious?

The unsafe `eval()` function, shell command execution, weak MD5 hashing, insecure OTP generation, and hardcoded secrets were important security concerns.

### 3. How were the issues fixed?

I replaced `eval()` with validated discount calculations, changed MD5 to SHA-256, used Python's `secrets` module for OTP generation, removed shell execution, improved file handling, and corrected naming and formatting issues.

### 4. What did you learn?

I learned that static-analysis tools help find security vulnerabilities and code-quality problems before software is deployed. Running the tools before and after fixing the code helps verify improvements.
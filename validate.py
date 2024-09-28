import os
import sys
import re

class ValidationResult:
    def __init__(self, success: bool, message: str = "", file: str = "", line: int = 0):
        self.success = success
        self.message = message
        self.file = file
        self.line = line

class Validator:
    def validate(self) -> ValidationResult:
        raise NotImplementedError("Each validator must implement the validate method.")

class DisclaimerValidator(Validator):
    """
    Validator to ensure that the last build_pres file contains the word 'Disclaimer'.
    """

    def __init__(self, deploy_yaml_path: str):
        self.deploy_yaml_path = deploy_yaml_path
        self.name_pattern = re.compile(r"--name=([^\s]+)\s+build_pres")

    def validate(self) -> ValidationResult:
        if not os.path.exists(self.deploy_yaml_path):
            return ValidationResult(False, f"File not found: {self.deploy_yaml_path}")

        try:
            with open(self.deploy_yaml_path, 'r') as f:
                deploy_content = f.read()
        except Exception as e:
            return ValidationResult(False, f"Error reading {self.deploy_yaml_path}: {e}")

        # Find all --name=<name> build_pres patterns
        names = self.name_pattern.findall(deploy_content)
        if not names:
            return ValidationResult(False, "No '--name=<name> build_pres' patterns found in deploy.yml.")

        last_name = names[-1]
        target_file = os.path.join('.', f"{last_name}.md",)

        if not os.path.exists(target_file):
            return ValidationResult(False, f"File not found: {target_file}")

        try:
            with open(target_file, 'r') as f:
                file_content = f.read()
        except Exception as e:
            return ValidationResult(False, f"Error reading {target_file}: {e}")

        if "Disclaimer" in file_content:
            return ValidationResult(True)
        else:
            return ValidationResult(False, "Disclaimer Slide Missing")

def emit_error(message: str, file: str = "", line: int = 0):
    """
    Emits an error annotation in GitHub Actions.

    Args:
        message (str): The error message.
        file (str): The file in which the error occurred.
        line (int): The line number of the error.
    """
    if file and line:
        annotation = f"::error file={file},line={line}::{message}"
    elif file:
        annotation = f"::error file={file}::{message}"
    else:
        annotation = f"::error::{message}"
    print(annotation)

def main():
    deploy_yaml_path = os.path.join('.github', 'workflows', 'deploy.yml')
    validators = [
        DisclaimerValidator(deploy_yaml_path=deploy_yaml_path),
        # Add more validators here
    ]

    all_success = True
    messages = []

    for validator in validators:
        result = validator.validate()
        if not result.success:
            all_success = False
            if result.file or result.line:
                emit_error(result.message, file=result.file, line=result.line)
            else:
                emit_error(result.message)
            messages.append(result.message)

    if not all_success:
        print("\nValidation Failed:")
        for msg in messages:
            print(f"- {msg}")
        sys.exit(1)
    else:
        print("All validations passed.")

if __name__ == "__main__":
    main()

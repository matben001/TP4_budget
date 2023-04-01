import subprocess

# Function that runs the tests and returns the result
def run_tests():
    result = subprocess.run(['python', 'manage.py'], capture_output=True, text=True)
    return result.returncode

# Function that checks out a commit and runs the tests
def check_commit(commit):
    subprocess.run(['git', 'checkout', commit], capture_output=True)
    return run_tests()

# Start git bisect and specify the good and bad commits
subprocess.run(['git', 'bisect', 'start'])
subprocess.run(['git', 'bisect', 'good', 'HEAD~10'])  # Specify a commit that is known to pass the tests
subprocess.run(['git', 'bisect', 'bad', 'HEAD'])  # Specify the current commit that is known to not pass the tests

# Run the bisect
while True:
    result = run_tests()
    if result == 0:
        # Tests passed, mark the commit as good
        subprocess.run(['git', 'bisect', 'good'])
    else:
        # Tests failed, mark the commit as bad
        subprocess.run(['git', 'bisect', 'bad'])

    # If there is only one commit left, print it and exit
    if subprocess.run(['git', 'bisect', 'visualize'], capture_output=True, text=True).stdout.strip() == '':
        result = subprocess.run(['git', 'rev-list', '--max-parents=0', 'HEAD'], capture_output=True, text=True).stdout.strip()
        print(f'The first bad commit is: {result}')
        break
import argparse
import importlib.util
import os

# We create an ArgumentParser object to define the command line arguments.
parser = argparse.ArgumentParser(description='Labsecurity is a tool that bundles ethical hacking python scripts into a single tool with cli interface.')
parser.add_argument('-t', '--target', help='Objective to use', required=False)
parser.add_argument('-p', '--port', help='Port to user', required=False)
parser.add_argument('script_name', help='Script name to be executed')

# We parse the command line arguments.
args = parser.parse_args()

# We verify that the script file exists.
script_path = os.path.join('scripts', args.script_name)
if not os.path.isfile(script_path):
    raise ValueError(f'The file {script_path} does not exist')

# We import the script module.
spec = importlib.util.spec_from_file_location('script_module', script_path)
script_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script_module)

# We run the script with the command line arguments.
if args.target and args.port:
    script_module.run(args.target, args.port)
elif args.target:
    script_module.run(args.target)
elif args.script_name:
    script_module.run()
else:
    print("An error occurred, missing arguments")

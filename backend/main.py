"""
Main script file to run backend and database
"""

import argparse

def _run_tests():
    """ Run tests """
    print("--test: running tests")
    
    import unittest
    import tests.test_parser
    import tests.test_tree_traversal
    
    loader = unittest.TestLoader()
    suite_parser = loader.loadTestsFromModule(tests.test_server)
    suite_tree = loader.loadTestsFromModule(tests.test_tree_traversal)
    
    runner = unittest.TextTestRunner()
    runner.run(suite_parser)
    runner.run(suite_tree)

def _run_dev_api_server(host, port):
    """ Run a dev instance of the FastAPI server """
    if not host:
        host = "0.0.0.0"
    
    if not port:
        port = 5000
    
    import uvicorn
    
    uvicorn.run('rules_engine.main:app', host=host, port=port, reload=True)


def _run_db_migrate():
    """ Instantiate Postgres DB with schema, and empty tables """
    print("--migrate: running DB Migrate")

def _run_start_db():
    """ Start the DB instance on local machine """
    print("--db: starting DB")

def _show_help():
    """ Show Help Information """
    help_string = """usage: main.py [-h] [--tests] [--dev] [--host HOST] [--port PORT]

    options:
    -h, --help         show this help message and exit
    --tests            Run tests for Parser and AST
    --dev              Run dev FastAPI Server
    --host HOST        Add host address to run the FastAPI Server
    --port PORT        Add port address to run the FastAPI Server
    """

    print(help_string)

def main():
    """
    Entry into the app, execute commands according to the arguments supplied.
    """
    parser = argparse.ArgumentParser(allow_abbrev=False)

    # Add arguments to be processed by the python cmd
    parser.add_argument('--tests', action='store_true', help='Run tests for Parser and AST')
    parser.add_argument('--dev', action='store_true', help='Run dev FastAPI Server')
    parser.add_argument('--host', dest='host', type=str, help='Add host address to run the FastAPI Server')
    parser.add_argument('--port', dest='port', type=int, help='Add port address to run the FastAPI Server')

    args = parser.parse_args()

    if args.tests:
        _run_tests()
    elif args.dev:
        _run_dev_api_server(args.host, args.port)
    else:
        _show_help()
        

if __name__ == "__main__":
    main()
"""Entry point for the car assembly CLI.

Business logic lives in the car_assembly package (catalog, rules,
builder, wizard, cli); this file only wires the terminal script to it.
"""

from car_assembly.cli import main

if __name__ == "__main__":
    main()

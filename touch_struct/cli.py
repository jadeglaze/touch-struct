"""Command-line interface for touch-struct."""

import sys
import click
from .core import create_structure

@click.command()
@click.argument('input', type=click.Path(exists=True, dir_okay=False, allow_dash=True))
@click.option('--output-dir', '-o', default=".",
              help="Directory where the structure should be created",
              type=click.Path(file_okay=False))
def main(input, output_dir):
    """Create directory structure from an input file or stdin (use - for stdin)."""
    try:
        if input == '-':
            content = sys.stdin.read()
            create_structure.from_string(content, output_dir)
        else:
            create_structure.from_file(input, output_dir)
        click.echo(f"Successfully created directory structure in {output_dir}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1) 
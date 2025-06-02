import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command():
    """Create tables from models or run schema.sql."""
    
    with current_app.app_context():
        db.drop_all()
        db.create_all()
        click.echo("PostgreSQL tables created successfully!")
import click


@click.group()
def brands():
    pass


@brands.command()
def list():
    click.echo('brands: list')


@brands.command()
@click.argument('id',
                type=int)
def show(id):
    click.echo('brands: show %d' % id)

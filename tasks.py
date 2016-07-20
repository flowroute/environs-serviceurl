from __future__ import print_function
import os
import sys

from invoke import task


@task
def ve(ctx, force=False):
    if os.path.exists('./ve') and not force:
        return
    ctx.run('virtualenv ve')
    ctx.run('./ve/bin/pip install -r requirements.txt')


@task(pre=[ve])
def test(ctx, pdb=False, std=False, kexpr=None, xit_fail=False):
    args = ''
    pty = False
    if pdb:
        args += ' --pdb'
        pty = True
    if std:
        args += ' -s'
    if kexpr:
        args += ' -k ' + kexpr
    if xit_fail:
        args += ' -x'
    ctx.run("./ve/bin/py.test --flake8 {args}".format(args=args), pty=pty)


@task(pre=[ve])
def coverage(ctx, debug=False):
    ctx.run(("./ve/bin/py.test --flake8 --cov-report html "
             "--cov=environs_serviceurl"))


@task(post=[test])
def version(ctx, level=None):
    if level not in ('patch', 'minor', 'major'):
        print('level (-l) must be one of patch, minor, or major')
        sys.exit(1)
    ctx.run("bumpversion {level}".format(level=level))

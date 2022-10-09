from invoke import task


@task
def build(c, src="./blog"):
    c.run(f"jupyter-book build {src}")

@task
def docs_folder(c):
    c.run('mkdir -p ./docs')

@task
def clean(c, src="./blog"):
    c.run(f"jupyter-book clean {src}")

@task(pre=[build, docs_folder], post=[clean])
def release(c):
    c.run('rm -r ./docs/*')
    c.run('mv ./blog/_build/html/* ./docs')
    c.run('touch ./docs/.nojekyll')

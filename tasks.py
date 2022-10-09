from invoke import task


@task
def build(c, src="./blog"):
    c.run(f"jupyter-book build {src}")


@task
def clean(c, src="./blog"):
    c.run(f"jupyter-book clean {src}")

@task(pre=[build], post=[clean])
def release(c):
    c.run('ghp-import -n -p -f ./blog/_build/html')
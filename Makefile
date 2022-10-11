blog := blog
docs := docs

.PHONY: build

release: build
	rm -r $(docs)/*
	mv $(blog)/_build/html/* $(docs)
	touch ${docs}/nojekyll
	$(MAKE) clean

build: 
	poetry run jupyter-book build $(blog)

clean:
	poetry run jupyter-book clean $(blog)

docs/:
	mkdir -p $@


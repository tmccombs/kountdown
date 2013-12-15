
SRCDIR = src
METADATA = $(SRCDIR)/metadata.desktop

CODEDIR = $(SRCDIR)/contents/code
PYSRCS = $(CODEDIR)/main.py $(CODEDIR)/model.py $(CODEDIR)/configUI.py

.PHONY: package
package: kountdown.zip

kountdown.zip: $(PYSRCS)
	cd $(SRCDIR) && zip -r --filesync  --exclude \*.swp ../kountdown.zip .

.PHONY: clean
clean:
	rm kountdown.zip


.PHONY: install
install: package
	plasmapkg -i kountdown.zip




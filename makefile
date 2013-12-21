
SRCDIR = src
METADATA = $(SRCDIR)/metadata.desktop

CONTENTDIR=$(SRCDIR)/contents
CODEDIR = $(SRCDIR)/contents/code
SRCS = $(CODEDIR)/main.py $(CODEDIR)/model.py $(CONTENTDIR)/config/main.xml $(CONTENTDIR)/ui/config.ui
ZIP_SRCS = $(subst $(SRCDIR)/,,$(SRCS)) metadata.desktop


.PHONY: package
package: kountdown.zip

kountdown.zip: $(SRCS) $(METADATA)
	cd $(SRCDIR) && zip -r --filesync ../kountdown.zip $(ZIP_SRCS)

.PHONY: clean
clean:
	rm kountdown.zip


.PHONY: install
install: package
	plasmapkg -i kountdown.zip

.PHONY: uninstall
	plasmapkg -r kountdown



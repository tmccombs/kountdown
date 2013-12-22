
SRCDIR = src
METADATA = $(SRCDIR)/metadata.desktop

CONTENTDIR=$(SRCDIR)/contents
CODEDIR = $(SRCDIR)/contents/code
SRCS = $(CODEDIR)/main.py $(CODEDIR)/model.py $(CONTENTDIR)/config/main.xml $(CONTENTDIR)/ui/config.ui
ZIP_SRCS = $(subst $(SRCDIR)/,,$(SRCS)) metadata.desktop


.PHONY: package
package: kountdown.plasmoid

kountdown.plasmoid: $(SRCS) $(METADATA)
	cd $(SRCDIR) && zip -r --filesync ../kountdown.plasmoid $(ZIP_SRCS)

.PHONY: clean
clean:
	rm kountdown.plasmoid


.PHONY: install
install: package
	plasmapkg -i kountdown.plasmoid

.PHONY: uninstall
	plasmapkg -r kountdown



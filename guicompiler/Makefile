

# NOTE: these have to be the same, as the UI files may import the RC files
RCDIR = qtauto
UIDIR = qtauto


TARGETS = $(RCDIR)/guicompiler_rc.py \
	 $(UIDIR)/ui_mainwidget.py \
	 $(UIDIR)/ui_compilerwidget.py


all: $(TARGETS)

clean:
	@rm $(TARGETS)

$(RCDIR)/%_rc.py: %.qrc
	pyrcc4 -o $@ $<

$(UIDIR)/ui_%.py: %.ui
	pyuic4 -o $@ $<

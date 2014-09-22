

RCDIR = rc
UIDIR = ui


TARGETS = $(RCDIR)/guicompiler_rc.py \
	 $(UIDIR)/ui_mainwidget.py \
	 $(UIDIR)/ui_compilewidget.py


all: $(TARGETS)

clean:
	@rm $(TARGETS)

$(RCDIR)/%_rc.py: %.qrc
	pyrcc4 -o $@ $<

$(UIDIR)/ui_%.py: %.ui
	pyuic4 -o $@ $<

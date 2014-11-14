#
# Makefile for demos
#


pdflatexex=../bin/pdflatexex
pdflatextips=../bin/pdflatextips
pdflatexsol=../bin/pdflatexsol


demos = \
	custom_labels_ex.pdf \
	custom_labels_tips.pdf \
	custom_labels_sol.pdf \
	exenumrefs_sol.pdf \
	figures_ex.pdf \
	figures_sol.pdf \
	headersubline_ex.pdf \
	style_ethunizh_ex.pdf \
	style_ethunizh_sol.pdf \
	style_ethunizh_tips.pdf \
	style_largesolutions_ex.pdf \
	style_largesolutions_sol.pdf \
	style_largetips_ex.pdf \
	style_largetips_sol.pdf \
	style_largetips_tips.pdf \
	style_previousitp_ex.pdf \
	style_previousitp_sol.pdf \
	style_previousitp_tips.pdf \
	test_badstructure_ex.pdf \
	test_badstructure_sol.pdf \
	test_badstructure_tips.pdf \
	test_deutsch_ex.pdf \
	test_deutsch_sol.pdf \
	test_exstarred_ex.pdf \
	test_features_ex.pdf \
	test_features_tips.pdf \
	test_features_sol.pdf \
	test_tips_ex.pdf \
	test_tips_sol.pdf \
	test_tips_tips.pdf


all: $(demos)

clean:
	rm -f $(demos)

%_tips.pdf: %.tex  ethuebung.sty
	$(pdflatextips) $<

%_sol.pdf: %.tex  ethuebung.sty
	$(pdflatexsol) $<

%_ex.pdf: %.tex  ethuebung.sty
	$(pdflatexex) $<

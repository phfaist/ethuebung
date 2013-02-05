
pdflatexex=../pdflatexex
pdflatextips=../pdflatextips
pdflatexsol=../pdflatexsol


demos = exenumrefs_sol.pdf \
	style_largesolutions_ex.pdf \
	style_largesolutions_sol.pdf \
	style_largetips_ex.pdf \
	style_largetips_sol.pdf \
	style_largetips_tips.pdf \
	style_previousitp_ex.pdf \
	style_previousitp_sol.pdf \
	style_previousitp_tips.pdf \
	test_deutsch_ex.pdf \
	test_deutsch_sol.pdf \
	test_features_ex.pdf \
	test_features_sol.pdf \
	test_tips_ex.pdf \
	test_tips_sol.pdf \
	test_tips_tips.pdf


all: $(demos)

clean:
	rm -f $(demos)

%_tips.pdf: %.tex
	$(pdflatextips) $<

%_sol.pdf: %.tex
	$(pdflatexsol) $<

%_ex.pdf: %.tex
	$(pdflatexex) $<


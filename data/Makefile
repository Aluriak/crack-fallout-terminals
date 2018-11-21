TESSDIR=/usr/share/tesseract/tessdata/
# TESSDIR=/usr/share/tessdata/


# combine all to build the Fixedsys.traineddata
Fixedsys.traineddata: clear train-from-box-files unicharset mftraining
	combine_tessdata Fixedsys.
	sudo cp Fixedsys.traineddata $(TESSDIR)


# once the generated box files have been corrected by hand, tell tesseract to learn from it.
train-from-box-files:
	tesseract eng.Fixedsys.exp0.png eng.Fixedsys.exp0.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp1.png eng.Fixedsys.exp1.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp2.png eng.Fixedsys.exp2.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp3.png eng.Fixedsys.exp3.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp4.png eng.Fixedsys.exp4.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp5.png eng.Fixedsys.exp5.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp6.png eng.Fixedsys.exp6.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp7.png eng.Fixedsys.exp7.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp8.png eng.Fixedsys.exp8.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp9.png eng.Fixedsys.exp9.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp10.png eng.Fixedsys.exp10.box nobatch box.train .stderr
	tesseract eng.Fixedsys.exp11.png eng.Fixedsys.exp11.box nobatch box.train .stderr
unicharset:
	unicharset_extractor *.box
mftraining:
	mftraining -F font_properties -U unicharset -O Fixedsys.unicharset *.tr
	cntraining *.tr
	# rename to get all related to Fixedsys
	mv normproto Fixedsys.normproto
	mv inttemp Fixedsys.inttemp
	mv shapetable Fixedsys.shapetable
	mv pffmtable Fixedsys.pffmtable


# use the current tesseract configuration to detect the letters.
# Since there is handwork after that step, be sure to not run this without saving the said handwork.
make-box-files:
	# tesseract eng.Fixedsys.exp0.png eng.Fixedsys.exp0 batch.nochop makebox
	# tesseract eng.Fixedsys.exp1.png eng.Fixedsys.exp1 batch.nochop makebox
	# tesseract eng.Fixedsys.exp2.png eng.Fixedsys.exp2 batch.nochop makebox
	# tesseract eng.Fixedsys.exp3.png eng.Fixedsys.exp3 batch.nochop makebox
	# tesseract eng.Fixedsys.exp4.png eng.Fixedsys.exp4 batch.nochop makebox
	# tesseract eng.Fixedsys.exp5.png eng.Fixedsys.exp5 batch.nochop makebox
	# tesseract eng.Fixedsys.exp6.png eng.Fixedsys.exp6 batch.nochop makebox
	# tesseract eng.Fixedsys.exp7.png eng.Fixedsys.exp7 batch.nochop makebox
	# tesseract eng.Fixedsys.exp8.png eng.Fixedsys.exp8 batch.nochop makebox
	# tesseract eng.Fixedsys.exp9.png eng.Fixedsys.exp9 batch.nochop makebox
	# tesseract eng.Fixedsys.exp10.png eng.Fixedsys.exp10 batch.nochop makebox
	# tesseract eng.Fixedsys.exp11.png eng.Fixedsys.exp11 batch.nochop makebox


use-basic-font-handling:
	sudo cp Fixedsys.traineddata.by-font $(TESSDIR)Fixedsys.traineddata


clear:
	- rm *.tr Fixedsys.traineddata inttemp normproto pffmtable shapetable unicharset Fixedsys.inttemp Fixedsys.normproto Fixedsys.pffmtable Fixedsys.shapetable Fixedsys.unicharset

.PHONY: clear

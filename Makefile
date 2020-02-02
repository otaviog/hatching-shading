about:
	@echo "Project tasks"

happy_recon.tar.gz:
	wget http://graphics.stanford.edu/pub/3Dscanrep/happy/happy_recon.tar.gz

happy_recon: happy_recon.tar.gz
	tar xzvf $^
	touch $@

demo-budha-lowres: happy_recon
	python demo.py $^/happy_vrip_res4.ply

demo-budha-highres: happy_recon
	python demo.py $^/happy_vrip.ply

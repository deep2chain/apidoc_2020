version=v1.0.0
daemon=hsd_${version}_linux_amd64.tar.gz
client=hscli_${version}_linux_amd64.tar.gz
client_debug=hscli_${version}_DEBUG_MODE_linux_amd64.tar.gz

update.hsd:
	@cp $$(which hsd) .
	@if [ -f "${daemon}" ]; then rm ${daemon}; fi
	@tar zcvf ${daemon} hsd
	@rm hsd

update.hscli:
	@cp $$(which hscli) .
	@if [ -f "${client}" ]; then rm ${client}; fi
	@tar zcvf ${client} hscli
	@rm hscli

update.hscli.debug:
	@cp $$(which hscli) .
	@if [ -f "${client_debug}" ]; then rm ${client_debug}; fi
	@tar zcvf ${client_debug} hscli
	@rm hscli

RELEASE := $(shell cat $(HOME)/.my-docker-images.release)

define make_image
	echo   "##########################################################"
	printf "###########  Making image %-15s  ###############\n" "${1}"
	echo ""
	
	docker build --build-arg RELEASE=$(RELEASE) -t ${1}:$(RELEASE) .

	echo ""
	printf "##########  Done with image %-15s  #############\n" "${1}"
	echo "##########################################################"
	echo ""
endef

dbt-env: 
	$(call make_image, ronkitay/image-tools-env)


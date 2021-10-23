SOURCE=main.go
OUTFILE=goreverseme

all:
	$(eval IMAGE_HASH = $(shell docker build --build-arg SOURCE=$(SOURCE) --build-arg OUTFILE=$(OUTFILE) -q .))
	$(eval CONTAINER_HASH = $(shell docker run -d -it --rm $(IMAGE_HASH) /bin/bash))
	docker cp $(CONTAINER_HASH):/build/$(OUTFILE) ..
	docker container stop $(CONTAINER_HASH)
	docker rmi $(IMAGE_HASH)
# 사용법
#   make video URL='<m3u8 URL>' [NAME=이름]     # data/<번호>_<이름>/lecture.mp4, lecture.srt
# URL은 & 가 있으므로 반드시 작은따옴표로 감쌉니다.

PYTHON ?= python3
MODEL_DIR ?= $(HOME)/.cache/whisper-cpp
MODEL ?= $(MODEL_DIR)/ggml-large-v3-turbo-q5_0.bin
LANG_CODE ?= ko
OUT ?= data

.PHONY: help video

help:
	@echo "make video URL='<m3u8 URL>' [NAME=이름]  영상·자막을 $(OUT)/<번호>_<이름>/ 에 저장"

video:
	@if [ -z "$(URL)" ]; then echo "사용법: make video URL='<m3u8 URL>' [NAME=이름]"; exit 1; fi
	@$(PYTHON) tools/nullnull_download.py '$(URL)' --model "$(MODEL)" --lang "$(LANG_CODE)" \
		--out "$(OUT)" $(if $(NAME),--name '$(NAME)')

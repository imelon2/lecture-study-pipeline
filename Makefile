# 사용법
#   make setup                                  # ffmpeg, whisper-cpp, 전사 모델 설치
#   make video URL='<m3u8 URL>' [NAME=이름]     # data/<번호>_<이름>/lecture.mp4, lecture.srt
# URL은 & 가 있으므로 반드시 작은따옴표로 감쌉니다.

PYTHON ?= python3
MODEL_DIR ?= $(HOME)/.cache/whisper-cpp
MODEL ?= $(MODEL_DIR)/ggml-large-v3-turbo-q5_0.bin
MODEL_URL ?= https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
LANG_CODE ?= ko
OUT ?= data

.PHONY: help setup video

help:
	@echo "make setup                               ffmpeg, whisper-cpp, 전사 모델 설치"
	@echo "make video URL='<m3u8 URL>' [NAME=이름]  영상·자막을 $(OUT)/<번호>_<이름>/ 에 저장"

setup:
	@if command -v brew >/dev/null 2>&1; then \
		brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg; \
		brew list whisper-cpp >/dev/null 2>&1 || brew install whisper-cpp; \
	else \
		for t in ffmpeg whisper-cli; do command -v $$t >/dev/null 2>&1 || \
			echo "$$t 를 직접 설치해 주세요 (Homebrew가 없습니다)."; done; \
	fi
	@mkdir -p "$(MODEL_DIR)"
	@if [ -f "$(MODEL)" ]; then echo "모델 있음: $(MODEL)"; else \
		echo "모델 내려받는 중 (약 574MB)"; \
		curl -L -f --progress-bar -o "$(MODEL).part" "$(MODEL_URL)" && mv "$(MODEL).part" "$(MODEL)"; \
	fi

video:
	@if [ -z "$(URL)" ]; then echo "사용법: make video URL='<m3u8 URL>' [NAME=이름]"; exit 1; fi
	@$(PYTHON) tools/nullnull_download.py '$(URL)' --model "$(MODEL)" --lang "$(LANG_CODE)" \
		--out "$(OUT)" $(if $(NAME),--name '$(NAME)')

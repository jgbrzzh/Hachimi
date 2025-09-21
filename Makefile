# 哈吉咪加密解密器 Makefile

# 默认目标
.DEFAULT_GOAL := build

# 变量定义
PYTHON := python
PIP := pip
CMAKE := cmake
BUILD_DIR := build
DIST_DIR := dist

# 帮助信息
.PHONY: help
help:
	@echo "哈吉咪加密解密器构建工具"
	@echo ""
	@echo "可用命令:"
	@echo "  build        - 构建项目（编译C++扩展）"
	@echo "  install      - 安装项目到当前Python环境"
	@echo "  develop      - 以开发模式安装项目"
	@echo "  test         - 运行测试"
	@echo "  clean        - 清理构建文件"
	@echo "  format       - 格式化代码"
	@echo "  lint         - 代码检查"
	@echo "  docs         - 生成文档"
	@echo "  package      - 创建分发包"
	@echo "  setup-dev    - 设置开发环境"
	@echo ""

# 设置开发环境
.PHONY: setup-dev
setup-dev:
	@echo "设置开发环境..."
	$(PIP) install -r requirements-dev.txt

# 构建项目
.PHONY: build
build:
	@echo "构建项目..."
	$(PYTHON) setup.py build_ext --inplace

# 安装项目
.PHONY: install
install: build
	@echo "安装项目..."
	$(PIP) install .

# 开发模式安装
.PHONY: develop
develop:
	@echo "以开发模式安装项目..."
	$(PIP) install -e .

# 运行测试
.PHONY: test
test:
	@echo "运行测试..."
	$(PYTHON) -m pytest tests/ -v

# 清理构建文件
.PHONY: clean
clean:
	@echo "清理构建文件..."
	$(RM) -rf $(BUILD_DIR)
	$(RM) -rf $(DIST_DIR)
	$(RM) -rf *.egg-info
	$(RM) -rf src/python/hachimi/*.so
	$(RM) -rf src/python/hachimi/*.pyd
	$(RM) -rf src/python/hachimi/__pycache__
	$(RM) -rf tests/__pycache__
	$(RM) -rf examples/__pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec $(RM) -rf {} +

# 代码格式化
.PHONY: format
format:
	@echo "格式化Python代码..."
	black src/python/ tests/ examples/ setup.py
	isort src/python/ tests/ examples/ setup.py

# 代码检查
.PHONY: lint
lint:
	@echo "检查Python代码..."
	flake8 src/python/ tests/ examples/ setup.py
	mypy src/python/

# 生成文档
.PHONY: docs
docs:
	@echo "生成文档..."
	@echo "文档生成功能待实现..."

# 创建分发包
.PHONY: package
package: clean
	@echo "创建分发包..."
	$(PYTHON) setup.py sdist bdist_wheel

# Windows专用命令
ifeq ($(OS),Windows_NT)
    RM := del /Q /S
    CMAKE_GENERATOR := "Visual Studio 16 2019"
else
    RM := rm -f
    CMAKE_GENERATOR := "Unix Makefiles"
endif

# CMake构建（可选）
.PHONY: cmake-build
cmake-build:
	@echo "使用CMake构建..."
	mkdir -p $(BUILD_DIR)
	cd $(BUILD_DIR) && $(CMAKE) -G $(CMAKE_GENERATOR) ../src/cpp
	cd $(BUILD_DIR) && $(CMAKE) --build . --config Release

# 快速测试
.PHONY: quick-test
quick-test: build
	@echo "快速测试..."
	$(PYTHON) -c "import hachimi; print('✓ 导入成功'); crypto = hachimi.HachimiCrypto(); print('✓ 创建实例成功'); print(crypto.test_connection())"

# 性能测试
.PHONY: benchmark
benchmark:
	@echo "运行性能测试..."
	$(PYTHON) -m pytest tests/benchmark.py -v

# 全面检查
.PHONY: check-all
check-all: format lint test
	@echo "全面检查完成！"
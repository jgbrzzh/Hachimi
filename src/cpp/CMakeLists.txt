cmake_minimum_required(VERSION 3.12)
project(hachimi_crypto)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置构建类型
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# 编译器特定设置
if(MSVC)
    # Visual Studio 编译器
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4 /EHsc")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /O2 /DNDEBUG")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Od /D_DEBUG")
else()
    # GCC 或 Clang
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG -march=native")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0 -g -D_DEBUG")
endif()

# 查找pybind11
find_package(pybind11 REQUIRED)

# 设置源文件目录
set(CPP_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/cpp")
set(CPP_INCLUDE_DIR "${CPP_SRC_DIR}/include")
set(CPP_SOURCE_DIR "${CPP_SRC_DIR}/src")

# 包含头文件目录
include_directories(${CPP_INCLUDE_DIR})

# 核心库源文件
set(CORE_SOURCES
    ${CPP_SOURCE_DIR}/hachimi_core.cpp
)

# 创建核心静态库
add_library(hachimi_core_lib STATIC ${CORE_SOURCES})
target_include_directories(hachimi_core_lib PUBLIC ${CPP_INCLUDE_DIR})

# Python绑定模块
pybind11_add_module(hachimi_core
    ${CPP_SOURCE_DIR}/python_binding.cpp
)

# 链接核心库
target_link_libraries(hachimi_core PRIVATE hachimi_core_lib)

# 设置Python模块属性
target_compile_definitions(hachimi_core PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

# 安装规则
install(TARGETS hachimi_core DESTINATION .)

# 可选：创建可执行文件进行测试
option(BUILD_TESTS "Build test executable" OFF)
if(BUILD_TESTS)
    add_executable(hachimi_test
        ${CPP_SOURCE_DIR}/test_main.cpp
    )
    target_link_libraries(hachimi_test hachimi_core_lib)
endif()

# 可选：生成文档
option(BUILD_DOCS "Build documentation" OFF)
if(BUILD_DOCS)
    find_package(Doxygen)
    if(DOXYGEN_FOUND)
        set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/docs/Doxyfile.in)
        set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
        configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
        add_custom_target(docs ALL
            COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Generating API documentation with Doxygen"
            VERBATIM
        )
    endif()
endif()
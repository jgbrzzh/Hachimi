#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "hachimi_core.h"

namespace py = pybind11;

PYBIND11_MODULE(hachimi_core, m) {
    m.doc() = "Hachimi Core - High performance encryption/decryption module";
    
    py::class_<hachimi::HachimiCore>(m, "HachimiCore")
        .def(py::init<>(), "Create a new HachimiCore instance")
        .def("encrypt", &hachimi::HachimiCore::encrypt,
             "Encrypt a string with the given key",
             py::arg("plaintext"), py::arg("key"))
        .def("decrypt", &hachimi::HachimiCore::decrypt,
             "Decrypt encrypted bytes with the given key",
             py::arg("ciphertext"), py::arg("key"))
        .def("encrypt_file", &hachimi::HachimiCore::encrypt_file,
             "Encrypt a file and save to output path",
             py::arg("input_path"), py::arg("output_path"), py::arg("key"))
        .def("decrypt_file", &hachimi::HachimiCore::decrypt_file,
             "Decrypt a file and save to output path",
             py::arg("input_path"), py::arg("output_path"), py::arg("key"));
    
    // 添加一些辅助函数
    m.def("version", []() {
        return "1.0.0";
    }, "Get the version of Hachimi Core");
    
    m.def("test_connection", []() {
        return "C++ module is working correctly!";
    }, "Test if the C++ module is properly loaded");
}
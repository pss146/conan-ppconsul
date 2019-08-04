from conans import ConanFile, CMake, tools


class ppConsulConan(ConanFile):
    name = "ppconsul"
    version = "0.1"
    license = "<Put the package license here>"
    author = "Perepelitsyn Stanislav <stas.perepel@gmail.com>"
    url = "https://github.com/pss146/conan-ppconsul"
    description = "C++ client for Consul"
    topics = ("consul", "ppconsul")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "ppconsul.patch"]

    _build_subfolder = "build"
    _source_subfolder = "ppconsul"

    def configure(self):
        # We can control the options of our dependencies based on current options
        # self.options["libcurl"].shared = self.options.shared
        self.options["libcurl"].shared = True

    def requirements(self):
        self.requires.add('boost/1.70.0@conan/stable')
        self.requires.add('libcurl/7.64.1@bincrafters/stable')

    def source(self):
        self.run("git clone https://github.com/oliora/ppconsul.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
#         tools.replace_in_file("ppconsul/CMakeLists.txt", "project(Ppconsul VERSION 0.1)",
#                               '''project(Ppconsul VERSION 0.1)
# include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
# conan_basic_setup()
# SET(BOOST_ROOT "${CONAN_BOOST_ROOT}")
# SET(CURL_ROOT "${CONAN_CURL_ROOT}")
# SET(Boost_NO_BOOST_CMAKE ON)
# SET(Boost_NO_SYSTEM_PATHS ON)
# ''')

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.options.shared == "False":
            cmake.definitions['BUILD_STATIC_LIB'] = 'ON'

        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file='ppconsul.patch')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        # self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libs = ['ppconsul', 'json11']


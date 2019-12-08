from conans import ConanFile, CMake, tools
import os


class LabSoundConan(ConanFile):
    name = "LabSound"
    version = "0.13.0"
    description = "modern C++ graph-based audio engine "
    topics = ("conan", "LabSound", "audio")
    url = "https://github.com/cdbishop/conan-labsound"
    homepage = "http://labsound.io/"
    license = "BSD-2-Clause" 
    # Remove following lines if the target lib does not use CMake
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {}
    default_options = {}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        pass

    def source(self):        
        url = 'https://github.com/LabSound/LabSound'
        git = tools.Git(folder=self.name)
        git.clone(url, branch='v%s' % self.version)
        git.run("submodule update --init")

    def _configure_cmake(self):
        cmake = CMake(self)        
        cmake.configure(source_folder=self.name)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        bin_folder = os.path.join(self.build_folder, "bin")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False, src=bin_folder)
        self.copy(pattern="*.lib", dst="lib", keep_path=False, src=bin_folder, exclude="*example.lib")
        self.copy(pattern="*.a", dst="lib", keep_path=False, src=bin_folder)
        self.copy(pattern="*.so*", dst="lib", keep_path=False, src=bin_folder)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False, src=bin_folder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
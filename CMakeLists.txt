project(covid LANGUAGES NONE)
cmake_minimum_required(VERSION 3.13)

set(PYFILES main.py pdfconvert.py request.py textparser.py)

include(ExternalProject)
ExternalProject_Add(poppler
    URL https://poppler.freedesktop.org/poppler-0.86.1.tar.xz
    URL_HASH SHA1=85e6bd5d96e667ea370dad4aabd2295210a706bb
    CMAKE_ARGS
        -DBUILD_CPP_TESTS=NO
        -DBUILD_GTK_TESTS=NO
        -DBUILD_QT5_TESTS=NO
        -DENABLE_GLIB=NO
        -DENABLE_QT5=NO
        -DFONT_CONFIGURATION=generic
        -DENABLE_LIBOPENJPEG=none
        -DENABLE_CMS=none
        -DENABLE_SPLASH=NO
        -DWITH_TIFF=NO
        -DWITH_PNG=NO
        -DBUILD_SHARED_LIBS=NO
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
)
ExternalProject_Get_Property(poppler INSTALL_DIR)
set(POPPLER_DIR ${INSTALL_DIR})

file(MAKE_DIRECTORY destdir)

add_custom_command(
    OUTPUT destdir/pdftotext
    DEPENDS poppler
    COMMAND cmake -E copy ${POPPLER_DIR}/bin/pdftotext destdir/pdftotext
    COMMENT "Copying pdftotext"
)

foreach(f ${PYFILES})
    add_custom_command(
        OUTPUT destdir/${f}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${f}
        COMMAND cmake -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${f} destdir/${f}
        COMMENT "Copying ${f}"
    )
    set(destdir_pyfiles ${destdir_pyfiles} destdir/${f})
endforeach()

add_custom_command(
    OUTPUT pip-stamp
    COMMAND pip3 install --target destdir attrs requests beautifulsoup4
    COMMAND cmake -E touch pip-stamp
)
add_custom_target(pip DEPENDS pip-stamp)

add_custom_command(
    OUTPUT destdir/pdftotext
    DEPENDS poppler
    COMMAND cmake -E copy ${POPPLER_DIR}/bin/pdftotext destdir/pdftotext
    COMMENT "Copying pdftotext"
)

add_custom_command(OUTPUT function.zip
    DEPENDS ${destdir_pyfiles} destdir/pdftotext pip
    WORKING_DIRECTORY destdir
    COMMAND cmake -E remove ${CMAKE_BINARY_DIR}/function.zip
    COMMAND zip -r ${CMAKE_BINARY_DIR}/function.zip .
)
add_custom_target(zip ALL DEPENDS function.zip)

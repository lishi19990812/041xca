file(WRITE "${CMAKE_BINARY_DIR}/embedded_files.h" "/* 空文件占位 */\n")

set(S "${PROJECT_SOURCE_DIR}/lang")
set(D "${PROJECT_BINARY_DIR}")

# English (en) must be first for Info.plist
list(APPEND XCA_LANGUAGES en bg de es fa fr hr id it ja ko nl pl pt_BR ru sk tr zh_CN)
list(JOIN XCA_LANGUAGES "</string>\n		<string>" LANGUAGES_PLIST)

foreach(lang ${XCA_LANGUAGES})
  guid(${lang})
  list(APPEND TS_FILES ${S}/xca_${lang}.ts)
  list(APPEND LANG_COMPREFS "  <ComponentRef Id=\"Ci18n.${lang}\"/>\n")
  set(LANG_COMPS "  <Component Id=\"Ci18n.${lang}\" Guid=\"${GUID}\">
    <File Id=\"xca_${lang}.qm\" Source=\"${D}/xca_${lang}.qm\" KeyPath=\"yes\"/>\n")
  if(EXISTS ${_qt_bin_dir}/../translations/qtbase_${lang}.qm)
    list(APPEND QT_QM_FILES ${_qt_bin_dir}/../translations/qtbase_${lang}.qm)
    string(APPEND LANG_COMPS "    <File Id=\"qtbase_${lang}.qm\" Source=\"${_qt_bin_dir}/../translations/qtbase_${lang}.qm\"/>\n")
  endif()
  string(APPEND LANG_COMPS "  </Component>\n")
  list(APPEND LANG_ALLCOMPS ${LANG_COMPS})
endforeach()

string(APPEND WIX_LANG_CONTENT
  "<DirectoryRef Id=\"i18n\">\n" ${LANG_ALLCOMPS} "</DirectoryRef>\n"
  "<ComponentGroup Id=\"GroupI18n\">\n" ${LANG_COMPREFS} "</ComponentGroup>"
)

WixFile(${D}/language.wxs ${WIX_LANG_CONTENT})
if (${QT_VERSION} VERSION_LESS 6.0.0)
  if (${QT_VERSION} VERSION_LESS 5.12.0)
    qt5_add_translation(QM_FILES ${TS_FILES})
  else()
    qt5_add_translation(QM_FILES ${TS_FILES} OPTIONS -silent)
  endif()
  message(STATUS "Updating translations from source with 'lupdate' only supported with QT6")
  target_sources(${CMAKE_PROJECT_NAME} PRIVATE ${QM_FILES})
else()
  get_target_property(LIBSRC xcalib SOURCES)
  get_target_property(XCASRC xca SOURCES)
  
  # 关键修复：必须用 PROJECT_SOURCE_DIR 指定到 lang 目录，否则找不到文件
  file(GLOB TS_FILES_ABS ${PROJECT_SOURCE_DIR}/lang/*.ts)
  
  # 1. 只生成 .qm 文件
  qt_add_lrelease(xca TS_FILES ${TS_FILES_ABS}
                     QM_FILES_OUTPUT_VARIABLE QM_FILES_GENERATED
                     LRELEASE_OPTIONS -silent
  )

  # 2. 为每个 .qm 文件设置相对路径别名
  foreach(qm_file ${QM_FILES_GENERATED})
    get_filename_component(qm_name ${qm_file} NAME)
    set_source_files_properties(${qm_file} PROPERTIES
        QT_RESOURCE_ALIAS "${qm_name}"
    )
  endforeach()

  # 3. 用官方 API 打包进内存 ":/lang/"
  qt_add_resources(xca "embedded_lang"
      PREFIX "/lang"
      FILES ${QM_FILES_GENERATED}
  )

  # 4. 构造 QM_FILES 列表，供后续打包使用
  foreach(f ${TS_FILES_ABS})
    string(REGEX REPLACE "\\.ts$" ".qm" qm_file "${f}")
    list(APPEND QM_FILES ${qm_file})
  endforeach()
endif()

find_program(LCONVERT lconvert HINTS ${_qt_bin_dir})
if (LCONVERT)
  add_custom_command(
    OUTPUT "${D}/xca.pot"
    COMMAND ${LCONVERT} -if ts -of po -i "${S}/xca.ts" -o "${D}/xca.pot"
    COMMAND ${CMAKE_COMMAND} -E copy "${D}/xca.pot" "${S}/xca.pot"
    DEPENDS "${S}/xca.ts"
    COMMENT "Update POT file"
  )
endif()

# 编译 xca 后自动拷贝帮助文件
add_custom_command(TARGET xca POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/html
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_BINARY_DIR}/doc/html
        ${CMAKE_BINARY_DIR}/html
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_BINARY_DIR}/doc/qthelp/xca.qhc
        ${CMAKE_BINARY_DIR}/doc/qthelp/xca.qch
        ${CMAKE_BINARY_DIR}/html/
    COMMENT "Copying HTML and Qt Help files to build/html directory"
)


# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_naima_mapping_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED naima_mapping_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(naima_mapping_FOUND FALSE)
  elseif(NOT naima_mapping_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(naima_mapping_FOUND FALSE)
  endif()
  return()
endif()
set(_naima_mapping_CONFIG_INCLUDED TRUE)

# output package information
if(NOT naima_mapping_FIND_QUIETLY)
  message(STATUS "Found naima_mapping: 0.0.0 (${naima_mapping_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'naima_mapping' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${naima_mapping_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(naima_mapping_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${naima_mapping_DIR}/${_extra}")
endforeach()

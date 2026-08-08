#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/nokia/sdm660-common',
    'hardware/qcom-caf/wlan',
    'hardware/qcom-caf/msm8998',
    'vendor/nokia/sdm660-common',
]

blob_fixups: blob_fixups_user_type = {
    'vendor/lib/hw/camera.sdm660.so': blob_fixup()
        .add_needed('libui_shim.so')
        .sig_replace('c1 68 d0 e9 0d 20 cd e9 03 20', 'c1 68 d0 e9 12 20 cd e9 03 20')
        .sig_replace('49 6b c6 e9 04 21', '89 6c c6 e9 04 21'),
    ('vendor/lib/libmmcamera_faceproc.so', 'vendor/lib/libmmcamera_faceproc2.so'): blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
}  # fmt: skip

module = ExtractUtilsModule(
    'PL2',
    'nokia',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sdm660-common', module.vendor
    )
    utils.run()

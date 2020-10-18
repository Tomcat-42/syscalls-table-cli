#!/bin/bash

# Target dir for instalation and for json file
INSTALL_DIR="/usr/bin"
JSON_DIR="/usr/share/syscalls"

# Change for the dir which the src code is
SRC_DIR="/tmp/"

# Change for the target version
KERNEL_VERSION="4.14.201"
KERNEL_LINK="https://www.kernel.org/pub/linux/kernel/v4.x/linux-${KERNEL_VERSION}.tar.xz"

TBL_64="${SRC_DIR}linux-${KERNEL_VERSION}/arch/x86/entry/syscalls/syscall_64.tbl"
TBL_32="${SRC_DIR}linux-${KERNEL_VERSION}/arch/x86/entry/syscalls/syscall_32.tbl"

# Will download the source from kernel.org if not already present
if [ ! -d ${SRC_DIR}linux-${KERNEL_VERSION} ]; then
    curl -L $KERNEL_LINK >${SRC_DIR}linux-${KERNEL_VERSION}.tar.xz
    tar xf ${SRC_DIR}linux-${KERNEL_VERSION}.tar.xz -C $SRC_DIR
fi

# Test if tbl files exists
if [ ! -f ${TBL_64} ] || [ ! -f ${TBL_32} ]; then
    echo "File(s) syscall_64.tbl or syscall_32.tbl doesn't exist"
    exit 1
fi

# gen tables
# If default syscalls.json is present don't generate another one
if [ ! -f "syscalls.json" ]; then
    echo "[+] Generating tags, this may take a while..."
    ctags --fields=afmikKlnsStz --c-kinds=+pc -R /tmp/linux-${KERNEL_VERSION}
    echo "[+] Tags generated"
    echo "[+] Preparing the syscalls tables files..."

    cp -v $TBL_32 . >/dev/null
    cp -v $TBL_64 . >/dev/null

    sed -i '1,8d' syscall_32.tbl
    sed -i "s/__x64_//g" syscall_64.tbl
    sed -i "s/__x32_compat_//g" syscall_64.tbl
    echo "[+] Done :)"

    echo "[+] Generating syscalls json file..."
    ./gen_syscalls.py >syscalls.json

    read -r -e -p "Do you want to delete tags files[y/n]? " choice
    [[ "$choice" == [Yy]* ]] && rm tags syscall_64.tbl syscall_32.tbl

    read -r -e -p "Do you want to delete the kernel source code(${SRC_DIR}linux-${KERNEL_VERSION})? [y/n]? " choice
    [[ "$choice" == [Yy]* ]] && rm -rf "/tmp/linux-${KERNEL_VERSION}" "/tmp/linux-${KERNEL_VERSION}.tar.xz"

    # changes /tmp/linux* to /linux* in the function definions
    sed -i "s/\/tmp\/linux-${KERNEL_VERSION}\///g" syscalls.json
else
    echo "[-] syscalls.json already exists! delete it to generate another one."
fi

# install
if [ -f "syscalls" ] && [ -f "syscalls.json" ]; then
    sudo mkdir -p ${JSON_DIR}
    cp -av syscalls.json ${JSON_DIR}
    cp -av syscalls ${INSTALL_DIR}
    chmod u+x ${INSTALL_DIR}/syscalls
else
    echo "[-] syscalls or syscalls.json don't exist! installation failed."
fi

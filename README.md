# syscall-table-cli (64-bit and 32-bit)

Generate linux x86 and x86_64 system calls table JSON and parse it from command
line.

## Installation

-   Install python-ctags3 and terminaltables:
    ```
    pip install python-ctags3 terminaltables.
    ```
-   Change **INSTALL_DIR**, **JSON_DIR** and **JSON_PATH** from **install.sh**
    and **syscalls** to reflect you installation and json file directories
    preferences.
-   Change **SRC_DIR** and **KERNEL_VERSION** from **install.sh** to change
    which dir the source will be downloaded and the version to download. Or you
    can simply go to https://kernel.org and download the **KERNEL_VERSION**
    tarball, extract it to **SRC_DIR**.
-   Delete **syscalls.json** (to generate another one) and `./install.sh`. The
    script will download the kernel source code, generate the ctags, generate
    the JSON file and copy the **syscalls** script to **SRC_DIR** and
    **syscalls.json** to **JSON_DIR**.

**TL,DR**: If you are ok with the linux 5.4.72 version syscalls, installing the
script in _/usr/bin/_ and moving the JSON file to _/usr/share/syscalls/_ just
clone the repo and

```
pip install python-ctags3 terminaltables && ./install.sh
```

## Usage

Help:

```
syscalls -h
```

Search a x86 syscall:

```python
syscalls -a 32 QUERY
```

Search a x86_64 syscall (default):

```python
syscalls QUERY
```

<img src="https://media.giphy.com/media/QAdqr4ZEsXw4BMc115/giphy.gif" width=100% />

## Kernel versions

Tested with linux 5.4.72 and 4.14.202. should work with other versions too.

## You might want to see

-   https://syscalls64.paolostivanin.com/ by Paolo Stivanin
    (https://github.com/paolostivanin/syscalls-table-64bit)

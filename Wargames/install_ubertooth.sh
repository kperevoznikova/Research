#!/bin/bash
#4.19.0-kali5-amd64 (2019-07-22) x86_64 GNU/Linux

if [ `id -u` -eq 0 ] ; then 
    apt-get install cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev libpcap-dev python-numpy python-qt4
    #installing PySide
    #wget http://ftp.br.debian.org/debian/pool/main/q/qtmobility/qtmobility-dev_1.2.0-3+b1_amd64.deb

    if [ ! -e /usr/bin/pip ] ; then
        wget https://bootstrap.pypa.io/get-pip.py
        python get-pip.py
    fi
    pip install PySide

    #building libbtbb
    echo wget https://github.com/greatscottgadgets/libbtbb/archive/2018-12-R1.tar.gz -O libbtbb-2018-12-R1.tar.gz
    if [ $? -eq 0 ] ; then 
        tar -xf libbtbb-2018-12-R1.tar.gz
        cd libbtbb-2018-12-R1
        mkdir build
        cd build
        cmake ..
        make
        make install
        cd ../..
    else
        echo "Failed while trying to get libbtbb"
        exit 1
    fi

    #building ubertooth tools
    wget https://github.com/greatscottgadgets/ubertooth/releases/download/2018-12-R1/ubertooth-2018-12-R1.tar.xz
    if [ $? -eq 0 ] ; then 
        tar xf ubertooth-2018-12-R1.tar.xz
        cd ubertooth-2018-12-R1/host
        mkdir build
        cd build
        apt-get install pkg-config
        cmake ..
        make
        make install
        cd ../..
    else
        echo "Failed while trying to get ubertooth repo"
        exit 2
    fi

    #updating firmware
    cd ubertooth-one-firmware-bin
    ldconfig
    echo "Plug in ubertooth and press enter"
    read skip
    ubertooth-dfu -d bluetooth_rxtx.dfu -r
    ubertooth-util -v
else
    echo "Attention! Sudo required!"
fi
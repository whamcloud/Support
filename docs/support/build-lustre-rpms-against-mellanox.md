# Build Lustre RPMs against Mellanox

[Support Table of Contents](TOC.md)

## TOC

- [Obtaining the Vagrantfile](#obtaining-the-vagrantfile)
- [Downloading the Mellanox Driver](#downloading-the-mellanox-driver)
- [Upload the Mellanox Driver](#upload-the-mellanox-driver)
- [Build Mellanox Drivers against Lustre Kernel](#build-mellanox-drivers-against-lustre-kernel)
- [Download the Mellanox OFA Kernel Modules RPM](#download-the-mellanox-ofa-kernel-modules-rpm)
- [Building Lustre against the new Mellanox Driver](#building-lustre-against-the-new-mellanox-driver)
- [Download New Lustre RPMs](#download-new-lustre-rpms)
  - [For non-dkms RPMs](#for-non-dkms-rpms)
  - [For dkms RPMs](#for-dkms-rpms)
- [Rules for Distribution](#rules-for-distribution)
  - [For ZFS Filesystems](#for-zfs-filesystems)
    - [Using DKMS](#using-dkms)
    - [Not Using DKMS](#not-using-dkms)
  - [For ldiskfs Filesystems](#for-ldiskfs-filesystems)

If a network is using IB instead of Ethernet it may require mellanox. If this is the case, mellanox will need to be installed with kernel support against the Lustre kernel. Upon completion, a new mellanox tar file will be created. This compressed file will contain the mellanox driver rpm that was built against the kernel. To help automate this process, a vagrant box has been created, which has the latest Lustre kernel installed and all needed dependencies to build the mellanox driver against it. To get started, make sure you've installed vagrant on your system (see [Create a Virtual HPC Storage Cluster with Vagrant](https://github.com/whamcloud/Vagrantfiles)).

[Top](#build-lustre-rpms-against-mellanox)

## Obtaining the Vagrantfile

Use git to clone the [Vagrantfiles](https://github.com/whamcloud/Vagrantfiles) repo.

```bash
git clone https://github.com/whamcloud/Vagrantfiles
cd Vagrantfiles/mellanox-lustre
```

[Top](#build-lustre-rpms-against-mellanox)

## Downloading the Mellanox Driver

Next, download the desired mellanox driver. This file can be downloaded by navigating to `http://mellanox.com` -> `Support/Education` -> `Infiniband/VPI drivers` -> `Mellanox OFED Linux (MLNX_OFED)`. Scroll to the bottom of the page and click the `Download` tab. Select the appropriate parameters and click on the link marked `tgz`. Scroll to the bottom of the page and select the checkbox and finally, click `I Accept`. This will initiate the download. When the download completes, copy it into the `Vagrantfiles/mellanox-lustre` directory. 

[Top](#build-lustre-rpms-against-mellanox)

## Upload the Mellanox Driver

Make sure to change directories to Vagrantfiles/mellanox-lustre.

```bash
MLNX_OFED_LINUX=$(ls MLNX_OFED_LINUX*.tgz) vagrant provision default --provision-with upload-mellanox
```

[Top](#build-lustre-rpms-against-mellanox)

## Build Mellanox Drivers against Lustre Kernel

```bash
vagrant provision default --provision-with build-mellanox
```

[Top](#build-lustre-rpms-against-mellanox)

## Download the Mellanox OFA Kernel Modules RPM

```bash
vagrant port
#     22 (guest) => 2205 (host)
# Note that the password is `vagrant`
scp -P 2205 root@localhost:/tmp/MLNX_OFED_LINUX-*_lustre.x86_64/MLNX_OFED_LINUX-*-ext/RPMS/mlnx-ofa_kernel-modules-*_lustre*.rpm .
```

[Top](#build-lustre-rpms-against-mellanox)

## Building Lustre against the new Mellanox Driver

In addition to building out the mellanox rpm, Lustre must also be built against the new mellanox driver. Since the mellanox driver is now installed on the system, the rpm task can be run to generate the necessary rpms.

```bash
LUSTRE_BRANCH=b2_10 vagrant provision default --provision-with build-lustre-rpms
```

[Top](#build-lustre-rpms-against-mellanox)

## Download New Lustre RPMs

### For non-dkms RPMs

```bash
vagrant port
#     22 (guest) => 2205 (host)
# Note that the password is `vagrant`

scp -P 2205 root@localhost:/tmp/lustre-release/kmod-lustre-*.el7.centos.x86_64.rpm .
scp -P 2205 root@localhost:/tmp/lustre-release/kmod-lustre-osd-ldiskfs-*.centos.x86_64.rpm .
scp -P 2205 root@localhost:/tmp/lustre-release/lustre-*.el7.centos.x86_64.rpm .
scp -P 2205 root@localhost:/tmp/lustre-release/lustre-osd-ldiskfs-mount-*.el7.centos.x86_64.rpm .
scp -P 2205 root@localhost:/tmp/lustre-release/lustre-osd-zfs-mount-*.el7.centos.x86_64.rpm .
scp -P 2205 root@localhost:/tmp/lustre-release/lustre-resource-agents-*.el7.centos.x86_64.rpm
```

### For dkms RPMs

```bash
vagrant port
#     22 (guest) => 2205 (host)
# Note that the password is `vagrant`

TODO: Add dkms rpms here
```

[Top](#build-lustre-rpms-against-mellanox)

## Rules for Distribution

Unfortunately Spl and ZFS can not be distributed, which means that they must be built on the server where it is intended to be used. The purpose of the vagrant provisioning scripts is to make this process as simple as possible so that anyone can generate the rpm's for their system without having to worry about distribution. If the rpms need to be distributed, however, there are a few rules that should be followed:

### For ZFS Filesystems

The first thing that should be asked when distributing rpms for a zfs filesystem is whether or not *dkms* is being used. If not, this means that the filesystem was built by their own kmods and they will need to generate the Lustre kmods against their version of zfs. If they are using dkms then they will simply need to install Mellanox and recompile lustre. Kmod rpms (kmod-spl, kmod-zfs, etc) may not be distributed. 

#### Using DKMS

TODO: How to handle DKMS

#### Not Using DKMS

TODO: How to handle non-dkms

[Top](#build-lustre-rpms-against-mellanox)

### For ldiskfs Filesystems

Kmods for ldiskfs can be distributed. In general, the following files would be distributed for an ldiskfs filesystem:

```bash
kmod-lustre-*.el7.centos.x86_64.rpm
kmod-lustre-osd-ldiskfs-*.el7.centos.x86_64.rpm
lustre-*.el7.centos.x86_64.rpm
lustre-osd-ldiskfs-mount-*.el7.centos.x86_64.rpm
lustre-osd-zfs-mount-*.el7.centos.x86_64.rpm
lustre-resource-agents-*.el7.centos.x86_64.rpm
```

---

[Top](#build-lustre-rpms-against-mellanox)

# Simulating cloud-init Behavior in Proxmox LXC Containers

The Proxmox default templates are great, but are (as of: June 2025) a bit dated, requiring ~150 updates. For many of my VMs I use recent releases to minimize the repetitive application of updates before each is usable.  This guide extends that practice to LXC containers.

## 🧱 1. Download a Cloud-Ready Template

Download a recent, cloud-ready image from https://images.linuxcontainers.org/ like ubuntu noble amd64 cloud into ```Proxmox-VE/local/CT Templates```, ```Download from URL```.

For the specific URL, you're looking for the rootfs.tar.xz - https://images.linuxcontainers.org/images/ubuntu/noble/amd64/cloud/20250620_07:42/rootfs.tar.xz

And give it a Proxmox-VE friendly name like `ubuntu-24.04-latest_24.04-2_amd64.tar.xz`

Something like `update_cloud_image.sh` to download the latest:
```bash
#!/usr/bin/env bash
BASEURL=https://images.linuxcontainers.org/images/ubuntu/noble/amd64/cloud/
FILECOMP=rootfs.tar.xz
TARGET=ubuntu-24.04-latest_24.04-2_amd64.tar.xz
DIRCOMP=$(wget -qO- https://images.linuxcontainers.org/images/ubuntu/noble/amd64/cloud/ | \
               lynx -dump -listonly -nonumbers -stdin | tail -n 1 | awk -F / '{print $6}')
echo $DIRCOMP > current_container
if cmp -s current_container latest_container; then
   echo "Container image is current"
else
   echo "New image available. Fetching now."
   rm -f /var/lib/vz/template/cache/$TARGET
   wget https://images.linuxcontainers.org/images/ubuntu/noble/amd64/cloud/$DIRCOMP/$FILECOMP -O \
        /var/lib/vz/template/cache/$TARGET
   cp current_container latest_container
fi
```

Or, just use the `fetch_container_image` role!

## 🛠️ 2. Create (But Don’t Start) Your Container

Create your container through the gui, or the command line:

```bash
pct create 105 local:vztmpl/ubuntu-24.04-latest_24.04-2_amd64.tar.xz \
               --hostname piglet \
               --cores 1 --memory 2048 \
               --net0 name=eth0,bridge=vmbr0,ip=192.168.86.7/24,gw=192.168.86.1 \
               --rootfs local:8 \
               --unprivileged 1
```

Notice we're not starting it on creation!

## 🔧 3. Inject cloud-init Files into the RootFS

So before you start it do the following:

Mount the rootfs with:

```bash
pct mount 105
```

And you'll find the rootfs mounted at /var/lib/lxc/105/rootfs ! 

Create a ```meta-data``` file like:

```yaml
instance-id: ubuntu-lxc-2404
local-hostname: piglet
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.86.7/24
      gateway4: 192.168.86.1
      nameservers:
        addresses:
          - 192.168.86.1
          - 8.8.8.8
```

and a ```user-data``` file like:

```yaml
#cloud-config
hostname: piglet
manage_etc_hosts: true
users:
  - default
  - name: ubuntu
    groups: [adm, cdrom, dip, lxd, sudo]
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-rsa AAAA...your_key_here...
package_update: true
package_upgrade: true
packages:
  - openssh-server
```

and a ```90_nocloud.cfg``` file like:
```yaml
datasource:
  NoCloud:
    seedfrom: file:///var/lib/cloud/seed/nocloud-net/
```

Then create the cloud data diretory and copy some files!
```bash
mkdir -p /var/lib/lxc/105/rootfs/var/lib/cloud/seed/nocloud-net/
cp meta-data /var/lib/lxc/105/rootfs/var/lib/cloud/seed/nocloud-net/meta-data
cp user-data /var/lib/lxc/105/rootfs/var/lib/cloud/seed/nocloud-net/user-data
cp 90_nocloud.cfg /var/lib/lxc/105/rootfs/etc/cloud/cloud.cfg.d/90_nocloud.cfg
```

## ⚠️ 4. Tame Unprivileged Container Quirks

Now for a couple of non-obvious things:

- You may have observed that I specified an unprivileged container - that means root doesn't really mean root! and as you'll glean from the code below - user 100000 on the proxmox node maps to user 0 (root) in the container, and

- Even though the image is cloud _capable_, it is not cloud-enabled by default the ```cloud-init.disabled``` file prevents it!

```bash
chown -R 100000:100000 /var/lib/lxc/105/rootfs/var/lib/cloud
rm /var/lib/lxc/105/rootfs/etc/cloud/cloud-init.disabled
```

## 🚀 5. Launch and Verify

Now, feel free to:

```bash
pct start 105
```

and then ssh in as ubuntu!

```bash
ssh ubuntu@192.168.86.7
```
Cloud-init should have set the hostname, installed OpenSSH, and dropped in your key.

Have fun!

## 💡Bonus Suggestion: Wrap it up with Reusability

Want to clone this container setup for future projects? Use ```pct clone``` or turn it into a template once it’s working.


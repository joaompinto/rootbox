
# LXC
rootbox uses linux distribution containers (LXC) from the LXC project:lx
https://linuxcontainers.org/

The index is obtained from: https://images.linuxcontainers.org/meta/1.0/index-user

The images are obtained from: https://images.linuxcontainers.org/images

The url to download the images is const5ructed from the index using the following template:

```python
# Python snippet
LXC_URL_TEMPL = 'https://images.linuxcontainers.org/images/{}/{}/{}/{}/{}/rootfs.tar.xz'
url = LXC_URL_TEMPL.format(image_name, distro_version, distro_arch, distro_variant, distro_build)
```

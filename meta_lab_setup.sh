"config: {}
networks:
- config:
    ipv4.address: 10.154.149.1/24
    ipv4.nat: "true"
    ipv6.address: fd42:f54a:d008:5776::1/64
    ipv6.nat: "true"
  description: ""
  name: lxdbr0
  type: bridge
  project: default
- config:
    ipv4.address: none
    ipv6.address: none
  description: ""
  name: rt
  type: bridge
  project: default
- config:
    ipv4.address: none
    ipv6.address: none
  description: ""
  name: tc
  type: bridge
  project: default
storage_pools:
- config:
    source: /var/snap/lxd/common/lxd/storage-pools/default
  description: ""
  name: default
  driver: dir
profiles:
- config: {}
  description: Default LXD profile
  devices:
    eth0:
      name: eth0
      network: lxdbr0
      type: nic
    root:
      path: /
      pool: default
      type: disk
  name: default
